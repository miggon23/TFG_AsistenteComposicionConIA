if not exist env (
    call install_requirements.bat
)

call ./env/Scripts/activate

py appRoot.py