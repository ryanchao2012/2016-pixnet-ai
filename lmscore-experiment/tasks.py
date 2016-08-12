from smttoktag import ZhTokTagger, KenLM, PyTablesTM
from celery import Celery
from celery import Task
from celery.signals import worker_process_init, worker_init

toktagger = None


@worker_process_init.connect
def loadtoktagger(sender=None, body=None, **kwargs):
    global toktagger
    print('init')
    toktagger = ZhTokTagger(
        tm=PyTablesTM('/pix/smttoktag/toktag.phrasetable.h5'),
        lm=KenLM('/pix/smttoktag/tag.blm'))


BROKER_URL = 'amqp://guest:guest@localhost:5672//'
app = Celery(
    'tasks', broker=BROKER_URL, backend='amqp://', CELERY_RESULT_BACKEND='amqp')


@app.task
def toktag_sentence(sent):
    return toktagger(sent)
