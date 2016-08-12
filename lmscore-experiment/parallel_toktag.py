from celery import group
from tasks import toktag_sentence

if __name__ == '__main__':
    from itertools import permutations
    sents = list(map(lambda x: ''.join(x), list(permutations('我要出去玩'))))
    jobs =group(toktag_sentence.s(sent) for sent in sents)
    result = job.apply_async()
    result.ready()
    result.successful()
    seginfos = result.get()

