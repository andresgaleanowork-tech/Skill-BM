#!/usr/bin/env python3
"""Carga manual de precios (el área de Iberdrola está bloqueada: se copian a mano).

Pensado para pegar un bloque de texto, no para teclear formularios.

Formato admitido (una línea por producto):

    3.0TD Empresa Flex | TP: 20,376927 10,617621 4,481534 3,886333 2,513851 1,442287
                       | TE: 0,253955 0,209968 0,180518 0,157978 0,149284 0,152954

    2.0TD Plan Exclusivo 15%TE/TP 1p | TP: 43,99 31,99 | TE: 0,241059

Uso:
    python tools/cargar_precios.py bandeja/precios/ficha_16112026.txt
    python tools/cargar_precios.py --plantilla     (imprime una ficha vacía)

Genera/actualiza `precios.json` en la raíz del paquete y una ficha legible en
`metricas/precios/ficha_DDMMAAAA.md`. Nunca inventa valores: si una línea está
incompleta, la rechaza y sigue con las demás.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
JSON = RAIZ / 'precios.json'
FICHAS = RAIZ / 'metricas' / 'precios'

PLANTILLA = """# Ficha de precios · copiar a mano de la Agencia Ágora (área bloqueada)
# Fecha de la hoja: DD/MM/AAAA
# Formato: PRODUCTO | TP: valores separados por espacios | TE: valores separados por espacios
# En 3.0TD y 6.xTD: seis TP y seis TE (P1..P6). En 2.0TD: dos TP y uno a tres TE.

3.0TD Empresa Flex | TP: | TE:
6.1TD Empresa Flex | TP: | TE:
2.0TD Plan Exclusivo 15%TE/TP 1p | TP: | TE:
"""


def a_num(txt):
    return float(txt.replace('.', '').replace(',', '.')) if ',' in txt else float(txt)


def parsear(texto):
    fecha = None
    productos, errores = {}, []
    for linea in texto.splitlines():
        l = linea.strip()
        if not l or l.startswith('#'):
            m = re.search(r'(\d{2})/(\d{2})/(\d{4})', l or '')
            if m:
                fecha = f'{m.group(3)}-{m.group(2)}-{m.group(1)}'
            continue
        if '|' not in l:
            errores.append(f'línea sin separador |: {l[:50]}')
            continue
        partes = [p.strip() for p in l.split('|')]
        nombre = partes[0]
        tp = te = None
        for p in partes[1:]:
            if p.upper().startswith('TP'):
                tp = [a_num(x) for x in p.split(':', 1)[1].split()]
            elif p.upper().startswith('TE'):
                te = [a_num(x) for x in p.split(':', 1)[1].split()]
        if not tp or not te:
            errores.append(f'{nombre}: faltan TP o TE')
            continue
        familias_6 = nombre.startswith(('3.0TD', '6.'))
        if familias_6 and (len(tp) != 6 or len(te) != 6):
            errores.append(f'{nombre}: se esperaban 6 TP y 6 TE, hay {len(tp)} y {len(te)}')
            continue
        if nombre.startswith('2.0TD') and (len(tp) != 2 or len(te) > 3):
            errores.append(f'{nombre}: se esperaban 2 TP y 1-3 TE, hay {len(tp)} y {len(te)}')
            continue
        productos[nombre] = {'tp': tp, 'te': te}
    return fecha, productos, errores


def comparar(productos):
    """Avisos de coherencia frente a la carga anterior. No bloquea: avisa."""
    if not JSON.exists():
        return ['No hay carga anterior con la que comparar.']
    anterior = json.loads(JSON.read_text(encoding='utf-8'))['productos']
    avisos = []
    for nombre, datos in productos.items():
        previo = anterior.get(nombre)
        if not previo:
            avisos.append(f'{nombre}: producto nuevo respecto a la carga anterior.')
            continue
        for campo in ('tp', 'te'):
            a, b = previo.get(campo), datos.get(campo)
            if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
                for i, (x, y) in enumerate(zip(a, b), 1):
                    if x and abs((y - x) / x) > 0.25:
                        avisos.append(f'{nombre}: {campo.upper()}{i} cambia un {round((y-x)/x*100,1)} % ({x} -> {y}). ¿Error de copia?')
                    elif abs(x - y) < 1e-12:
                        pass
    return avisos


def main(ruta=None):
    if ruta == '--plantilla':
        print(PLANTILLA)
        return
    if not ruta:
        print(__doc__)
        sys.exit(1)
    texto = Path(ruta).read_text(encoding='utf-8')
    fecha, productos, errores = parsear(texto)
    if not productos:
        print('No se ha podido leer ningún producto. Revisa el formato con --plantilla')
        for e in errores:
            print('  -', e)
        sys.exit(1)
    datos = {'fecha_hoja': fecha or 'sin fecha (¡anotarla!)', 'cargado': date.today().isoformat(),
             'origen': ruta, 'productos': productos}
    JSON.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding='utf-8')
    FICHAS.mkdir(parents=True, exist_ok=True)
    nombre_ficha = FICHAS / f'ficha_{(fecha or date.today().isoformat()).replace("-","")}.md'
    filas = '\n'.join(
        f"| {n} | {' · '.join(f'{x:.6f}'.replace('.', ',') for x in d['tp'])} | {' · '.join(f'{x:.6f}'.replace('.', ',') for x in d['te'])} |"
        for n, d in productos.items())
    nombre_ficha.write_text(
        f"# Ficha de precios · hoja del {datos['fecha_hoja']}\n\n"
        f"Cargada el {datos['cargado']} desde `{ruta}` (copia manual, área de Iberdrola bloqueada).\n\n"
        f"| Producto | TP €/kW·año | TE €/kWh |\n|---|---|---|\n{filas}\n", encoding='utf-8')
    print(f'{len(productos)} productos cargados · hoja del {datos["fecha_hoja"]}')
    print(f'  JSON:  {JSON}')
    print(f'  Ficha: {nombre_ficha}')
    if errores:
        print('\nLíneas rechazadas:')
        for e in errores:
            print('  -', e)
    avisos = comparar(productos)
    if avisos:
        print('\nAvisos:')
        for a in avisos:
            print('  -', a)
    print('\nSiguiente paso: python eval/run.py (si un caso de precios falla, es que la hoja ha cambiado de verdad)')


if __name__ == '__main__':
    main(*sys.argv[1:])
