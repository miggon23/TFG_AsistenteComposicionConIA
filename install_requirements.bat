@echo off

if not exist env (
    py -3.9 -m venv env

    cd MagentaGenerator
    call install_magenta_dependencies.bat
    cd ..
)

call ./env/Scripts/activate

pip install -r requirements.txt

