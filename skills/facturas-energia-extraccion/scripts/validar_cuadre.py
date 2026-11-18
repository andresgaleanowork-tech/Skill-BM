#!/usr/bin/env python3
"""Validador de cuadre de factura · B&M Asesores Energéticos.

Determinista y sin dependencias. Reproduce una factura al céntimo y compara con
otro juego de precios manteniendo potencias, consumo y periodo.

Uso:
    python calc_energia.py ejemplo.json

Formato del JSON de entrada (ver ejemplo.json):
{
  "dias": 31,
  "potencias_kw": [41.5, 41.5, 41.5, 41.5, 41.5, 41.5],
  "kwh": {"P1":0,"P2":0,"P3":0,"P4":1154,"P5":747,"P6":227},
  "actual":  {"tp":[0.0558,...], "tp_unidad":"dia", "te":[0.30,...]},
  "nuevo":   {"tp":[20.37,...], "tp_unidad":"anio", "te":[0.25,...]},
  "extras": {"excesos":9.89, "bono_social":0.77, "alquiler":11.01,
             "autoconsumo_kwh":1217, "autoconsumo_precio_actual":0.10,
             "autoconsumo_precio_nuevo":0.0},
  "iee": 0.0511269632,
  "iva": 0.21
}
"""
import json
import sys
from decimal import Decimal as D, ROUND_HALF_UP

Q = lambda x: float(D(str(x)).quantize(D('0.01'), rounding=ROUND_HALF_UP))
PERIODOS = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6']


def coste_potencia(potencias, tp, dias, unidad='anio'):
    """unidad: 'anio' si el TP viene en €/kW·año (catálogo) o 'dia' si viene en €/kW·día (factura)."""
    if str(unidad).lower().startswith('dia'):
        return Q(sum(p * t * dias for p, t in zip(potencias, tp)))
    return Q(sum(p * t * dias / 365 for p, t in zip(potencias, tp)))


def coste_energia(kwh, te):
    return Q(sum(kwh.get(p, 0) * t for p, t in zip(PERIODOS, te)))


def factura(pot, ene, extras, iee_tipo, iva_tipo, autoconsumo=0.0):
    """Devuelve el desglose completo aplicando IEE e IVA en el orden correcto."""
    bono = extras.get('bono_social', 0)
    bono_en_base = extras.get('bono_social_en_base_iee', True)
    base_iee = Q(pot + ene + extras.get('excesos', 0) + (bono if bono_en_base else 0) - autoconsumo)
    iee = Q(base_iee * iee_tipo)
    base_iva = Q(base_iee + iee + extras.get('alquiler', 0) + (0 if bono_en_base else bono))
    iva = Q(base_iva * iva_tipo)
    return {
        'potencia': Q(pot), 'energia': Q(ene), 'autoconsumo': Q(-autoconsumo),
        'extras': Q(extras.get('excesos', 0) + extras.get('bono_social', 0)),
        'base_iee': base_iee, 'iee': iee, 'alquiler': extras.get('alquiler', 0),
        'base_iva': base_iva, 'iva': iva, 'total': Q(base_iva + iva),
    }


def main(ruta):
    d = json.load(open(ruta, encoding='utf-8'))
    dias = d['dias']
    potencias = d['potencias_kw']
    kwh = d['kwh']
    extras = d.get('extras', {})
    iee_tipo = d.get('iee', 0.0511269632)
    iva_tipo = d.get('iva', 0.21)

    out = {}
    for etiqueta in ('actual', 'nuevo'):
        precios = d[etiqueta]
        pot = coste_potencia(potencias, precios['tp'], dias, precios.get('tp_unidad', 'anio'))
        ene = coste_energia(kwh, precios['te'])
        autok = extras.get('autoconsumo_kwh', 0)
        autop = extras.get(f'autoconsumo_precio_{etiqueta}', 0)
        auto = Q(autok * autop)
        out[etiqueta] = factura(pot, ene, extras, iee_tipo, iva_tipo, auto)
        out[etiqueta]['autoconsumo_kwh'] = autok
        out[etiqueta]['autoconsumo_precio'] = autop

    ahorro = Q(out['actual']['total'] - out['nuevo']['total'])
    pct = round(ahorro / out['actual']['total'] * 100, 1) if out['actual']['total'] else 0.0
    resultado = {
        'actual': out['actual'],
        'nuevo': out['nuevo'],
        'ahorro_eur': ahorro,
        'ahorro_pct': pct,
        'ahorro_sin_impuestos': Q((out['actual']['potencia'] + out['actual']['energia'])
                                   - (out['nuevo']['potencia'] + out['nuevo']['energia'])),
    }
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return resultado


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
