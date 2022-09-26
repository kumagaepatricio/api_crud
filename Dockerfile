FROM python:3.8-alpine
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev \
    && apk add libffi-dev
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN mkdir -p /app/logs/
RUN mkdir -p /app/logs/gunicorn
RUN pip install -r requirements.txt

CMD ["gunicorn", "api_crud.wsgi", "--bind", "0.0.0.0:8000", "--name", "api_crud", "--workers", "4", "--timeout", "3600", "--error-logfile", "/app/logs/gunicorn/gunicorn-error.log", "--log-level", "debug", "--preload"]


