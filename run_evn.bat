@echo off
REM Establecer la política de ejecución de scripts en PowerShell
powershell -Command "& { Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass }"

REM Activar el entorno virtual (usando PowerShell)
powershell -Command "& { .\.env\Scripts\Activate }"

REM Agrega cualquier otro comando que desees ejecutar después de activar el entorno virtual
REM Por ejemplo, puedes lanzar tu script Python o abrir el intérprete interactivo, etc.
