#!/usr/bin/env python3
"""Calculadora de factura eléctrica y comparativa · B&M Asesores Energéticos.

Determinista y sin dependencias externas. Reproduce una factura al céntimo,
compara con otro juego de precios y SE NIEGA a dar cifras cuando los datos son
incoherentes o cuando el total no cuadra con la factura real.

Uso:
    python calc_energia.py ejemplo.json
    python calc_energia.py ejemplo.json --verbose

Códigos de salida:
    0  cálculo correcto (y, si se declaró total real, cuadra)
    1  error de uso
    2  datos inválidos: no se calcula nada
    3  descuadre con el total real de la factura: no se entrega nada

Estructuras admitidas: 6 periodos (3.0TD, 6.1TD) y 3 periodos (2.0TD).
El número de periodos se deduce de la longitud de la lista de potencias.

Formato del JSON de entrada:
{
  "dias": 31,
  "potencias_kw": [41.5, 41.5, 41.5, 41.5, 41.5, 41.5],
  "kwh": {"P1":0,"P2":0,"P3":0,"P4":1154,"P5":747,"P6":227},
  "actual":  {"tp":[...], "tp_unidad":"dia", "te":[...]},
  "nuevo":   {"tp":[...], "tp_unidad":"anio", "te":[...]},
  "extras": {"excesos":9.89, "bono_social":0.77, "bono_social_en_base_iee":false,
             "alquiler":11.01, "autoconsumo_kwh":1217,
             "autoconsumo_precio_actual":0.10, "autoconsumo_precio_nuevo":0.0},
  "iee": 0.0511269632,
  "iva": 0.21,
  "total_factura_real": 836.27        <-- opcional pero muy recomendable
}

`total_factura_real` es el total impreso en la factura del cliente. Si se
declara y no coincide al céntimo, el programa termina con código 3.
"""
import json
import sys
from decimal import Decimal as D, ROUND_HALF_UP, InvalidOperation

Q = lambda x: float(D(str(x)).quantize(D('0.01'), rounding=ROUND_HALF_UP))
PERIODOS_6 = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6']
PERIODOS_3 = ['P1', 'P2', 'P3']
TOLERANCIA_CUADRE = 0.01   # por defecto, al céntimo
VERBOSE = '--verbose' in sys.argv


# ----------------------------------------------------------------- validación
def validar(d):
    """Devuelve (lista de errores, lista de avisos). Un solo error bloquea el cálculo."""
    errores, avisos = [], []

    # 'nuevo' es opcional: sin él solo se reproduce la factura, sin comparativa
    for clave in ('dias', 'potencias_kw', 'kwh', 'actual'):
        if clave not in d:
            errores.append(f'falta el campo obligatorio "{clave}"')
    if errores:
        return errores, avisos

    dias = d['dias']
    if not isinstance(dias, (int, float)) or not (1 <= dias <= 366):
        errores.append(f'"dias" debe estar entre 1 y 366, y vale {dias!r}')

    potencias = d['potencias_kw']
    if len(potencias) not in (2, 3, 6):
        errores.append(f'potencias_kw debe tener 2 (2.0TD real: punta y valle), 3 o 6 valores, '
                       f'tiene {len(potencias)}')
        return errores, avisos
    n = len(potencias)
    # En 2.0TD el término de potencia tiene 2 periodos (P1 punta, P2 valle) y el de energía 3.
    # Se admiten por tanto listas de distinto tamaño: N para potencia, M para energía.
    periodos_pot = (PERIODOS_3 if n == 3 else PERIODOS_6)[:n] if n != 3 else PERIODOS_3
    if n == 2:
        periodos_pot = ['P1', 'P2']
    te_actual = d['actual'].get('te', [])
    m = len(te_actual) if len(te_actual) in (3, 6) else n
    if m not in (3, 6):
        errores.append(f'"actual".te debe tener 3 (2.0TD) o 6 (3.0TD/6.1TD) valores, tiene {len(te_actual)}')
        return errores, avisos
    periodos = PERIODOS_3 if m == 3 else PERIODOS_6

    if any((not isinstance(p, (int, float))) or p <= 0 for p in potencias):
        errores.append(f'potencias_kw debe contener números positivos: {potencias}')

    if n == 6 and any(potencias[i] > potencias[i + 1] for i in range(5)):
        avisos.append(f'potencias decrecientes en 3.0TD {potencias}: en la tarifa de acceso deben ser '
                      f'no decrecientes (P1<=P2<=...<=P6). ¿Están traspuestas?')
    if n == 6 and all(p <= 15 for p in potencias):
        avisos.append('en 3.0TD al menos una potencia debe superar 15 kW; revisa la tarifa de acceso')

    kwh = d['kwh']
    claves_ok = {*periodos}
    desconocidas = [k for k in kwh if k not in claves_ok]
    if desconocidas:
        errores.append(f'kwh tiene periodos que no existen en una estructura de {n}: {desconocidas}')
    if any(v < 0 for v in kwh.values()):
        errores.append(f'kwh no puede ser negativo: {kwh}')
    if sum(kwh.values()) == 0:
        avisos.append('el consumo declarado es 0 kWh: la comparativa de energía saldrá a cero')

    for etiqueta in ('actual', 'nuevo'):
        if etiqueta not in d:
            continue
        p = d[etiqueta]
        if 'tp' not in p or 'te' not in p:
            errores.append(f'"{etiqueta}" necesita "tp" y "te"')
            continue
        if len(p['tp']) != n:
            errores.append(f'"{etiqueta}".tp tiene {len(p["tp"])} valores y hay {n} periodos de potencia '
                           f'({"punta y valle" if n == 2 else "P1 a P" + str(n)})')
        if len(p['te']) != m:
            errores.append(f'"{etiqueta}".te tiene {len(p["te"])} valores y hay {m} periodos de energía')
        unidad = str(p.get('tp_unidad', '')).lower()
        if unidad not in ('anio', 'año', 'dia', 'día', 'mes'):
            errores.append(f'"{etiqueta}".tp_unidad debe ser "anio" (catálogo, €/kW·año), "dia" '
                           f'(factura, €/kW·día) o "mes" (€/kW·mes). Vale {p.get("tp_unidad")!r}')
        elif len(p['tp']) == n and len(p['te']) == m:
            # el error clásico: consumo en un periodo cuyo precio de energía es 0
            for per, k in zip(periodos, [kwh.get(x, 0) for x in periodos]):
                i = periodos.index(per)
                if k > 0 and p['te'][i] == 0:
                    errores.append(f'"{etiqueta}": hay {k} kWh en {per} pero el precio de energía es 0. '
                                   f'Faltan periodos o están desordenados: la cifra saldría falsa por defecto')

    iee = d.get('iee', 0.0511269632)
    iva = d.get('iva', 0.21)
    if not (0 <= iee < 0.30):
        errores.append(f'"iee" fuera de rango razonable (0-30 %): {iee}')
    if not (0 <= iva < 0.60):
        errores.append(f'"iva" fuera de rango razonable (0-60 %): {iva}')

    extras = d.get('extras', {})
    if extras.get('autoconsumo_kwh', 0) and not extras.get('autoconsumo_precio_actual', 0):
        avisos.append('hay kWh autoconsumidos pero el precio del excedente actual es 0: '
                      'la factura actual no los está valorando')
    if 'total_factura_real' not in d:
        avisos.append('no se ha declarado "total_factura_real": el cálculo no se puede cuadrar '
                      'contra la factura del cliente. Es la comprobación más importante.')

    return errores, avisos


# ---------------------------------------------------------------------- cálculo
def coste_potencia(potencias, tp, dias, unidad='anio'):
    """unidad: 'anio' = €/kW·año (catálogo) · 'dia' = €/kW·día · 'mes' = €/kW·mes (30 días)."""
    u = str(unidad).lower()
    if u.startswith('dia'):
        return Q(sum(p * t * dias for p, t in zip(potencias, tp)))
    if u.startswith('mes'):
        return Q(sum(p * t * dias / 30 for p, t in zip(potencias, tp)))
    return Q(sum(p * t * dias / 365 for p, t in zip(potencias, tp)))


def coste_energia(kwh, te, periodos):
    return Q(sum(kwh.get(p, 0) * t for p, t in zip(periodos, te)))


def factura(pot, ene, extras, iee_tipo, iva_tipo, autoconsumo=0.0):
    """Aplica IEE e IVA en el orden correcto y devuelve el desglose completo.

    extras admite además 'reactiva' y 'otros' (ajustes REE, servicios, soporte): son
    conceptos que NO generan ahorro por cambio de tarifa, pero forman parte de la factura
    y deben estar para que el total cuadre.
    """
    no_comparable = extras.get('reactiva', 0) + extras.get('otros', 0)
    otros_sin_iee = extras.get('otros_sin_iee', 0)          # p. ej. soporte de gestión: IVA sí, IEE no
    agregada = extras.get('energia_agregada_importe', 0)    # energía sin reparto por periodos
    ajuste_total = extras.get('ajuste_total', 0)            # p. ej. devolución de fianza: resta al total,
                                                            # DESPUÉS de impuestos (la factura lo indica así)
    bono = extras.get('bono_social', 0)
    bono_en_base = extras.get('bono_social_en_base_iee', True)
    base_iee = Q(pot + ene + agregada + extras.get('excesos', 0) + no_comparable
                 + (bono if bono_en_base else 0) - autoconsumo)
    iee = Q(base_iee * iee_tipo)
    base_iva = Q(base_iee + iee + otros_sin_iee + extras.get('alquiler', 0)
                 + (0 if bono_en_base else bono))
    iva = Q(base_iva * iva_tipo)
    return {
        'potencia': Q(pot), 'energia': Q(ene), 'autoconsumo': Q(-autoconsumo),
        'extras': Q(extras.get('excesos', 0) + bono + no_comparable),
        'reactiva': Q(extras.get('reactiva', 0)), 'otros': Q(extras.get('otros', 0)),
        'otros_sin_iee': Q(otros_sin_iee), 'energia_agregada': Q(agregada),
        'ajuste_total': Q(ajuste_total),
        'base_iee': base_iee, 'iee': iee, 'alquiler': extras.get('alquiler', 0),
        'base_iva': base_iva, 'iva': iva, 'total': Q(base_iva + iva + ajuste_total),
    }


def calcular(d):
    dias = d['dias']
    potencias = d['potencias_kw']
    kwh = d['kwh']
    extras = d.get('extras', {})
    iee_tipo = d.get('iee', 0.0511269632)
    iva_tipo = d.get('iva', 0.21)
    periodos = PERIODOS_3 if len(d['actual'].get('te', [])) == 3 else PERIODOS_6

    out = {}
    for etiqueta in ('actual', 'nuevo'):
        if etiqueta not in d:
            continue
        precios = d[etiqueta]
        pot = coste_potencia(potencias, precios['tp'], dias, precios.get('tp_unidad', 'anio'))
        ene = coste_energia(kwh, precios['te'], periodos)
        autok = extras.get('autoconsumo_kwh', 0)
        autop = extras.get(f'autoconsumo_precio_{etiqueta}', 0)
        out[etiqueta] = factura(pot, ene, extras, iee_tipo, iva_tipo, Q(autok * autop))
        out[etiqueta]['autoconsumo_kwh'] = autok
        out[etiqueta]['autoconsumo_precio'] = autop
        out[etiqueta]['kwh_total'] = sum(kwh.values())
        out[etiqueta]['periodos'] = periodos
        out[etiqueta]['periodos_potencia'] = len(potencias)

    if 'nuevo' in out:
        ahorro = Q(out['actual']['total'] - out['nuevo']['total'])
        pct = round(ahorro / out['actual']['total'] * 100, 1) if out['actual']['total'] else 0.0
        sin_imp = Q((out['actual']['potencia'] + out['actual']['energia'])
                    - (out['nuevo']['potencia'] + out['nuevo']['energia']))
    else:
        ahorro, pct, sin_imp = None, None, None
    resultado = {
        'actual': out['actual'],
        'nuevo': out.get('nuevo'),
        'ahorro_eur': ahorro,
        'ahorro_pct': pct,
        'ahorro_sin_impuestos': sin_imp,
        'comparativa': 'nuevo' in out,
    }

    # comprobación aritmética interna: la suma de las partes tiene que dar el total
    for etiqueta in out:
        f = out[etiqueta]
        recalculado = Q(f['base_iva'] + f['iva'] + f.get('ajuste_total', 0))
        if abs(recalculado - f['total']) > TOLERANCIA_CUADRE:
            raise ArithmeticError(f'inconsistencia interna en {etiqueta}: {recalculado} != {f["total"]}')

    # cuadre contra el total real de la factura
    real = d.get('total_factura_real')
    if real is None:
        resultado['cuadre'] = {'declarado': False}
    else:
        diferencia = Q(out['actual']['total'] - real)
        tolerancia = float(d.get('tolerancia_cuadre', TOLERANCIA_CUADRE))
        resultado['cuadre'] = {
            'declarado': True,
            'total_real': Q(real),
            'total_calculado': out['actual']['total'],
            'diferencia': diferencia,
            'tolerancia': tolerancia,
            'cuadra': abs(diferencia) <= tolerancia + 1e-9,
            'al_centimo': abs(diferencia) <= TOLERANCIA_CUADRE + 1e-9,
        }
    return resultado


def main(ruta):
    try:
        with open(ruta, encoding='utf-8') as f:
            d = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f'ERROR no se pudo leer el JSON: {e}', file=sys.stderr)
        return 1

    errores, avisos = validar(d)
    if VERBOSE:
        for a in avisos:
            print(f'AVISO: {a}', file=sys.stderr)
    if errores:
        print('DATOS INVÁLIDOS: no se calcula nada.', file=sys.stderr)
        for e in errores:
            print(f'  - {e}', file=sys.stderr)
        return 2
    for a in avisos:
        print(f'AVISO: {a}', file=sys.stderr)

    resultado = calcular(d)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))

    c = resultado['cuadre']
    if c.get('declarado') and not c['cuadra']:
        print(f'\nDESCUADRE: la factura real es {c["total_real"]} € y el cálculo da '
              f'{c["total_calculado"]} € (diferencia {c["diferencia"]} €).\n'
              f'NO se entrega ninguna cifra hasta localizar la diferencia: revisa bono social dentro/fuera '
              f'de la base del IEE, alquiler de contador, regularizaciones, excesos, reactiva y redondeos.',
              file=sys.stderr)
        return 3
    if c.get('declarado') and c.get('al_centimo'):
        print(f'\nCUADRE OK: {c["total_real"]} € reproducidos al céntimo.', file=sys.stderr)
    elif c.get('declarado'):
        print(f'\nCUADRE CON TOLERANCIA: {c["total_real"]} € frente a {c["total_calculado"]} € '
              f'(diferencia {c["diferencia"]} €, dentro de la tolerancia de {c["tolerancia"]} € declarada '
              f'para esta comercializadora por redondeo línea a línea).\n'
              f'Esta diferencia se declara por escrito en el informe: no se oculta.', file=sys.stderr)
    return 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
