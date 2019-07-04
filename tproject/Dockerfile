FROM python:2.7
ENV PYTHONUNBUFFERED 1
# nginx installation
RUN apt-get update
RUN apt-get -y install nginx
COPY nginx/. /etc/nginx/
# Debugging tools
# RUN apt-get -y install lsof
# RUN apt-get -y install vim
# application
WORKDIR /tproject
RUN pip install mod_wsgi-httpd
COPY requirements.txt /tproject/
RUN pip install -r requirements.txt
COPY . /tproject/
EXPOSE 80
EXPOSE 443
CMD nginx -g 'daemon on;' && python manage.py runserver 0.0.0.0:8000
