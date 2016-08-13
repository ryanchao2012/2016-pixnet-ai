from parallel_toktag import parallel_toktag
from urllib.parse import quote
from urllib import request
import codecs, jieba
import re, html, time
from os import listdir
from os.path import isfile, join
import random
from operator import attrgetter
from lmscore import *
# toktagger = ZhTokTagger(
#         tm=PyTablesTM('/pix/smttoktag/toktag.phrasetable.h5'),
#         lm=KenLM('/pix/smttoktag/tag.blm'))
OPTION_LIST = ['a', 'b', 'c', 'd', 'e']
SAMPLE_PATH = '../pixbot/question_samples/'
SAMPLE_FILES = [f for f in listdir(SAMPLE_PATH) if isfile(join(SAMPLE_PATH, f))]

def sample_lmscore(sample):
    no, content, a, b, c, d, e = re.findall(r'\[(\d+)\](.*)### a:(.*), b:(.*), c:(.*), d:(.*), e:(.*)\[END\]', sample)[0]
    # content = re.sub('(")(.?)', r'\2', content.strip())
    sents = gen_answer_sentences(content, (a,b,c,d,e))
    seginfos = parallel_toktag(sents)
    # print(seginfos[0])
    # lmscore(list(map(attrgetter('zh_seg'), seginfos)))
    # scores = list(map(lambda seginfo: lmscore(seginfo.zh_seg), seginfos))
    return (no, lmscore(list(map(attrgetter('zh_seg'), seginfos))))
    

if __name__ == '__main__':
    correct = 0
    total = 0
    import time
    start_time = time.time()
    for dummy in range(10):
        file = random.choice(SAMPLE_FILES)
        ans = []
        samples = ['-1', '-1', '-1', '-1', '-1','-1', '-1', '-1', '-1', '-1']
        pred = ['-1', '-1', '-1', '-1', '-1','-1', '-1', '-1', '-1', '-1']
        with codecs.open(SAMPLE_PATH + file, 'r', 'utf-8') as f:
            for line in f:
                if line.find('[END]') < 0:
                    ans = line.strip().split(' ')
                else:
                    (no, a) = sample_lmscore(line.strip())
                    samples[int(no)-1] = line
                    pred[int(no)-1] = a
            for j in range(len(ans)):
                if pred[j] == ans[j]:
                    correct += 1
                else:
                    with open('lmscore_failure_log.txt', 'a') as f:
                        f.write('[sample]{}[yh]{}[y]{}\n'.format(samples[j][:-1], pred[j], ans[j]))
                total += 1
            print('batch accuracy', float(correct)/float(total))
    elapsed_time = time.time() - start_time
    print('tested samples: ', str(total))
    print('elapsed: ', elapsed_time)
    print('overall accuracy: ', float(correct)/float(total))
    
    