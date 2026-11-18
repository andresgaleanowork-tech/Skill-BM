#!/usr/bin/env python3
"""Índice de informes emitidos: qué se mandó, a quién, con qué precios y cuándo.

Para qué sirve, en la práctica:

  · responder «¿qué le mandé a este cliente en marzo?» sin bucear en el correo;
  · saber qué informes hay que rehacer cuando cambia la hoja de precios;
  · no repetir una llamada a quien ya se le envió, y volver a llamar a quien no contestó;
  · tener el histórico si un cliente discute una cifra.

La tabla vive en `metricas/indice_informes.csv`, que se abre con cualquier hoja de cálculo.

Uso:
    python tools/indice_informes.py --listar
    python tools/indice_informes.py --anadir --cliente "RAFAEL TENA SL" --cif B22243935 \
        --cups ES0031300646612001CS0F --tipo informe --hoja 2026-11-16 \
        --coste-actual 9222.91 --coste-nuevo 7225.74 --ahorro 1997.17 --producto "3.0TD Empresa Flex" \
        --modo A --comercial "Andrés Galeano" --archivo Informes/Noviembre_2026/Tena_v2.pdf
    python tools/indice_informes.py --revisar          # informes con hoja anterior a la vigente
    python tools/indice_informes.py --pendientes       # emitidos sin seguimiento anotado
"""
import csv
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
INDICE = RAIZ / 'metricas' / 'indice_informes.csv'
CABECERA = ['fecha_emision', 'cliente', 'cif_nif', 'cups', 'tipo', 'producto', 'modo',
            'hoja_precios', 'coste_actual', 'coste_nuevo', 'ahorro', 'ahorro_pct',
            'comercial', 'archivo', 'estado', 'seguimiento']


def leer():
    if not INDICE.exists():
        return []
    with INDICE.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def escribir(filas):
    INDICE.parent.mkdir(parents=True, exist_ok=True)
    with INDICE.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=CABECERA)
        w.writeheader()
        for fila in filas:
            w.writerow({k: fila.get(k, '') for k in CABECERA})


def arg(nombre, defecto=''):
    return sys.argv[sys.argv.index(nombre) + 1] if nombre in sys.argv else defecto


def main():
    if '--help' in sys.argv or len(sys.argv) == 1:
        print(__doc__)
        return 1

    filas = leer()

    if '--listar' in sys.argv:
        if not filas:
            print('El índice está vacío. Se llena con --anadir al entregar cada informe.')
            return 0
        print(f'{len(filas)} documento(s) emitido(s)\n')
        print(f'{"fecha":12s} {"cliente":28s} {"tipo":10s} {"modo":4s} {"hoja":11s} {"ahorro":>10s}  estado')
        for f in sorted(filas, key=lambda x: x['fecha_emision'], reverse=True):
            ahorro = f['ahorro']
            ahorro = f'{float(ahorro):,.2f} €'.replace(',', '.') if ahorro else '—'
            print(f'{f["fecha_emision"]:12s} {f["cliente"][:28]:28s} {f["tipo"][:10]:10s} '
                  f'{f["modo"]:4s} {f["hoja_precios"]:11s} {ahorro:>10s}  {f["estado"]}')
        return 0

    if '--revisar' in sys.argv:
        import json
        ruta = RAIZ / 'precios.json'
        if not ruta.exists():
            print('No hay precios.json: no se puede saber qué hoja está vigente.')
            return 1
        vigente = json.loads(ruta.read_text(encoding='utf-8')).get('fecha_hoja')
        antiguos = [f for f in filas if f['hoja_precios'] and f['hoja_precios'] < vigente]
        if not antiguos:
            print(f'Todos los documentos emitidos usan la hoja vigente ({vigente}).')
            return 0
        print(f'Hoja vigente: {vigente}. Documentos con hoja anterior: {len(antiguos)}\n')
        for f in antiguos:
            print(f'  {f["fecha_emision"]} · {f["cliente"]} · hoja {f["hoja_precios"]} · '
                  f'{f["tipo"]} · {f["archivo"] or "sin archivo anotado"}')
        print('\nUn informe antiguo no se «actualiza»: se recalcula entero con la hoja nueva.')
        return 0

    if '--pendientes' in sys.argv:
        pend = [f for f in filas if f['estado'] in ('', 'enviado') and not f['seguimiento']]
        if not pend:
            print('No hay documentos a la espera de seguimiento.')
            return 0
        print(f'{len(pend)} documento(s) sin seguimiento anotado:\n')
        for f in pend:
            print(f'  {f["fecha_emision"]} · {f["cliente"]} · {f["tipo"]} · ahorro {f["ahorro"]} €')
        return 0

    if '--anadir' in sys.argv:
        actual, nuevo = arg('--coste-actual'), arg('--coste-nuevo')
        ahorro = arg('--ahorro')
        pct = ''
        try:
            if not ahorro and actual and nuevo:
                ahorro = f'{float(actual) - float(nuevo):.2f}'
            if ahorro and actual and float(actual):
                pct = f'{float(ahorro) / float(actual) * 100:.1f}'
        except ValueError:
            print('Los importes deben ser números: 9222.91, no «9.222,91»')
            return 1
        fila = {
            'fecha_emision': arg('--fecha', date.today().isoformat()),
            'cliente': arg('--cliente'),
            'cif_nif': arg('--cif'),
            'cups': arg('--cups'),
            'tipo': arg('--tipo', 'informe'),
            'producto': arg('--producto'),
            'modo': arg('--modo'),
            'hoja_precios': arg('--hoja'),
            'coste_actual': actual,
            'coste_nuevo': nuevo,
            'ahorro': ahorro,
            'ahorro_pct': pct,
            'comercial': arg('--comercial'),
            'archivo': arg('--archivo'),
            'estado': arg('--estado', 'enviado'),
            'seguimiento': '',
        }
        if not fila['cliente']:
            print('Falta --cliente: sin cliente el índice no sirve de nada.')
            return 1
        if not fila['hoja_precios']:
            print('AVISO: no se ha indicado --hoja. Sin la fecha de la hoja no se puede saber qué '
                  'informes hay que rehacer cuando cambien los precios.')
        filas.append(fila)
        escribir(filas)
        print(f'Anotado: {fila["cliente"]} · {fila["tipo"]} · hoja {fila["hoja_precios"] or "—"} · '
              f'ahorro {ahorro or "—"} €')
        print(f'Índice: {INDICE.relative_to(RAIZ)} ({len(filas)} documentos)')
        return 0

    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
