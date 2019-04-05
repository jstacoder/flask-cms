#!/bin/sh

APP_PATH=/app/flask_cms/
MANAGE_PY=${APP_PATH}manage.py

python ${MANAGE_PY} db upgrade 
python ${MANAGE_PY} init_data

#python ${MANAGE_PY} runserver --host 0.0.0.0 --port 5000 
