FROM python:3.8-alpine
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev \
    && apk add libffi-dev
RUN python3 -m venv /opt/venv
CMD . /opt/venv/bin/activate
RUN pip install -r requirements.txt
RUN touch db.sqlite3
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('ine_admin', 'admin@ine.com', 'ineadminpass')"

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
