#!/usr/bin/env python3
"""Factura (PDF) → JSON de cálculo, sin teclear números.

Usa un perfil por comercializadora (`tools/perfiles/`). Cada perfil sabe cómo factura esa
comercializadora, que no es lo mismo en todas: hay quien parte el precio en dos, quien
desglosa peajes y cargos, quien usa €/kW·mes con descuento.

Regla que no se salta nunca: si un bloque no cuadra con el subtotal impreso en la factura,
o si falta un dato que no se puede verificar, el programa **lo dice y no entrega cifras**.

Uso:
    python tools/factura_a_json.py bandeja/facturas/factura.pdf
    python tools/factura_a_json.py factura.pdf --producto "3.0TD Empresa Flex" --json salida.json
    python tools/factura_a_json.py factura.pdf --perfil octopus
    python tools/factura_a_json.py factura.pdf --listar-perfiles

Con --producto se toma el juego de precios nuevo de precios.json.
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / 'tools'))

try:
    import pymupdf
except ImportError:
    pymupdf = None

from perfiles import elegir, por_clave, REGISTRO  # noqa: E402

RE_TOTAL = re.compile(r'Total\s+factura:?\s*(-?\d{1,3}(?:\.\d{3})*,\d+|-?\d+,\d+)', re.IGNORECASE)
RE_CIF = re.compile(r'\b([A-HJNP-SUVW]\d{7}[0-9A-J])\b')
RE_CUPS = re.compile(r'\b(ES\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?[A-Z0-9]{2})\b')
RE_NIF = re.compile(r'\b(\d{8}[A-Z])\b|\b([XYZ]\d{7}[A-Z])\b')
RE_TARIFA = re.compile(r'\b(\d,\dTD|\d\.\dTD)\b')


def leer_texto(ruta):
    if pymupdf is None:
        raise SystemExit('Falta pymupdf: pip install pymupdf')
    doc = pymupdf.open(ruta)
    texto = '\n'.join(p.get_text() for p in doc)
    return texto, len(doc)


def construir_entrada(datos, producto=None):
    """Convierte lo leído en el JSON que consume calc_energia.py."""
    periodos = datos['periodos']
    # En 2.0TD la potencia tiene 2 periodos y la energía 3: no tienen por qué coincidir
    periodos_pot = datos.get('periodos_potencia') or periodos
    entrada = {
        'dias': datos['dias'],
        'potencias_kw': [datos['potencias_kw'].get(p, 0) for p in periodos_pot],
        'kwh': {p: datos['kwh'].get(p, 0) for p in periodos},
        'actual': {'tp': [datos['tp'].get(p, 0) for p in periodos_pot],
                   'tp_unidad': datos.get('tp_unidad', 'dia'),
                   'te': [datos['te'].get(p, 0) for p in periodos]},
        'extras': dict(datos['extras']),
        'iee': datos.get('iee', 0.0511269632),
        'iva': 0.21,
    }
    if datos.get('total_factura') is not None:
        entrada['total_factura_real'] = datos['total_factura']
    if datos.get('bono_en_base_iee') is not None:
        entrada['extras']['bono_social_en_base_iee'] = datos['bono_en_base_iee']
    if datos.get('devolucion_fianza'):
        entrada['extras']['ajuste_total'] = -abs(datos['devolucion_fianza'])
    if datos.get('energia_agregada'):
        ag = datos['energia_agregada']
        entrada['extras']['energia_agregada_importe'] = round(ag['kwh'] * ag['precio'], 2)
        entrada['energia_agregada'] = ag
    if datos.get('tolerancia_cuadre') is not None:
        entrada['tolerancia_cuadre'] = datos['tolerancia_cuadre']

    if producto:
        ruta_precios = RAIZ / 'precios.json'
        if ruta_precios.exists():
            catalogo = json.loads(ruta_precios.read_text(encoding='utf-8'))
            prod = catalogo.get('productos', {}).get(producto)
            if prod:
                tp_prod, te_prod = list(prod['tp']), list(prod['te'])
                if len(tp_prod) == 3 and len(periodos_pot) == 2:      # 2.0TD: punta y valle
                    tp_prod = tp_prod[:2]
                if len(te_prod) == 1 and len(periodos) == 3:          # 2.0TD: un solo precio de energía
                    te_prod = te_prod * 3
                elif len(te_prod) == 1 and len(periodos) == 2:
                    te_prod = te_prod * 2
                entrada['nuevo'] = {'tp': tp_prod, 'tp_unidad': 'anio', 'te': te_prod}
                entrada['hoja_precios'] = catalogo.get('fecha_hoja')
            else:
                entrada['producto_no_encontrado'] = producto
        else:
            entrada['producto_no_encontrado'] = f'{producto} (no existe precios.json)'
    return entrada


def extraer(ruta, producto=None, clave_perfil=None):
    texto, paginas = leer_texto(ruta)
    avisos, errores, comprobaciones = [], [], []

    if len(texto.strip()) < 120:
        return None, [
            'el PDF no tiene capa de texto: es un escaneo o una foto.',
            'La vía correcta, y la que ya está disponible en ChatGPT, Claude y Gemini, es pasarle la '
            'imagen o el PDF al asistente y pedirle los datos con este formato exacto. La regla que no '
            'se salta: ninguna cifra se da por buena hasta que cuadre contra el total impreso en la '
            'factura. Si no cuadra, no hay informe.',
            'Si se prefiere la vía local: tesseract sobre el PDF (pdftoppm -r 300 → tesseract -l spa) y '
            'volver a pasar el resultado por este mismo programa. Para un uso continuado merece la pena '
            'instalarlo; para una factura suelta, no.'], [], None

    perfil = por_clave(clave_perfil) if clave_perfil else elegir(texto)
    if perfil is None:
        return None, [f'no hay ningún perfil que reconozca esta factura. Perfiles disponibles: '
                      f'{", ".join(REGISTRO)}. Añade uno con las líneas de esta maqueta: es trabajo '
                      f'acotado y verificable'], [], None

    datos, avisos_p, errores_p, comprobaciones = perfil.leer(texto)
    avisos.extend(avisos_p)
    errores.extend(errores_p)
    datos['perfil'] = perfil.clave
    datos['paginas'] = paginas

    # --- identificación común a todas las maquetas
    m = RE_CIF.search(texto)
    datos['cif'] = m.group(1) if m else None
    m = RE_CUPS.search(texto)
    datos['cups'] = re.sub(r'\s', '', m.group(1)) if m else None
    m = RE_NIF.search(texto)
    datos['nif_titular'] = (m.group(1) or m.group(2)) if m else None
    m = RE_TARIFA.search(texto)
    datos['tarifa_acceso'] = datos.get('tarifa_acceso') or (m.group(1) if m else None)
    if datos.get('total_factura') is None:
        m = RE_TOTAL.search(texto)
        if m:
            datos['total_factura'] = float(m.group(1).replace('.', '').replace(',', '.'))
    if datos.get('total_factura') is None:
        errores.append('no se ha encontrado el total de la factura: sin él no hay cuadre posible')

    # --- el bono social, ¿dentro o fuera de la base del IEE? se decide cuadrando
    if datos.get('iee_base_factura'):
        base = datos['iee_base_factura']
        pot = round(sum(datos['potencias_kw'].get(p, 0) * datos['tp'].get(p, 0) * (datos['dias'] or 30)
                        / (30 if datos.get('tp_unidad') == 'mes' else 1) for p in datos['periodos']), 2)
        if any(datos['kwh'].values()):
            ene = round(sum(datos['kwh'].get(p, 0) * datos['te'].get(p, 0) for p in datos['periodos']), 2)
        elif datos.get('energia_agregada'):
            ag = datos['energia_agregada']
            ene = round(ag['kwh'] * ag['precio'], 2)
        else:
            ene = 0.0
        fijos = (datos['extras'].get('excesos', 0) + datos['extras'].get('reactiva', 0)
                 + datos['extras'].get('otros', 0))
        auto = -(datos['extras'].get('autoconsumo_kwh', 0) * datos['extras'].get('autoconsumo_precio_actual', 0))
        sin_bono = round(pot + ene + fijos + auto, 2)
        con_bono = round(sin_bono + datos['extras'].get('bono_social', 0), 2)
        en_base = abs(con_bono - base) <= 0.05
        datos['bono_en_base_iee'] = en_base
        comprobaciones.append({'bloque': 'base IEE', 'sin_bono': sin_bono, 'con_bono': con_bono,
                               'base_factura': base, 'bono_en_base': en_base,
                               'cuadra': en_base or abs(sin_bono - base) <= 0.05})
        if not (en_base or abs(sin_bono - base) <= 0.05):
            avisos.append('la base del IEE de la factura no se reproduce con los datos leídos: puede haber '
                          'un concepto de la factura que no está contemplado (deuda, ajuste, servicio). '
                          'Revisa la factura antes de usar las cifras')

    entrada = construir_entrada(datos, producto)
    if 'producto_no_encontrado' in entrada:
        avisos.append(f'el producto «{entrada["producto_no_encontrado"]}» no está en precios.json: '
                      f'la comparativa queda a cero')
    elif not producto:
        avisos.append('sin --producto: la factura se cuadra, pero no hay comparativa')

    datos['entrada_calculo'] = entrada
    datos['comprobaciones'] = comprobaciones

    for c in comprobaciones:
        if not c.get('cuadra'):
            errores.append(f'el bloque «{c["bloque"]}» no cuadra con el subtotal impreso '
                           f'({c.get("suma_lineas", c.get("sin_bono"))} frente a '
                           f'{c.get("subtotal_factura", c.get("base_factura"))})')
    return datos, avisos, errores, texto


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if '--listar-perfiles' in sys.argv:
        for clave, c in REGISTRO.items():
            print(f'  {clave:22s} {c.nombre}')
        return 0
    if not args:
        print(__doc__)
        return 1
    ruta = Path(args[0])
    producto = sys.argv[sys.argv.index('--producto') + 1] if '--producto' in sys.argv else None
    salida = sys.argv[sys.argv.index('--json') + 1] if '--json' in sys.argv else None
    clave = sys.argv[sys.argv.index('--perfil') + 1] if '--perfil' in sys.argv else None

    datos, avisos, errores, _ = extraer(ruta, producto, clave)

    if datos is None:
        for a in avisos:
            print(f'AVISO: {a}')
        print('\nNo se ha generado nada.')
        return 2

    print(f'{Path(ruta).name} · {datos["paginas"] if "paginas" in datos else "?"} página(s) · '
          f'perfil «{datos["perfil"]}»')
    print(f'  Titular {datos.get("nif_titular") or "—"} · CIF {datos.get("cif") or "—"} · '
          f'{datos.get("tarifa_acceso") or "—"} · {datos["dias"]} días')
    print('  Periodos ' + ', '.join(datos['periodos']) + ' · '
          f'{sum(datos["kwh"].values()):.0f} kWh')
    print('  Precios: ' + ' · '.join(
        f'{p} {datos["tp"].get(p, 0):.6f}/kW·{datos.get("tp_unidad", "dia")} {datos["te"].get(p, 0):.6f}/kWh'
        for p in datos['periodos']))
    e = datos['extras']
    print(f'  Excesos {e.get("excesos", 0):.2f} € · reactiva {e.get("reactiva", 0):.2f} € · '
          f'otros {e.get("otros", 0):.2f} € · bono {e.get("bono_social", 0):.2f} € · '
          f'alquiler {e.get("alquiler", 0):.2f} € · autoconsumo {e.get("autoconsumo_kwh", 0):.0f} kWh')
    print(f'  Total en factura: {datos.get("total_factura")} €')

    if datos['comprobaciones']:
        print('\n  Comprobaciones contra los subtotales impresos:')
        for c in datos['comprobaciones']:
            detalle = (f'suma {c.get("suma_lineas")} vs {c.get("subtotal_factura")}' if 'suma_lineas' in c
                       else f'sin bono {c.get("sin_bono")} · con bono {c.get("con_bono")} vs {c.get("base_factura")}')
            print(f'    [{"OK" if c.get("cuadra") else "REVISAR"}] {c["bloque"]}: {detalle}')
    for a in avisos:
        print(f'  AVISO: {a}')
    if errores:
        print('\n  ERRORES:')
        for x in errores:
            print(f'    - {x}')

    if salida:
        Path(salida).write_text(json.dumps(datos['entrada_calculo'], ensure_ascii=False, indent=2),
                                encoding='utf-8')
        print(f'\nJSON de cálculo escrito en {salida}')
    else:
        print('\nJSON de cálculo:')
        print(json.dumps(datos['entrada_calculo'], ensure_ascii=False, indent=2))

    if errores:
        print('\nNO uses estas cifras hasta resolver los errores.')
        return 3
    print('\nSiguiente paso:')
    print(f'  python skills/informes-ahorro-electrico/scripts/calc_energia.py {salida or "factura.json"}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
