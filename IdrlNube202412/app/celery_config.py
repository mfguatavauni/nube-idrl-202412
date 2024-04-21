from celery import Celery

def make_celery():
    return Celery(
        'app',
        backend='redis://34.72.18.166:6379/0',
        broker='redis://34.72.18.166:6379/0'
    )

celery = make_celery()
