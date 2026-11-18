@echo off
REM Comprobacion del paquete B&M antes de entregar cualquier documento.
REM Uso: doble clic, o desde la consola:  comprobar.bat
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================
echo  B^&M - comprobacion del paquete
echo ============================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH.
    echo Instalalo desde https://www.python.org/downloads/ marcando "Add python.exe to PATH".
    pause
    exit /b 1
)

python -c "import pymupdf" 2>nul
if errorlevel 1 (
    echo Instalando la unica dependencia necesaria ^(pymupdf^)...
    python -m pip install --quiet pymupdf
)

echo [1/3] Bateria de pruebas...
python eval\run.py
if errorlevel 1 (
    echo.
    echo ATENCION: hay pruebas en rojo. NO entregues ningun documento hasta arreglarlo.
    pause
    exit /b 1
)

echo.
echo [2/3] Estado de los precios...
python tools\estado_precios.py

echo.
echo [3/3] Documentos emitidos con hoja de precios anterior a la vigente...
python tools\indice_informes.py --revisar

echo.
echo ============================================
echo  Todo comprobado. Si las pruebas estan en verde,
echo  puedes generar documentos.
echo ============================================
pause
