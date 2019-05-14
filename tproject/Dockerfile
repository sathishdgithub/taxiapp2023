FROM python:2.7
ENV PYTHONUNBUFFERED 1
WORKDIR /tproject
RUN pip install mod_wsgi-httpd
COPY requirements.txt /tproject/
RUN pip install -r requirements.txt
COPY . /tproject/
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]