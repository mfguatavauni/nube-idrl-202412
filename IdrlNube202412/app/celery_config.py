from celery import Celery

def make_celery():
    return Celery(
        'app',
        backend='redis://redis:6379/0',
        broker='redis://redis:6379/0'
    )

celery = make_celery()
