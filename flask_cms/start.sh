#!/bin/bash
export FLASK_PORT=8088;
export SERVER_COMMAND="python manage.py runserver --host=0.0.0.0 --port=$FLASK_PORT";
if [ "$1" == "twisted" ]; then
    export SERVER_COMMAND="twistd -n web --port $FLASK_PORT --wsgi=app.app";
fi

$SERVER_COMMAND
