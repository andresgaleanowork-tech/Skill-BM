#!/usr/bin/env python3
"""Estado de la carga de precios: fecha, antigüedad y aviso.

Los precios se cargan a mano una vez y se vuelven a cargar cuando cambian
(cadencia semanal o mensual). Este script dice si la carga sigue siendo razonable.

Uso: python tools/estado_precios.py [--silencioso]
"""
import json
import sys
from datetime import date, datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
JSON = RAIZ / 'precios.json'

DIAS_REVISAR = 7    # a partir de aquí, merece la pena mirar si ha salido hoja nueva
DIAS_PEDIR = 30     # a partir de aquí, no se emite informe sin confirmar vigencia


def main(silencioso=False):
    if not JSON.exists():
        print('NO HAY PRECIOS CARGADOS. Pide la ficha de precios antes de calcular nada.')
        return 1
    d = json.loads(JSON.read_text(encoding='utf-8'))
    fecha_hoja = d.get('fecha_hoja', 'sin fecha')
    cargado = d.get('cargado')
    dias = None
    if cargado:
        dias = (date.today() - datetime.fromisoformat(cargado).date()).days
    if dias is None:
        estado, aviso = 'DESCONOCIDO', 'La carga no tiene fecha: pide la fecha de la hoja y vuelve a cargarla.'
    elif dias < DIAS_REVISAR:
        estado, aviso = 'AL DÍA', f'Cargada hace {dias} día(s). Sin acción.'
    elif dias < DIAS_PEDIR:
        estado, aviso = 'REVISAR', (f'Cargada hace {dias} días. La hoja se actualiza semanal o mensualmente: '
                                    'conviene confirmar con el usuario si hay una nueva antes de un informe importante.')
    else:
        estado, aviso = 'PEDIR ACTUALIZACIÓN', (f'Cargada hace {dias} días. No emitir un informe nuevo sin confirmar '
                                                'que estos precios siguen vigentes; la hoja cambia cada semana o mes.')
    if not silencioso:
        print(f'Hoja del {fecha_hoja} · cargada el {cargado} · {len(d.get("productos", {}))} productos')
        for nombre in d.get('productos', {}):
            print(f'  · {nombre}')
        print(f'\nEstado: {estado}\n  {aviso}')
        print('\nRecuerda: en cada informe y presupuesto debe figurar la fecha de la hoja usada.')
    return {'estado': estado, 'dias': dias, 'fecha_hoja': fecha_hoja, 'aviso': aviso}


if __name__ == '__main__':
    r = main('--silencioso' in sys.argv)
    sys.exit(0 if r != 1 else 1)
