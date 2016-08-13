import kenlm
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from smttoktag import ZhTokTagger, KenLM, PyTablesTM
from string import ascii_lowercase
zhseg_lm = KenLM('/pix/zh-seg.barpa')
zhtag_lm = KenLM('/pix/smttoktag/tag.blm')
zhseg_simple_lm = KenLM('/pix/zh-simple-seg.barpa')
from zh_simple_tok import simple_seg

def lmscore(toked_sents):
    scores = list(map(lambda sent: zhseg_lm[sent] ,toked_sents))
    top_score_choice = max(list(zip(scores, ascii_lowercase)))[1]
    return top_score_choice

def lmscore_simple(sents):
    scores = []
    for sent in sents:
        toked_sent = ' '.join(simple_seg(sent))
        scores.append(zhseg_simple_lm[toked_sent])
    top_score_choice = max(zip(scores, ascii_lowercase))[1]
    return top_score_choice
      

def gen_answer_sentences(question, answer_choices):
    for choice in answer_choices:
        yield question.replace('︽⊙＿⊙︽', choice)

    

if __name__ == '__main__':
    
    toktagger = ZhTokTagger(
        tm=PyTablesTM('/pix/smttoktag/toktag.phrasetable.h5'),
        lm=KenLM('/pix/smttoktag/tag.blm'))
    
    # test_question = '竹節包的出現是來自戰後物質匱乏的1947年　︽⊙＿⊙︽工匠們獨具巧心和創意的創作'
    # test_answer_choices = '國道', '小肚', 'gucci', '秋吉', '硫酸'

    test_question = '一年沒再踏入︽⊙＿⊙︽，這裡變化真的相當多，不知道下次再踏入這塊土地，是否又會有不一樣的感覺呢'

    test_answer_choices =  '涼拌菜', '墾丁', '邊框', '生田', '金金'
    import time
    start_time = time.time()
    

    sents = list(gen_answer_sentences(test_question, test_answer_choices))
    seginfos = list(map(toktagger, sents))
    scores = list(map(lambda seginfo: zhseg_lm(seginfo.zh_seg), seginfos))
    elapsed_time = time.time() - start_time
    print('elapsed: ', elapsed_time)

    for seginfo, choice, score in zip(seginfos, test_answer_choices, scores):
        print('\033[0;34m', seginfo, '\033[m')
        print(choice, score)
    

    print('question:', test_question)
    print('choices scores:', list(zip(test_answer_choices, scores)))
    print('winner:', max(zip(scores, test_answer_choices)))


    print(lmscore_simple(sents))
