if not exist env (
    call instalar_dependencias.bat
)

call ./env/Scripts/activate

py appRoot.py