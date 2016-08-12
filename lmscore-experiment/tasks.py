
from smttoktag import ZhTokTagger, KenLM, PyTablesTM
from celery import Celery

BROKER_URL = 'amqp://guest:guest@localhost:5672//'
app = Celery('tasks', broker=BROKER_URL, backend='amqp://', CELERY_RESULT_BACKEND = 'amqp'
)


toktagger = ZhTokTagger(
    tm=PyTablesTM('/pix/smttoktag/toktag.phrasetable.h5'),
    lm=KenLM('/pix/smttoktag/tag.blm'))
    

@app.task
def toktag_sentence(sent):
    return toktagger(sent)

