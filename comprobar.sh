#!/usr/bin/env bash
# Comprobación del paquete B&M antes de entregar cualquier documento.
# Uso:  ./comprobar.sh   (o: bash comprobar.sh)
set -u
cd "$(dirname "$0")" || exit 1

echo "============================================"
echo " B&M · comprobación del paquete"
echo "============================================"
echo

if ! command -v python3 >/dev/null 2>&1 && ! command -v python >/dev/null 2>&1; then
    echo "ERROR: Python no está instalado o no está en el PATH."
    exit 1
fi
PY=$(command -v python3 || command -v python)

"$PY" -c "import pymupdf" 2>/dev/null || {
    echo "Instalando la única dependencia necesaria (pymupdf)…"
    "$PY" -m pip install --quiet pymupdf
}

echo "[1/3] Batería de pruebas…"
"$PY" eval/run.py || {
    echo
    echo "ATENCIÓN: hay pruebas en rojo. NO entregues ningún documento hasta arreglarlo."
    exit 1
}

echo
echo "[2/3] Estado de los precios…"
"$PY" tools/estado_precios.py

echo
echo "[3/3] Documentos emitidos con hoja de precios anterior a la vigente…"
"$PY" tools/indice_informes.py --revisar

echo
echo "============================================"
echo " Todo comprobado."
echo "============================================"