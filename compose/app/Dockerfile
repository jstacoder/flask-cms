FROM python:2.7-alpine 
ARG DB_HOST

ENV DATABASE_URI postgres://user:pw@${DB_HOST}:5432/db
ENV DATABASE_URL postgres://user:pw@${DB_HOST}:5432/db

WORKDIR /app

EXPOSE 5000

COPY ./flask_cms /app/flask_cms

ADD ./compose/app/local_settings.py /app/flask_cms/

ADD ./compose/app/initalize.sh /

ADD ./setup.py /app/

ADD ./flask_cms/requirements.txt /app/flask_cms

RUN chmod +x /initalize.sh

RUN apk update && \
    apk add postgresql-dev gcc python-dev musl-dev && \
    python /app/setup.py develop && \
    pip install ipython

CMD ["/bin/sh"]