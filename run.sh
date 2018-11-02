export FLASK_APP=flask_main.py
SECRETS="secrets.txt"

if [ -s ${SECRETS} ]; then
    export FLASK_SECRET_KEY=$(cat secrets.txt)
else
    undef FLASK_SECRET_KEY
fi

flask run