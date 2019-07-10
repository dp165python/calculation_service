from celery import Celery

celery = Celery('mission', broker='amqp://guest:guest@localhost:5672')
