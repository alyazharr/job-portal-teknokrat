FROM python:3.8   
# setup environment variable  
ENV DockerHOME=/home/app/webapp  

# set work directory  
RUN mkdir -p $DockerHOME  

# where your code lives  
WORKDIR $DockerHOME  

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

# install dependencies  
RUN pip install --upgrade pip  

# copy whole project to your docker home directory. 
COPY . $DockerHOME  
# run this command to install all dependencies  
RUN pip install -r requirements.txt
# port where the Django app runs  

EXPOSE 8000  

CMD python manage.py makemigrations && \
    python manage.py migrate && \ 
    echo "from jobseeker.models import Users; \
          Users.objects.create_superuser('123',username= 'l1',name = 'ikram',npm= 1,prodi_id= 1)" \
    | python manage.py shell & \
      python manage.py runserver 0.0.0.0:8000 & \
      celery -A jobseeker worker --loglevel=info -P eventlet & \
      celery -A jobseeker beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler