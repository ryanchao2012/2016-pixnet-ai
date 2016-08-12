from celery import group
from tasks import toktag_sentence
import logging
logging.basicConfig(format='[%(asctime)s] %(levelname)s:%(message)s', level=logging.WARN)
import time


def parallel_toktag(sents):
    start_time = time.time()
    logging.warn('start')
    jobs =group(toktag_sentence.s(sent) for sent in sents)
    result = jobs.apply_async()
    logging.warn('apply')
    result.ready()
    result.successful()
    seginfos = result.get()
    logging.warn('end')
    elapsed_time = time.time() - start_time
    logging.warn('elapsed: %s', elapsed_time)
    return seginfos
    

if __name__ == '__main__':
    from itertools import permutations, islice
    sents = list(map(lambda x: ''.join(x), islice(permutations('我要出去玩，不想上班。好累喔！'), 0, 100)))
    parallel_toktag(sents)
    # print(parallel_toktag(sents))
    logging.warn('print')
