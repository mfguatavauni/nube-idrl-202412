from celery import Celery

def make_celery():
    return Celery(
        'app',
        backend='redis://34.121.134.171:6379/0',
        broker='redis://34.121.134.171:6379/0'
    )

celery = make_celery()
