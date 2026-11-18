#!/usr/bin/env python3
"""Convierte un documento recibido (factura del cliente, presupuesto ajeno) a estilo B&M.

No reescribe el contenido: extrae los datos y avisa de lo que falta. La redacción
final la hace el asistente con las skills; esto deja el terreno preparado.

Uso:
    python tools/normalizar_documento.py bandeja/presupuestos/oferta_competencia.pdf
    python tools/normalizar_documento.py bandeja/facturas/factura.pdf --json
"""
import json
import re
import sys
from pathlib import Path

try:
    import pymupdf
except ImportError:
    pymupdf = None

PATRONES = {
    'cif': r'\b([A-HJNP-SUVW]\d{7}[0-9A-J])\b',
    'nif': r'\b(\d{8}[A-Z])\b',
    'nie': r'\b([XYZ]\d{7}[A-Z])\b',
    'cups': r'\b(ES\d{16}[A-Z0-9]{4})\b',
    'importe': r'\b(\d{1,3}(?:\.\d{3})*,\d{2})\s*€',
    'fecha': r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b',
    'potencia_kw': r'(\d+(?:[.,]\d+)?)\s*kW\b',
    'kwh': r'(\d{1,3}(?:\.\d{3})*,\d+|\d+,\d+)\s*kWh\b',
    'descuento': r'(\d{1,2}(?:[.,]\d+)?)\s*%',
}


def extraer_texto(ruta):
    sufijo = ruta.suffix.lower()
    if sufijo == '.pdf':
        if pymupdf is None:
            raise SystemExit('Falta pymupdf: pip install pymupdf')
        doc = pymupdf.open(ruta)
        texto = '\n'.join(p.get_text() for p in doc)
        paginas = len(doc)
        if len(texto.strip()) < 120:
            return texto, paginas, False  # escaneo: hay que mirarlo a ojo
        return texto, paginas, True
    if sufijo in ('.txt', '.md', '.csv'):
        return ruta.read_text(encoding='utf-8', errors='ignore'), 1, True
    raise SystemExit(f'Formato no soportado para lectura directa: {sufijo}. Exporta a PDF o TXT, o pide el original.')


def main(ruta, como_json=False):
    ruta = Path(ruta)
    texto, paginas, legible = extraer_texto(ruta)
    datos = {'archivo': ruta.name, 'paginas': paginas, 'texto_legible': legible}
    for nombre, patron in PATRONES.items():
        encontrados = re.findall(patron, texto)
        vistos = []
        for e in encontrados:
            if e not in vistos:
                vistos.append(e)
        datos[nombre] = vistos[:12]
    if como_json:
        print(json.dumps(datos, ensure_ascii=False, indent=2))
        return datos
    print(f"{ruta.name} · {paginas} página(s) · texto {'legible' if legible else 'NO legible (escaneo: hay que revisarlo a la vista)'}")
    etiquetas = {'cif': 'CIF', 'nif': 'NIF', 'nie': 'NIE', 'cups': 'CUPS', 'importe': 'Importes €',
                 'fecha': 'Fechas', 'potencia_kw': 'Potencias kW', 'kwh': 'Consumos kWh', 'descuento': 'Porcentajes'}
    for clave, etiqueta in etiquetas.items():
        if datos[clave]:
            print(f'  {etiqueta:14s} {", ".join(datos[clave][:8])}')
    faltan = [etiquetas[k] for k in ('cif', 'nif', 'nie', 'cups') if not datos[k]]
    if len(faltan) == 4:
        print('  AVISO: no se ha detectado ningún CIF, NIF, NIE ni CUPS: puede ser un documento que no es una factura o un escaneo sin capa de texto.')
    print('\nSiguiente paso: la skill correspondiente decide con estos datos; no se inventa ningún campo vacío.')
    return datos


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1], '--json' in sys.argv)
