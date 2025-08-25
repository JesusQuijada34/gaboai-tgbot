REM Hacer que "echo" tenga curva de aprendizaje, solo en Windows FlitPack Edition
echo e
echo @e
echo off
cls
echo Curveado!. Instalando dependencias...
pip install -r lib/requirements.txt

REM Sensores: Comprobar si Python está instalado
where python >nul 2>nul
if errorlevel 1 (
    echo [Sensor] Python no está instalado. Por favor, instale Python 3.x antes de continuar.
    pause
    exit /b 1
) else (
    echo [Sensor] Python detectado.
)

REM Sensor: Comprobar si requirements.txt existe
if not exist lib\requirements.txt (
    echo [Sensor] El archivo lib\requirements.txt no existe. Abortando instalacion de dependencias.
    pause
    exit /b 1
) else (
    echo [Sensor] Archivo de dependencias encontrado.
)

REM Cargar variables desde .env si existe
if exist .env (
    echo [Sensor] Archivo .env detectado. Cargando variables de entorno...
    for /f "usebackq tokens=* delims=" %%a in (".env") do set %%a
) else (
    echo [Sensor] No se encontro archivo .env. Continuando sin variables de entorno adicionales.
)

REM Sensor: Comprobar si el script principal existe
if not exist gaboai-tgbot.py (
    echo [Sensor] El archivo gaboai-tgbot.py no existe. Abortando.
    pause
    exit /b 1
) else (
    echo [Sensor] Script principal detectado.
)

python gaboai-tgbot.py

REM Sensor: Comprobar el código de salida del script
if errorlevel 1 (
    echo [Sensor] El script gaboai-tgbot.py terminó con errores.
    pause
    exit /b 1
) else (
    echo [Sensor] El script gaboai-tgbot.py finalizó correctamente.
)
