#!/bin/bash
TGT='manage.py'
HOST='0.0.0.0'
PORT='8080'
CMD='runserver'
PY='/usr/bin/python'

$PY $TGT $CMD --host=$HOST --port=$PORT

