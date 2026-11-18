#!/usr/bin/env python3
"""Anualización REAL del consumo: SIPS o las doce facturas del año.

Por qué existe: anualizar «12 recibos equivalentes» es una proyección, y las proyecciones
se caen en la primera conversación con el cliente. Con el SIPS (o con doce facturas) el
ahorro anual deja de ser una estimación y pasa a ser un cálculo con el perfil real.

Orden de preferencia, que es el que debe seguir el comercial:

    1. SIPS / fichero de consumos de la distribuidora   → perfil real por periodos
    2. Doce facturas del último año                     → mismo resultado, más trabajo
    3. Una sola factura                                 → modo B: se advierte de que es proyección

En la Comunidad Valenciana la distribuidora es i-DE (Iberdrola) en la práctica totalidad
del territorio, así que el SIPS se puede pedir. Si el suministro es de otra distribuidora
y no hay acceso, se piden las doce facturas.

Uso:
    python tools/anualizar.py --sips bandeja/facturas/sips.pdf
    python tools/anualizar.py --sips sips.pdf --factura factura.json --producto "3.0TD Empresa Flex" --json anual.json
    python tools/anualizar.py --facturas bandeja/facturas/ano2026/ --json anual.json

El JSON que sale con --factura y --producto entra directamente en calc_energia.py.
"""
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / 'tools'))

try:
    import pymupdf
except ImportError:
    pymupdf = None

PERIODOS_6 = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6']
PERIODOS_3 = ['P1', 'P2', 'P3']
MESES_MINIMOS = 11          # por debajo de esto no se considera año completo


def leer_tabla(ruta):
    """Devuelve las filas de la tabla SIPS como listas de celdas.

    El SIPS se exporta de tres maneras y hay que admitirlas todas:
      · CSV/TSV con separador (lo más cómodo),
      · PDF con la tabla de verdad (celdas alineadas en columnas),
      · PDF donde cada celda ha salido en su propia línea (caso de i-DE).
    """
    ruta = Path(ruta)
    if ruta.suffix.lower() in ('.csv', '.txt'):
        texto = ruta.read_text(encoding='utf-8', errors='ignore')
        filas = []
        for linea in texto.splitlines():
            for sep in ('|', ';', '\t', ','):
                if sep in linea:
                    celdas = [c.strip() for c in linea.split(sep)]
                    if any(re.fullmatch(r'\d{1,2}/\d{1,2}/\d{4}', c) for c in celdas):
                        filas.append(celdas)
                    break
        return filas

    if pymupdf is None:
        raise SystemExit('Falta pymupdf: pip install pymupdf')
    doc = pymupdf.open(ruta)

    # 1) intento por columnas reales del PDF (lo más fiable cuando existe la tabla)
    filas = []
    for pagina in doc:
        try:
            for tabla in pagina.find_tables():
                for fila in tabla.extract():
                    celdas = [(c or '').strip() for c in fila]
                    if sum(1 for c in celdas if re.fullmatch(r'\d{1,2}/\d{1,2}/\d{4}', c)) >= 2:
                        filas.append(celdas)
        except Exception:                      # noqa: BLE001  (PDF sin tablas detectables)
            continue
    if filas:
        return filas

    # 2) intento por líneas con separador
    texto = '\n'.join(p.get_text() for p in doc)
    for linea in texto.splitlines():
        for sep in ('|', ';', '\t'):
            if sep in linea:
                celdas = [c.strip() for c in linea.split(sep)]
                if any(re.fullmatch(r'\d{1,2}/\d{1,2}/\d{4}', c) for c in celdas):
                    filas.append(celdas)
                break
    if filas:
        return filas

    # 3) cada celda en una línea: se recompone la fila a partir de la primera fecha
    lineas = [l.strip() for l in texto.splitlines() if l.strip()]
    i = 0
    while i < len(lineas):
        if re.fullmatch(r'\d{1,2}/\d{1,2}/\d{4}', lineas[i]):
            bloque = [lineas[i]]
            j = i + 1
            while j < len(lineas) and re.fullmatch(r'-?\d+(?:[.,]\d+)?', lineas[j]):
                bloque.append(lineas[j])
                j += 1
            if len(bloque) >= 3:
                filas.append(bloque)
            i = j
        else:
            i += 1
    return filas


def parsear_sips(ruta):
    filas = leer_tabla(ruta)
    if not filas:
        raise SystemExit('no se ha encontrado ninguna fila con fechas: el fichero no parece un SIPS '
                         'en formato de tabla. Exporta el SIPS a CSV o revisa el PDF.')

    registros = []
    avisos = []
    for celdas in filas:
        idx = [i for i, c in enumerate(celdas) if re.fullmatch(r'\d{1,2}/\d{1,2}/\d{4}', c)]
        if len(idx) < 2:
            # formato «cada celda en una línea»: fecha inicio, fecha fin y 7 energías
            if len(celdas) >= 3 and all(re.fullmatch(r'-?\d+(?:[.,]\d+)?', c) for c in celdas[1:]):
                fechas = [datetime.strptime(celdas[0], '%d/%m/%Y').date(),
                          datetime.strptime(celdas[1], '%d/%m/%Y').date()]
                numeros = [float(c.replace('.', '').replace(',', '.')) for c in celdas[2:9]]
                if len(numeros) == 7:
                    registros.append({'desde': fechas[0], 'hasta': fechas[1], 'energia': numeros})
            continue
        i0, i1 = idx[0], idx[1]
        fechas = [datetime.strptime(celdas[i], '%d/%m/%Y').date() for i in (i0, i1)]
        numeros = []
        for c in celdas[i1 + 1:]:
            c = c.replace('.', '').replace(',', '.')
            try:
                numeros.append(float(c))
            except ValueError:
                break
        if len(numeros) < 7:
            continue
        energia = numeros[:7]
        registros.append({'desde': fechas[0], 'hasta': fechas[1], 'energia': energia})

    if not registros:
        raise SystemExit('las filas no tienen las 7 columnas de energía esperadas (Ener.1 … Ener.7)')

    # ¿2.0TD o 3.0TD? lo dice el uso de los periodos 4 a 6
    usa_p4_p6 = any(sum(r['energia'][3:6]) > 0 for r in registros)
    periodos = PERIODOS_6 if usa_p4_p6 else PERIODOS_3

    registros.sort(key=lambda r: r['desde'], reverse=True)
    ultimo = registros[0]['hasta']
    desde = ultimo.replace(year=ultimo.year - 1)
    ventana = [r for r in registros if r['desde'] >= desde]

    if not ventana:
        ventana = registros
        avisos.append('no hay filas dentro de los últimos doce meses: se usan todas las disponibles')

    totales = [0.0] * len(periodos)
    dias = 0
    for r in ventana:
        for i in range(len(periodos)):
            totales[i] += r['energia'][i]
        dias += (r['hasta'] - r['desde']).days
    kwh_anual = sum(totales)

    if dias < 330:
        avisos.append(f'el SIPS solo cubre {dias} días de los últimos doce meses: el perfil es válido, pero '
                      f'la anualización se apoya en menos de un año. Se declara así en el informe')

    if kwh_anual == 0:
        raise SystemExit('el SIPS no trae consumo en los últimos doce meses: revisa el periodo o el CUPS')

    return {
        'periodos': periodos,
        'kwh_por_periodo': {p: round(t, 1) for p, t in zip(periodos, totales)},
        'kwh_anual': round(kwh_anual, 1),
        'distribucion': {p: round(t / kwh_anual, 4) for p, t in zip(periodos, totales)},
        'dias_cubiertos': dias,
        'ventana': {'desde': min(r['desde'] for r in ventana).isoformat(),
                    'hasta': max(r['hasta'] for r in ventana).isoformat()},
        'filas': len(ventana),
        'avisos': avisos,
        'fuente': Path(ruta).name,
    }


def consumo_de_facturas(carpeta):
    """Suma el consumo por periodos de un conjunto de facturas ya leídas (JSON o PDF)."""
    carpeta = Path(carpeta)
    if not carpeta.exists():
        raise SystemExit(f'no existe la carpeta {carpeta}')
    from factura_a_json import extraer

    kwh = {}
    dias = 0
    leidas, fallidas = [], []
    for f in sorted(list(carpeta.glob('*.json')) + list(carpeta.glob('*.pdf')) + list(carpeta.glob('*.PDF'))):
        try:
            if f.suffix.lower() == '.json':
                d = json.loads(f.read_text(encoding='utf-8'))
                if 'entrada_calculo' in d:
                    d = d['entrada_calculo']
                periodos = list(d.get('kwh', {}))
                for p in periodos:
                    kwh[p] = kwh.get(p, 0) + d['kwh'][p]
                dias += d.get('dias', 0)
            else:
                datos, avisos, errores, _ = extraer(f)
                if not datos or errores:
                    fallidas.append(f.name)
                    continue
                for p, v in datos['kwh'].items():
                    kwh[p] = kwh.get(p, 0) + v
                dias += datos['dias'] or 0
            leidas.append(f.name)
        except Exception as e:                       # noqa: BLE001
            fallidas.append(f'{f.name} ({e})')

    if not leidas:
        raise SystemExit('no se ha podido leer ninguna factura de la carpeta')
    total = sum(kwh.values())
    if total == 0:
        raise SystemExit('las facturas leídas no traen consumo por periodos (puede que sean del mismo mes '
                         'o que la maqueta no se lea todavía)')
    avisos = []
    if dias < 330:
        avisos.append(f'las facturas cubren {dias} días de consumo, no un año: la anualización es parcial')
    if fallidas:
        avisos.append('no se han podido usar: ' + ', '.join(fallidas))
    periodos = sorted(kwh)
    return {
        'periodos': periodos,
        'kwh_por_periodo': {p: round(v, 1) for p, v in kwh.items()},
        'kwh_anual': round(total, 1),
        'distribucion': {p: round(v / total, 4) for p, v in kwh.items()},
        'dias_cubiertos': dias,
        'avisos': avisos,
        'fuente': f'{len(leidas)} facturas de {carpeta.name}',
        'facturas': leidas,
    }


def construir_anual(perfil, factura_json, producto):
    """JSON listo para calc_energia.py: consumo anual real con los precios de la factura."""
    ficha = json.loads(Path(factura_json).read_text(encoding='utf-8'))
    if 'entrada_calculo' in ficha:
        ficha = ficha['entrada_calculo']

    periodos = perfil['periodos']
    kwh = {p: round(perfil['distribucion'].get(p, 0) * perfil['kwh_anual'], 1) for p in periodos}

    # Si la factura no trae precio por periodos (Iberdrola Clientes factura la energía en una
    # sola línea), el cliente paga lo mismo por cada kWh: se repite el precio agregado. El coste
    # anual actual sale exacto y la comparativa con nuestro precio por periodos sigue siendo válida.
    te = list(ficha['actual']['te'])
    nota_agregada = None
    if all(v == 0 for v in te) and ficha.get('energia_agregada'):
        precio = ficha['energia_agregada']['precio']
        te = [precio] * len(periodos)
        nota_agregada = (f'la factura de origen cobra un único precio de energía '
                         f'({precio} €/kWh) para todos los periodos: el coste actual anual se calcula con '
                         f'ese precio y el consumo real del SIPS')
    entrada = {
        'dias': 365,
        'potencias_kw': ficha['potencias_kw'],
        'kwh': kwh,
        'actual': {'tp': ficha['actual']['tp'], 'tp_unidad': ficha['actual']['tp_unidad'],
                   'te': te},
        'extras': dict(ficha.get('extras', {})),
        'iee': ficha.get('iee', 0.0511269632),
        'iva': 0.21,
        'anualizacion': {'metodo': 'real', 'fuente': perfil['fuente'],
                         'dias_cubiertos': perfil['dias_cubiertos'],
                         'kwh_anual': perfil['kwh_anual'],
                         'nota': nota_agregada},
    }
    # los extras de una factura suelta (excesos, autoconsumo, bono) no se extrapolan solos
    for clave in ('excesos', 'reactiva', 'otros', 'otros_sin_iee', 'ajuste_total',
                  'energia_agregada_importe', 'autoconsumo_kwh'):
        if clave in entrada['extras']:
            entrada['extras'][clave] = 0.0
    entrada.pop('total_factura_real', None)

    if producto:
        catalogo = json.loads((RAIZ / 'precios.json').read_text(encoding='utf-8'))
        prod = catalogo['productos'].get(producto)
        if not prod:
            raise SystemExit(f'el producto «{producto}» no está en precios.json')
        tp, te = list(prod['tp']), list(prod['te'])
        if len(tp) == 3 and len(entrada['potencias_kw']) == 2:
            tp = tp[:2]
        if len(te) == 1:
            te = te * len(periodos)
        entrada['nuevo'] = {'tp': tp, 'tp_unidad': 'anio', 'te': te}
        entrada['hoja_precios'] = catalogo.get('fecha_hoja')
    return entrada


def main():
    if len(sys.argv) < 2 or '--help' in sys.argv:
        print(__doc__)
        return 1
    sips = sys.argv[sys.argv.index('--sips') + 1] if '--sips' in sys.argv else None
    facturas = sys.argv[sys.argv.index('--facturas') + 1] if '--facturas' in sys.argv else None
    factura_json = sys.argv[sys.argv.index('--factura') + 1] if '--factura' in sys.argv else None
    producto = sys.argv[sys.argv.index('--producto') + 1] if '--producto' in sys.argv else None
    salida = sys.argv[sys.argv.index('--json') + 1] if '--json' in sys.argv else None

    if not sips and not facturas:
        print('Indica --sips o --facturas. Es lo que decide si la anualización es real o una proyección.')
        print(__doc__)
        return 1

    perfil = parsear_sips(sips) if sips else consumo_de_facturas(facturas)
    print(f'Anualización REAL · fuente: {perfil["fuente"]}')
    print(f'  Periodos {", ".join(perfil["periodos"])} · {perfil["kwh_anual"]:.0f} kWh · '
          f'{perfil["dias_cubiertos"]} días cubiertos')
    print('  Reparto del consumo: ' + ' · '.join(
        f'{p} {perfil["distribucion"][p] * 100:.1f} %' for p in perfil['periodos']))
    for a in perfil['avisos']:
        print(f'  AVISO: {a}')

    if factura_json:
        entrada = construir_anual(perfil, factura_json, producto)
        if salida:
            Path(salida).write_text(json.dumps(entrada, ensure_ascii=False, indent=2), encoding='utf-8')
            print(f'\nJSON anualizado escrito en {salida}')
            print(f'  python skills/informes-ahorro-electrico/scripts/calc_energia.py {salida}')
        else:
            print('\nJSON anualizado:')
            print(json.dumps(entrada, ensure_ascii=False, indent=2))
    else:
        print('\nSin --factura no se genera comparativa. Añade la ficha de una factura con:')
        print('  python tools/anualizar.py --sips {} --factura ficha.json --producto "3.0TD Empresa Flex"'
              .format(Path(sips).name if sips else 'sips.pdf'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
