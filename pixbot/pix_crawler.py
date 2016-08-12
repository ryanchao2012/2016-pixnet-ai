from urllib.parse import quote
from urllib import request
import codecs, jieba
import re, html, time
from os import listdir
from os.path import isfile, join
import random

jieba.add_word('龐傍燮謝', freq=10, tag='xx')

def simple_preprocess(sample):
    no, content, a, b, c, d, e = re.findall(r'\[(\d+)\](.*)### a:(.*), b:(.*), c:(.*), d:(.*), e:(.*)\[END\]', sample)[0]
    options = [a.strip(), b.strip(), c.strip(), d.strip(), e.strip()]
    content = re.sub('(")(.?)', r'\2', content.strip())
    content = content.strip().replace('︽⊙＿⊙︽', '龐傍燮謝')
    wlist = list(jieba.cut(content))
    qidx = []
    i = 0
    for w in wlist:
        if w == '龐傍燮謝':
            wlist[i] = '*'
            qidx.append(i)
        i += 1
    return (no, wlist, qidx, options)

class GoogleCrawler(object):
    def __init__(self, qno, wlist, qidx, anslist):
        self.qno = qno
        self.wlist = wlist
        self.iqlist = qidx
        self.anslist = anslist
        self.qnum = 2
        self.rand_query = []
        self.set_rand_query()
    
    def add_rand_query(self, rwlist = None, qidx = None):
        if rwlist == None or qidx == None:
            rwlist = self.wlist
            qidx = self.iqlist
            rwlen = len(rwlist)
            
            for i in range(self.qnum):
                iq = random.choice(qidx)
                if iq > 0:
                    ihead = random.choice(range(0, iq))
                else:
                    ihead = 0
                if iq + 1 < rwlen:
                    iend = random.choice(range(iq + 1, rwlen))
                else:
                    iend = rwlen- 1
                self.rand_query.append(''.join(rwlist[ihead : iend]))
                
    def set_rand_query(self):
        self.rand_query = []
        self.add_rand_query()
    
    def get_rand_query(self):
        return self.rand_query
    
    def print_rand_query(self):
        for q in self.rand_query:
            print(q)
    
    def crawl(self, query):
        raw_html = self.google_crawl(query).lower()
        clean_html = self.clean_html(raw_html)
        return clean_html
    
    def multitask_craw(self):
        pass
    
    def fast_search(self):
        html_pool = ''
        for q in self.rand_query:
            html_pool += self.crawl(q)
            time.sleep(0.5)
        for x in self.anslist:
            if html_pool.find(x) > 0:
                return (self.anslist.index(x), x)
        return None
        
    def google_crawl(self, query = None):
        if query == None: query = self.short_query
        self.link = "https://www.google.com/search?q=" + quote(query)  + '&ie=utf8&oe=utf8' # + '&lr=lang_zh-TW'
        req = request.Request(self.link, headers = {'User-Agent' : "Chrome Browser"})
        raw = html.unescape(request.urlopen(req).read().decode('utf-8'))
        return raw
    
    def clean_html(self, raw_html = None):
        if raw_html == None: raw_html = self.google_crawl(self.short_query)
        clean_html = re.sub(re.compile(r'(<br?>)|(</br?>)|\n|\r|\s'), '', raw_html)
        return clean_html
