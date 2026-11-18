#!/usr/bin/env python3
"""Batería de pruebas del paquete de skills B&M.

Uso:  python eval/run.py            (desde la raíz del paquete)
      python eval/run.py --verbose
Requiere: pymupdf para los casos de precios.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CASOS = json.loads((RAIZ / 'eval' / 'casos.json').read_text(encoding='utf-8'))['casos']
VERBOSE = '--verbose' in sys.argv


def leer(d, ruta):
    cur = d
    for parte in ruta.split('.'):
        cur = cur[parte]
    return cur


def caso_calc(caso, entradas):
    entrada = caso.get('entrada') or entradas[caso['entrada_ref']]
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(entrada, f, ensure_ascii=False)
        ruta = f.name
    r = subprocess.run([sys.executable, str(RAIZ / 'skills/informes-ahorro-electrico/scripts/calc_energia.py'), ruta],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return False, f'error al ejecutar calc_energia: {r.stderr.strip()[:200]}'
    salida = json.loads(r.stdout)
    fallos = []
    for clave, esperado in caso['esperado'].items():
        obtenido = leer(salida, clave)
        if isinstance(esperado, float):
            ok = abs(obtenido - esperado) < 0.02
        else:
            ok = obtenido == esperado
        if not ok:
            fallos.append(f'{clave}: esperado {esperado}, obtenido {obtenido}')
    return (not fallos), '; '.join(fallos)


def caso_negativo(caso):
    """Un caso negativo pasa cuando la calculadora SE NIEGA: código de salida y motivo esperados."""
    entrada = caso['entrada']
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(entrada, f, ensure_ascii=False)
        ruta = f.name
    r = subprocess.run([sys.executable, str(RAIZ / 'skills/informes-ahorro-electrico/scripts/calc_energia.py'), ruta],
                       capture_output=True, text=True)
    esperado_rc = caso.get('esperado_rc', 2)
    if r.returncode != esperado_rc:
        return False, f'código de salida {r.returncode}, se esperaba {esperado_rc}. stderr: {r.stderr.strip()[:200]}'
    texto = caso.get('esperado_error') or caso.get('esperado_aviso') or ''
    if texto and texto not in (r.stderr + r.stdout):
        return False, f'no aparece el motivo esperado «{texto}» en la salida'
    return True, ''


def caso_factura_pdf(caso):
    """Cadena completa: PDF de factura → JSON → cálculo. Se omite si el PDF de ejemplo no está."""
    entrada = caso['entrada']
    pdf = RAIZ / entrada['pdf']
    if not pdf.exists():
        return None, f'PDF de ejemplo no encontrado en {entrada["pdf"]} (caso omitido)'
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8') as f:
        ruta = f.name
    orden = [sys.executable, str(RAIZ / 'tools/factura_a_json.py'), str(pdf), '--json', ruta]
    if entrada.get('producto'):
        orden[3:3] = ['--producto', entrada['producto']]
    r = subprocess.run(orden, capture_output=True, text=True)
    if r.returncode != 0:
        return False, f'la extracción falló (código {r.returncode}): {(r.stdout + r.stderr).strip()[-300:]}'
    r2 = subprocess.run([sys.executable, str(RAIZ / 'skills/informes-ahorro-electrico/scripts/calc_energia.py'), ruta],
                        capture_output=True, text=True)
    if r2.returncode != 0:
        return False, f'el cálculo falló: {r2.stderr.strip()[:200]}'
    salida = json.loads(r2.stdout)
    fallos = []
    for clave, esperado in caso['esperado'].items():
        obtenido = leer(salida, clave)
        if isinstance(esperado, float):
            ok = abs(obtenido - esperado) < 0.02
        else:
            ok = obtenido == esperado
        if not ok:
            fallos.append(f'{clave}: esperado {esperado}, obtenido {obtenido}')
    return (not fallos), '; '.join(fallos)


def caso_anualizar(caso):
    """Cadena completa: SIPS + factura → JSON anualizado → cálculo anual."""
    entrada = caso['entrada']
    sips = RAIZ / entrada['sips']
    factura = RAIZ / entrada['factura']
    for f in (sips, factura):
        if not f.exists():
            return None, f'falta {f.name} (caso omitido)'
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8') as tf:
        ruta_factura = tf.name
    r = subprocess.run([sys.executable, str(RAIZ / 'tools/factura_a_json.py'), str(factura),
                        '--json', ruta_factura], capture_output=True, text=True)
    if r.returncode != 0:
        return False, f'la extracción de la factura falló: {(r.stdout + r.stderr).strip()[-250:]}'
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8') as tf:
        ruta_anual = tf.name
    r = subprocess.run([sys.executable, str(RAIZ / 'tools/anualizar.py'), '--sips', str(sips),
                        '--factura', ruta_factura, '--producto', entrada['producto'],
                        '--json', ruta_anual], capture_output=True, text=True)
    if r.returncode != 0:
        return False, f'la anualización falló: {(r.stdout + r.stderr).strip()[-250:]}'
    r = subprocess.run([sys.executable, str(RAIZ / 'skills/informes-ahorro-electrico/scripts/calc_energia.py'),
                        ruta_anual], capture_output=True, text=True)
    if r.returncode != 0:
        return False, f'el cálculo anual falló: {r.stderr.strip()[:200]}'
    salida = json.loads(r.stdout)
    fallos = []
    for clave, esperado in caso['esperado'].items():
        obtenido = leer(salida, clave)
        if isinstance(esperado, float) and isinstance(obtenido, (int, float)):
            ok = abs(obtenido - esperado) < 0.05
        else:
            ok = obtenido == esperado
        if not ok:
            fallos.append(f'{clave}: esperado {esperado}, obtenido {obtenido}')
    return (not fallos), '; '.join(fallos)


def caso_plantilla(caso):
    """La plantilla se rellena sola: los logos quedan incrustados y no sobra ningún marcador."""
    import re
    tipo = caso['entrada']['tipo']
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8') as tf:
        salida = tf.name
    r = subprocess.run([sys.executable, str(RAIZ / 'tools/rellenar_plantilla.py'),
                        '--tipo', tipo, '--salida', salida], capture_output=True, text=True)
    if r.returncode not in (0, 2):          # 2 = quedan datos por rellenar, normal sin --datos
        return False, f'la plantilla no se generó: {(r.stdout + r.stderr).strip()[:250]}'
    html = Path(salida).read_text(encoding='utf-8')
    png = len(re.findall(r'data:image/png;base64,', html))
    jpeg = len(re.findall(r'data:image/jpeg;base64,', html))
    quedan = len(re.findall(r'\{\{LOGO_[A-Z_]+\}\}', html))
    esperado = caso['esperado']
    fallos = []
    if 'png' in esperado and png != esperado['png']:
        fallos.append(f'logos B&M incrustados: esperado {esperado["png"]}, hay {png}')
    if 'jpeg' in esperado and jpeg != esperado['jpeg']:
        fallos.append(f'logos Iberdrola incrustados: esperado {esperado["jpeg"]}, hay {jpeg}')
    if 'marcadores_logo' in esperado and quedan != esperado['marcadores_logo']:
        fallos.append(f'marcadores de logo sin sustituir: {quedan}')
    if esperado.get('solo_bm') and jpeg:
        fallos.append('el documento dice «solo B&M» pero lleva imágenes JPEG (Iberdrola)')
    return (not fallos), '; '.join(fallos)


def caso_precios(caso):
    """Comprueba la carga manual de precios contra los valores de referencia."""
    entrada = caso['entrada']
    ficha = RAIZ / entrada['ficha']
    if not ficha.exists():
        return False, f'no existe la ficha {entrada["ficha"]}'
    r = subprocess.run([sys.executable, str(RAIZ / 'tools/cargar_precios.py'), str(ficha)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return False, f'la ficha no se pudo cargar: {r.stderr.strip()[:160]}'
    datos = json.loads((RAIZ / 'precios.json').read_text(encoding='utf-8'))['productos'].get(entrada['producto'])
    if not datos:
        return False, f'producto {entrada["producto"]} no está en la ficha'
    fallos = []
    for clave, esperado in caso['esperado'].items():
        obtenido = datos.get(clave)
        if obtenido is None or len(obtenido) != len(esperado) or any(abs(a - b) > 1e-6 for a, b in zip(obtenido, esperado)):
            fallos.append(f'{clave}: esperado {esperado}, obtenido {obtenido}')
    return (not fallos), '; '.join(fallos)


def main():
    entradas = {c['id']: c['entrada'] for c in CASOS if 'entrada' in c}
    ok_total = 0
    omitidos = 0
    for caso in CASOS:
        herramienta = caso['herramienta']
        if herramienta == 'calc_energia':
            ok, msg = caso_calc(caso, entradas)
        elif herramienta == 'factura_pdf':
            ok, msg = caso_factura_pdf(caso)
            if ok is None:
                print(f'[OMITE] {caso["id"]:16s} {msg}')
                omitidos += 1
                continue
        elif herramienta == 'anualizar':
            ok, msg = caso_anualizar(caso)
            if ok is None:
                print(f'[OMITE] {caso["id"]:16s} {msg}')
                omitidos += 1
                continue
        elif herramienta == 'plantilla':
            ok, msg = caso_plantilla(caso)
        elif herramienta == 'calc_negativo':
            ok, msg = caso_negativo(caso)
        elif herramienta == 'cargar_precios':
            ok, msg = caso_precios(caso)
        else:
            ok, msg = False, f'herramienta desconocida: {herramienta}'
        estado = 'PASA' if ok else 'FALLA'
        print(f'[{estado}] {caso["id"]:16s} {caso["descripcion"][:70]}')
        if not ok or VERBOSE:
            print(f'         {msg}')
        ok_total += ok
    evaluables = len(CASOS) - omitidos
    sufijo = f' ({omitidos} omitido(s): falta el documento de muestra en local)' if omitidos else ''
    print(f'\n{ok_total}/{evaluables} casos correctos{sufijo}')
    if ok_total != evaluables:
        print('Si el fallo viene de una hoja de precios nueva, actualiza eval/casos.json a propósito y anótalo en metricas/bitacora.md')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())