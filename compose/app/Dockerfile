FROM python:2.7-alpine 
ARG DB_HOST

ENV DATABASE_URI postgres://user:pw@${DB_HOST}:5432/db
ENV DATABASE_URL postgres://user:pw@${DB_HOST}:5432/db

WORKDIR /app



RUN apk update && \
    apk add postgresql-dev gcc python-dev musl-dev 

RUN mkdir /app/flask_cms


ADD setup.py /app/

ADD ./flask_cms/requirements.txt /app/

RUN python /app/setup.py develop && \
    pip install ipython

RUN pip install redis

EXPOSE 5000

ADD ./flask_cms/ /app/flask_cms

ADD ./compose/app/local_settings.py /app/flask_cms

ADD ./compose/app/initalize.sh /

RUN chmod +x /initalize.sh



CMD ["/bin/sh"]