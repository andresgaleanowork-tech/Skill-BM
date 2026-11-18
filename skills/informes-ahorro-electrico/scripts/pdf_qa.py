#!/usr/bin/env python3
"""QA de PDF de B&M: tamaño, páginas, pies y texto mínimo por página.

Uso: python pdf_qa.py informe.pdf [marca_en_el_pie]
Requiere: pip install pymupdf
"""
import sys
import pymupdf

MIN_CHARS = 120  # una página con menos texto suele ser un salto de página vacío
PIE = '671 681 039'


def qa(ruta, marca=PIE):
    doc = pymupdf.open(ruta)
    problemas = []
    for i, page in enumerate(doc, 1):
        ancho, alto = page.rect.width, page.rect.height
        if round(ancho) != 595 or round(alto) != 842:
            problemas.append(f'pág {i}: tamaño {ancho:.0f}x{alto:.0f} (se espera A4 595x842)')
        texto = page.get_text()
        if len(texto.strip()) < MIN_CHARS:
            problemas.append(f'pág {i}: solo {len(texto.strip())} caracteres, posible página vacía')
        if marca and marca not in texto:
            problemas.append(f'pág {i}: no aparece el pie con {marca}')
    print(f'{ruta}: {len(doc)} páginas, {doc[0].rect.width:.0f}x{doc[0].rect.height:.0f} mm-units')
    if problemas:
        print('REVISAR:')
        for p in problemas:
            print('  -', p)
        return False
    print('OK: todas las páginas con tamaño correcto, texto y pie')
    return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    sys.exit(0 if qa(*sys.argv[1:]) else 1)
