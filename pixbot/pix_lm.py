from operator import attrgetter
from lmscore import lmscore, lmscore_simple

def cal_lmscore(seginfos):
    return lmscore(list(map(attrgetter('zh_seg'), seginfos)))

# def cal_simplelmscore(feed_sents):
#     return lmscore_simple(list(map(attrgetter('zh_seg'), feed_sents)))