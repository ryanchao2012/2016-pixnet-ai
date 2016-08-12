import kenlm
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from smttoktag import ZhTokTagger, KenLM, PyTablesTM

zhseg_lm = KenLM('/pix/zh-seg.barpa')

def lmscore(sent):
    return zhseg_lm[sent]
    

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

    test_answer_choices =  '墾丁','涼拌菜', '邊框', '生田', '金金'

    sents = gen_answer_sentences(test_question, test_answer_choices)
    seginfos = list(map(toktagger, sents))
    import time
    start_time = time.time()
    scores = list(map(lambda seginfo: zhseg_lm(seginfo.zh_seg), seginfos))
    elapsed_time = time.time() - start_time
    print('elapsed: ', elapsed_time)

    for seginfo, choice, score in zip(seginfos, test_answer_choices, scores):
        print('\033[0;34m', seginfo, '\033[m')
        print(choice, score)
    

    print('question:', test_question)
    print('choices scores:', list(zip(test_answer_choices, scores)))
    print('winner:', max(zip(scores, test_answer_choices)))



