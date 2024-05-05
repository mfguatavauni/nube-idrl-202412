from celery import Celery

def make_celery():
    return Celery(
        'app',
        backend='redis://104.197.174.214:6379/0',
        broker='redis://104.197.174.214:6379/0'
    )

celery = make_celery()
