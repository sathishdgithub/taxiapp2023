# FROM python:3.10
# ENV PYTHONUNBUFFERED 1
# # nginx installation
# RUN apt-get update
# # RUN apt-get -y install nginx
# # COPY nginx/. /etc/nginx/
# # Debugging tools
# # RUN apt-get -y install lsof
# # RUN apt-get -y install vim
# # application
# RUN mkdir tproject
# WORKDIR /tproject
# RUN pip install --upgrade setuptools==57.5.0
# # RUN pip install mod_wsgi-httpd
# COPY . /tproject
# RUN pip install --upgrade pip 
# # COPY requirements.txt /tproject/
# RUN pip install -r requirements.txt
# #COPY . /tproject/
# # EXPOSE 80
# # EXPOSE 443
# #CMD nginx -g 'daemon on;' && python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
# # CMD nginx -g 'daemon on;' && 
# CMD python manage.py runserver 0.0.0.0:8000&

FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN apt-get update

RUN mkdir tproject

WORKDIR /tproject

RUN apt-get install -y apache2 apache2-dev

RUN pip install mod_wsgi

#RUN apt-get install -y python3-pip apache2 libapache2-mod-wsgi-py3

RUN pip install --upgrade setuptools==57.5.0

COPY . /tproject

RUN pip install --upgrade pip 

RUN pip install -r requirements.txt
 
#CMD python manage.py runserver 0.0.0.0:8000&

#RUN ["chmod", "+x", "./python-run.sh"]

#CMD ./python-run.sh
