"""Utilidades compartidas por los perfiles de factura.

La regla que resuelve casi todos los errores de lectura: un importe se toma de la línea
siguiente a su etiqueta, **saltando las líneas que son un precio unitario** («31 días x
0,024688 €/día», «1728,000x0,141890€/kWh»). Si no se salta eso, se lee 0,02 € donde la
factura dice 0,77 €.
"""
import re

NUM = r'(-?\d{1,3}(?:\.\d{3})*,\d+|-?\d+,\d+)'
RE_IMPORTE = re.compile(NUM + r'\s*€')
RE_UNITARIO = re.compile(r'€\s*/|/\s*kW|/\s*kWh|x\s*\d')


def a_float(txt):
    return float(str(txt).replace('.', '').replace(',', '.'))


def importe_tras(texto, etiqueta, max_lineas=4):
    """Primer importe real que aparece tras la etiqueta, ignorando precios unitarios."""
    m = re.search(etiqueta, texto)
    if not m:
        return None
    resto = texto[m.end():]
    for linea in resto.splitlines()[:max_lineas + 1]:
        limpia = linea.strip()
        if not limpia or RE_UNITARIO.search(limpia):
            continue
        e = RE_IMPORTE.search(limpia)
        if e:
            return a_float(e.group(1))
    return None


def bloque_etiqueta(texto, etiqueta, siguientes=40):
    """Texto que va desde la etiqueta hasta `siguientes` líneas después."""
    m = re.search(etiqueta, texto)
    if not m:
        return ''
    return '\n'.join(texto[m.start():].splitlines()[:siguientes])
