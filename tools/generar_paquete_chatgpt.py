#!/usr/bin/env python3
"""Genera el paquete de conocimiento para ChatGPT a partir de las skills.

Una sola fuente de verdad: se edita `skills/` y este script reconstruye
`chatgpt/conocimiento/`. Evita la deriva entre la versión de Claude/Codex y la de ChatGPT.

Uso:
    python tools/generar_paquete_chatgpt.py                        # escribe en chatgpt/conocimiento
    python tools/generar_paquete_chatgpt.py --destino /tmp/salida   # escribe en otra carpeta
"""
import shutil
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
S = RAIZ / 'skills'
OUT = RAIZ / 'chatgpt' / 'conocimiento'
if '--destino' in sys.argv:
    OUT = Path(sys.argv[sys.argv.index('--destino') + 1])

# (archivo de salida, título, piezas de origen)
MAPA = [
    ('01_proceso_informes.md', 'Proceso de informes de ahorro · B&M', [
        'informes-ahorro-electrico/SKILL.md',
        'informes-ahorro-electrico/references/escenarios_de_datos.md',
        'informes-ahorro-electrico/references/plantilla_recepcion.md',
        'informes-ahorro-electrico/references/checklist_final.md']),
    ('02_formulas.md', 'Fórmulas de cálculo eléctrico · B&M', [
        'informes-ahorro-electrico/references/formulas.md']),
    ('03_reglas_comerciales.md', 'Reglas comerciales · B&M', [
        'informes-ahorro-electrico/references/reglas_comerciales.md']),
    ('04_errores_conocidos.md', 'Errores conocidos y corrección · B&M', [
        'informes-ahorro-electrico/references/errores_conocidos.md',
        'metricas/bitacora.md']),
    ('05_maquetacion.md', 'Maquetación de documentos · B&M', [
        'maquetacion-documentos-bm/SKILL.md',
        'maquetacion-documentos-bm/references/estilos.md']),
    ('06_facturas_extraccion.md', 'Extracción y cuadre de facturas, y lectura de SIPS', [
        'facturas-energia-extraccion/SKILL.md',
        'facturas-energia-extraccion/references/orden_impuestos.md',
        'facturas-energia-extraccion/references/esquema_json.md',
        'facturas-energia-extraccion/references/sips.md']),
    ('07_precios_iberdrola.md', 'Precios de Iberdrola · localización y vigencia', [
        'precios-iberdrola/SKILL.md',
        'precios-iberdrola/references/mapa_de_la_hoja.md',
        'precios-iberdrola/references/productos.md']),
    ('08_presupuestos.md', 'Presupuestos · B&M', [
        'presupuestos-bm/SKILL.md',
        'presupuestos-bm/references/estructura.md']),
    ('09_servicios.md', 'Servicios de B&M: boletines, expedientes y legalizaciones', [
        'servicios-bm/SKILL.md',
        'servicios-bm/references/servicios.md',
        'servicios-bm/references/textos_comerciales.md']),
    ('10_actas_entrega.md', 'Actas de entrega y devolución · B&M', [
        'actas-entrega-bm/SKILL.md',
        'actas-entrega-bm/references/acta_entrega.md']),
]

# Los logos viajan al paquete de ChatGPT: las plantillas los necesitan y en el Proyecto no hay
# forma de pegar una imagen dentro de un marcador.
COPIAS = [
    ('actas-entrega-bm/assets/acta_base.html', 'acta_base.html'),
    ('maquetacion-documentos-bm/assets/logos/bm.png', 'logo_bm.png'),
    ('maquetacion-documentos-bm/assets/logos/iberdrola.jpg', 'logo_iberdrola.jpg'),
    ('maquetacion-documentos-bm/assets/informe_base.html', 'informe_base.html'),
    ('presupuestos-bm/assets/presupuesto_base.html', 'presupuesto_base.html'),
    ('informes-ahorro-electrico/scripts/calc_energia.py', 'calc_energia.py'),
    ('informes-ahorro-electrico/scripts/pdf_qa.py', 'pdf_qa.py'),
    ('LICENSE.md', 'LICENSE.md'),
]


def leer(ruta_rel):
    # primero dentro de skills/, luego en la raíz del paquete (bitácora, licencia…)
    for base in (S, RAIZ):
        candidato = base / ruta_rel
        if candidato.exists():
            return candidato.read_text(encoding='utf-8').strip()
    raise FileNotFoundError(f'no se encuentra la pieza: {ruta_rel}')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for viejo in OUT.glob('*'):
        if viejo.is_file():
            viejo.unlink()
    total = 0
    for destino, titulo, piezas in MAPA:
        trozos = [f'# {titulo}\n']
        for p in piezas:
            trozos.append(leer(p) + '\n')
        texto = '\n\n---\n\n'.join(trozos)
        (OUT / destino).write_text(texto, encoding='utf-8')
        total += len(texto)
        print(f'{destino:28s} {len(texto):6d} caracteres')
    for origen, destino in COPIAS:
        fuente = S / origen if (S / origen).exists() else RAIZ / origen.lstrip('./')
        shutil.copy(fuente, OUT / destino)
    zips = RAIZ / 'zips'
    zips.mkdir(exist_ok=True)
    with zipfile.ZipFile(zips / 'paquete_chatgpt_bm.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        for f in sorted((RAIZ / 'chatgpt').rglob('*')):
            if f.is_file():
                z.write(f, f.relative_to(RAIZ / 'chatgpt'))
    print(f'\nTotal conocimiento: {total} caracteres en {len(MAPA)} archivos')
    print(f'ZIP regenerado: zips/paquete_chatgpt_bm.zip')


if __name__ == '__main__':
    main()
