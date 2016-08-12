import kenlm
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def lmscore(question, answer_choices):
    
    return 0

def gen_answer_sentences(question, answer_choices):
    for choice in answer_choices:
        yield question.replace('︽⊙＿⊙︽', choice)

    

if __name__ == '__main__':
    from smttoktag import ZhTokTagger, KenLM, PyTablesTM
    toktagger = ZhTokTagger(
        tm=PyTablesTM('/pix/smttoktag/toktag.phrasetable.h5'),
        lm=KenLM('/pix/smttoktag/tag.blm'))
    
    test_question = '竹節包的出現是來自戰後物質匱乏的1947年　︽⊙＿⊙︽工匠們獨具巧心和創意的創作'
    test_answer_choices = '國道', '小肚', 'gucci', '秋吉', '硫酸'

    zhseg_lm = KenLM('/pix/zh-seg.barpa')

    with ProcessPoolExecutor(max_workers=4) as executor:
        sents = gen_answer_sentences(test_question, test_answer_choices)
        seginfos = executor.map(toktagger, sents)

    for seginfo in seginfos:
        print(seginfo)
        zhseg_lm_score = zhseg_lm(seginfo.zh_seg)
        print(zhseg_lm_score)




