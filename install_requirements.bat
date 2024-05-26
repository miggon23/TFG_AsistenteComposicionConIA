if not exist env (
    py -3.9 -m venv env
)

call ./env/Scripts/activate

pip install -r requirements.txt

