# coding=UTF-8
import gevent
from gevent import monkey; monkey.patch_all(socket=False)
from parallel_toktag import parallel_toktag
from slackbot.bot import respond_to
from slackbot.bot import listen_to
from strmatch import *
# from pix_crawler import *
import os.path
import re, json, random, time
from datetime import datetime
from pix_lm import *
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
CHANNEL_ID = "C1QQG5SJG"
PIX_INSPECTOR = "U1QDCHJ3H"
PIX_INSPECTOR_USERNAME = "pix_inspector"
PIX_QUIZMASTER_USERNAME = "pix_quizmaster"
PIX_QUESTION_NUM = 1
# @respond_to('DEBUG')
# def debug(message):
#     message.send(u"<@{}>: {}{}".format(MR_ROBOT_ID, message, u'\U0001F601'))
#     hey(message)

OPTION_LIST = ['a', 'b', 'c', 'd', 'e']
ANSWER_LIST = []
PIX_MODE = 20
def question_preprocess(question):
    q_no, q_body, a, b, c, d, e = re.findall(r'\[(\d+)\](.*)### a:(.*), b:(.*), c:(.*), d:(.*), e:(.*)\[END\]', question)[0]
    return (int(q_no), q_body.strip(), (a.strip(), b.strip(), c.strip(), d.strip(), e.strip()))


def feed_option_in_question(raw_question, options):
    feed_sents = []
    for choice in options:
        feed_sents.append(raw_question.replace('︽⊙＿⊙︽', choice))
    return feed_sents

@respond_to(r'sset (.*)', re.DOTALL)
def setmode(message, mode):
    try:
        PIX_MODE = int(mode)
        # message.send(str(PIX_MODE))
    except:
        pass

@respond_to(r'ddbug (.*)', re.DOTALL)
def debug(message, question):
    
    q_no, q_body, options = question_preprocess(question)
    print('{}\n{}\n{}\n'.format(q_no, q_body, options))
    lm_ans = None
    strmatch_ans = None
    craw_ans = None
    feed_sents = feed_option_in_question(q_body, options)
    t = time.time()
    strmatch_ans = grepsents(feed_sents)
    
    seginfos = parallel_toktag(feed_sents)
    lm_ans = cal_lmscore(seginfos)
    lmsimple_ans = lmscore_simple(feed_sents)
    print(time.time() - t)
    print("{},{},{}\n".format(strmatch_ans, lm_ans, lmsimple_ans))
    
    t = time.time()
    jobs = [gevent.spawn(grepsents, feed_sents),
            gevent.spawn(cal_lmscore, seginfos),
            gevent.spawn(lmscore_simple, feed_sents)]
    gevent.joinall(jobs, timeout=1)
    print(time.time() - t)
    ans = [job.value for job in jobs]
    print(ans)
    

## 取得 quizmaster 丟出的題目字串，解析出問題及選項
@listen_to(r'題目 (.*)', re.DOTALL)
def receive_question(message, question):
    global CURRENT_TIME
    if message._client.users[message._get_user_id()]['name'] == PIX_QUIZMASTER_USERNAME:
        q_no, q_body, options = question_preprocess(question)
        # lm_ans = None
        # strmatch_ans = None
        # craw_ans = None
        # crawler = None
        # no, wlist, qidx, anslist = simple_preprocess(question)
        # try:
        #     crawler = GoogleCrawler(no, wlist, qidx, anslist)
        # except Exception as inst:
        #     print('[{}]{}'.format(type(inst), inst))
        # if crawler != None:
        #     ans = crawler.fast_search()
        feed_sents = feed_option_in_question(q_body, options)
        seginfos = parallel_toktag(feed_sents)
        jobs = [gevent.spawn(grepsents, feed_sents),
                gevent.spawn(lmscore_simple, feed_sents),
                gevent.spawn(cal_lmscore, seginfos)]
        gevent.joinall(jobs, timeout=1)
        ans = [job.value for job in jobs]
        for a in ans:
            if a != -1 and a != None:
                ANSWER_LIST.append((q_no, a))
                break
        
                #
        # strmatch_ans = grepsents(feed_sents)
        # if strmatch_ans != -1 and strmatch_ans != None:
        #     print(q_no, strmatch_ans)
        #     ANSWER_LIST.append((q_no, strmatch_ans))
        # else:
        #     print("strmatch failed: {}".format(q_no))
        #     seginfos = parallel_toktag(feed_sents)
        #     lm_ans = cal_lmscore(seginfos)
        #     if lm_ans != None:
        #         print(q_no, lm_ans)
        #         ANSWER_LIST.append((q_no, lm_ans))
        #     else:
        #         print("lm failed: {}".format(q_no))
        #         ANSWER_LIST.append((q_no, random.choice(OPTION_LIST)))
                
#        threads = [gevent.spawn(task, i) for i in xrange(10)]
#        gevent.joinall(threads)
        
        # with open('question_samples/' + CURRENT_TIME + '.txt', 'a') as f:
        #     f.write(question)
        #     f.write('\n')
        
        

    
@listen_to(r'正確答案是：(.*)')
def collect_answer(message, answer):
    global CURRENT_TIME
    ANSWER_LIST[:] = []
    # if message._client.users[message._get_user_id()]['name'] == "pix_inspector":
        # with open('question_samples/' + CURRENT_TIME + '.txt', 'a') as f:
        #     f.write(answer)
        #     f.write('\n')
        # CURRENT_TIME = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        # hey(message)



## 當 quizmaster 丟出 "機器人小朋友請搶答"，請儘速把答案丟到 channel     
@listen_to(r'機器人小朋友請搶答$')
def hello_send(message):
    # message.send('ANS:')
    if message._client.users[message._get_user_id()]['name'] == PIX_QUIZMASTER_USERNAME:
        reply_ans = ""
        while(len(ANSWER_LIST) < PIX_QUESTION_NUM): time.sleep(0.01)
        for idx, ans in ANSWER_LIST:
            reply_ans += str(idx) + " : " + ans + ", "
        message.send("<@%s>: %s %s" % (PIX_INSPECTOR, '請給分 ', reply_ans[:-2]))
        ANSWER_LIST[:] = []
    


# 幫按讚
@listen_to(r'題號(.*)')
def hey(message):
    message.react('+1')



