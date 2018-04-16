FROM python:latest

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
ADD . /code/

RUN ls /code

RUN pip install -r /code/requirements.txt
RUN python3 manage.py collectstatic --noinput --clear

RUN echo Making migrations.
RUN python3 manage.py makemigrations
RUN echo Migrating.
RUN yes yes | python3 manage.py migrate

RUN python3 create_admin.py

EXPOSE 8000

COPY start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]

