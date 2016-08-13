import time

# start_time = time.time()
# lines = open('/pix/zh-all.txt').readlines()
# elapsed_time = time.time() - start_time
# print('load elapsed time', elapsed_time)


def gen_answer_sentences(question, answer_choices):
    for choice in answer_choices:
        yield question.replace('︽⊙＿⊙︽', choice)


from string import ascii_lowercase
from cytoolz import first


def is_in_lines(sent):
    for line in lines:
        if sent in line:
            return line
    else:
        return None


def strmatch(sents):

    sents_is_matched = [is_in_lines(sent) for sent in sents]
#    print(sents_is_matched)
    return [choice
            for is_matched, choice in zip(sents_is_matched, ascii_lowercase)
            if is_matched]


import subprocess
def grepsents(sents):
    return first(choice for sent, choice in zip(sents, ascii_lowercase)
                 if subprocess.run(['grep', '-Fl', sent, '/pix/zh-all.txt'
                                   ], stdout=subprocess.PIPE).returncode == 0)


def grep_question(question, choiceList):
    pre_str, post_str, *_ = question.split('︽⊙＿⊙︽')
    cmd = "grep -F '{pre_str}' /pix/zh-all.txt | grep -Po '(?<={pre_str}).+(?={post_str})'".format(pre_str=pre_str, post_str=post_str)
    matched_choice = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    return gotcha(matched_choice, choiceList)

import gensim

def gotcha(keyword, choiceList):
    if len(keyword) == 0:
        return -1
    else:
        choice = ['a','b','c','d','e']
        for i in range(len(choiceList)):
            try:
                choiceList[i] = model.similarity(keyword, choiceList[i])
            except KeyError:
                choiceList[i] = -999999999
        return choice[choiceList.index(max(choiceList))]

if __name__ == '__main__':
    test_question = '一年沒再踏入︽⊙＿⊙︽，這裡變化真的相當多，不知道下次再踏入這塊土地，是否又會有不一樣的感覺呢'
    test_answer_choices = ['飛機', '邊框', '田', '金金', '墾丁']
    model = gensim.models.Word2Vec.load_word2vec_format('/home/ifengc/dav/word2vec/data/zhseg-all-vector.bin', binary=True)
    start_time = time.time()
    sents = gen_answer_sentences(test_question, test_answer_choices)
    print(grepsents(sents))
    print(grep_question(test_question, test_answer_choices))
    elapsed_time = time.time() - start_time
#    print('find elapsed time', elapsed_time)
