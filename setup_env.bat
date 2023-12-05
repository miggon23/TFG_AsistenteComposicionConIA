@echo off
REM Crear el entorno virtual
python -m venv .env

REM Activar el entorno virtual (usando PowerShell)
powershell -Command "& { .\.env\Scripts\Activate }"

REM Instalar las dependencias desde el archivo requirements.txt
pip install -r requirements.txt