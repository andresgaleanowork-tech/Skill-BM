#!/usr/bin/env python3
"""Rellena una plantilla HTML de B&M con los logos ya incrustados y los datos del documento.

Por qué existe: las plantillas llevan marcadores `{{LOGO_BM}}` y `{{LOGO_IB}}`. Si se abren tal
cual, los logos no aparecen, y si se pegan a mano se acaba con un logo distinto en cada documento.
Esto los incrusta en base64 desde `assets/logos/`, así el HTML resultante es **un solo archivo**
que se puede enviar por correo o convertir a PDF sin dependencias externas.

Reglas de marca que aplica:
  · **Actas: solo el logo de B&M.** El de Iberdrola se retira y no se deja hueco.
  · En el resto de documentos: B&M a la izquierda, Iberdrola a la derecha.
  · Si se pide «sin Iberdrola», se quita limpiamente.

Uso:
    python tools/rellenar_plantilla.py --tipo informe --datos datos.json --salida /tmp/informe.html
    python tools/rellenar_plantilla.py --tipo acta --datos datos.json --solo-bm --salida /tmp/acta.html
    python tools/rellenar_plantilla.py --tipo presupuesto --listar-campos

El JSON de datos es un diccionario de marcador → valor: {"TITULAR": "RAFAEL TENA SL", "FECHA": "17/11/2026"}.
Los marcadores de logo no se pasan: los pone el programa.
"""
import base64
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
S = RAIZ / 'skills'
LOGOS = S / 'maquetacion-documentos-bm' / 'assets' / 'logos'
LOGOS_ACTA = S / 'actas-entrega-bm' / 'assets' / 'logos'

PLANTILLAS = {
    'informe': S / 'maquetacion-documentos-bm' / 'assets' / 'informe_base.html',
    'presupuesto': S / 'presupuestos-bm' / 'assets' / 'presupuesto_base.html',
    'acta': S / 'actas-entrega-bm' / 'assets' / 'acta_base.html',
}

# el acta solo lleva B&M, por regla de marca
SOLO_BM_POR_TIPO = {'acta'}


def buscar_logo(nombres, carpetas):
    for carpeta in carpetas:
        for nombre in nombres:
            ruta = carpeta / nombre
            if ruta.exists():
                return ruta
    return None


def data_uri(ruta):
    mime = 'image/png' if ruta.suffix.lower() == '.png' else 'image/jpeg'
    return f'data:{mime};base64,' + base64.b64encode(ruta.read_bytes()).decode('ascii')


def marcadores(html):
    return sorted(set(re.findall(r'\{\{([A-Z0-9_]+)\}\}', html)))


def main():
    if len(sys.argv) < 2 or '--help' in sys.argv:
        print(__doc__)
        return 1

    tipo = sys.argv[sys.argv.index('--tipo') + 1] if '--tipo' in sys.argv else 'informe'
    if tipo not in PLANTILLAS:
        print(f'Tipo desconocido: {tipo}. Válidos: {", ".join(PLANTILLAS)}')
        return 1
    plantilla = PLANTILLAS[tipo]
    if not plantilla.exists():
        print(f'No existe la plantilla: {plantilla}')
        return 1
    html = plantilla.read_text(encoding='utf-8')

    if '--listar-campos' in sys.argv:
        print(f'Marcadores de la plantilla «{tipo}» ({plantilla.name}):')
        for m in marcadores(html):
            print(f'  {{{{{m}}}}}')
        print('\nLos LOGO_* los rellena este programa. El resto van en el JSON de --datos.')
        return 0

    datos = {}
    if '--datos' in sys.argv:
        ruta_datos = Path(sys.argv[sys.argv.index('--datos') + 1])
        datos = json.loads(ruta_datos.read_text(encoding='utf-8'))

    solo_bm = '--solo-bm' in sys.argv or tipo in SOLO_BM_POR_TIPO

    # ── logos
    bm = buscar_logo(['bm.png', 'bm.jpg', 'bm_full.jpg'], [LOGOS, LOGOS_ACTA])
    ib = buscar_logo(['iberdrola.jpg', 'iberdrola.png'], [LOGOS])
    if bm is None:
        print('ERROR: no se encuentra el logo de B&M en assets/logos/. Sin logo no se genera el documento.')
        return 1
    html = html.replace('{{LOGO_BM}}', data_uri(bm))

    if '{{LOGO_IB}}' in html:
        if solo_bm:
            # se retira la etiqueta <img> entera y el hueco: en actas no va Iberdrola
            html = re.sub(r'<img[^>]*\{\{LOGO_IB\}\}[^>]*>', '', html)
            print('Logo de Iberdrola retirado (regla de marca: solo B&M).')
        elif ib is None:
            html = re.sub(r'<img[^>]*\{\{LOGO_IB\}\}[^>]*>', '', html)
            print('AVISO: no hay logo de Iberdrola en assets/logos/. Se genera sin él.')
        else:
            html = html.replace('{{LOGO_IB}}', data_uri(ib))

    # ── datos del documento
    pendientes = []
    for m in marcadores(html):
        if m in datos:
            html = html.replace('{{' + m + '}}', str(datos[m]))
        else:
            pendientes.append(m)

    salida = sys.argv[sys.argv.index('--salida') + 1] if '--salida' in sys.argv else None
    if salida:
        Path(salida).write_text(html, encoding='utf-8')
        print(f'Escrito: {salida}')
        print(f'  plantilla: {plantilla.name} · tipo: {tipo} · logo Iberdrola: '
              f'{"no (solo B&M)" if solo_bm else "sí"}')
    else:
        print(html)

    if pendientes:
        print('\nMarcadores SIN rellenar (hay que darlos en el JSON de --datos):')
        for m in pendientes:
            print(f'  {{{{{m}}}}}')
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
