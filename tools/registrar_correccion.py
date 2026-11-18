#!/usr/bin/env python3
"""Añade una línea a la bitácora de correcciones. Uso rápido desde la conversación:

python tools/registrar_correccion.py "Informe ACME" "El IEE se calculó sobre la base equivocada" "Nueva regla en 02_formulas"
"""
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BITACORA = RAIZ / 'metricas' / 'bitacora.md'


def registrar(documento, que_paso, cambio):
    texto = BITACORA.read_text(encoding='utf-8')
    fila = f'| {date.today().isoformat()} | {documento} | {que_paso} | {cambio} |\n'
    marcador = '\n## Cómo se usa'
    if marcador in texto:
        texto = texto.replace(marcador, fila + marcador, 1)
    else:
        texto += fila
    BITACORA.write_text(texto, encoding='utf-8')
    print('registrado:', fila.strip())


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    registrar(*sys.argv[1:])
