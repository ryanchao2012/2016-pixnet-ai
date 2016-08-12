# coding=UTF-8
from slackbot.bot import respond_to
from slackbot.bot import listen_to
from pix_crawler import *
import os.path
import re, json, random
from datetime import datetime
# rmate test
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

# @respond_to('DEBUG')
# def debug(message):
#     message.send(u"<@{}>: {}{}".format(MR_ROBOT_ID, message, u'\U0001F601'))
#     hey(message)

OPTION_LIST = ['a', 'b', 'c', 'd', 'e']
ANSWER_LIST = []

## 取得 quizmaster 丟出的題目字串，解析出問題及選項
@listen_to(r'題目 (.*)', re.DOTALL)
def receive_question(message, question):
    global CURRENT_TIME
    if message._client.users[message._get_user_id()]['name'] == "pix_quizmaster":
        no, wlist, qidx, anslist = simple_preprocess(question)
        crawler = GoogleCrawler(no, wlist, qidx, anslist)
        with open('question_samples/' + CURRENT_TIME + '.txt', 'a') as f:
            f.write(question)
            f.write('\n')
        ans = crawler.fast_search()
        if ans != None:
            print(ans)
            ANSWER_LIST.append((no, OPTION_LIST[ans[0]]))

    #     m = re.search(r'\[(\d+)\] (.*) ### (.*) \[END\]', question)
    #     quiz_no = int(m.group(1))
    #     question = m.group(2)
    #     options = {}
    #     for item in m.group(3).split(','):
    #         index, value = item.split(':')
    #         options[index] = value
    #     # 可在此呼叫自定義算法，透過題目(question)、選項(options)，計算出該題答案，本範例為 random 一個答案
    #     ANSWER_LIST.append(random.choice(list(options.keys())))
    
@listen_to(r'正確答案是：(.*)')
def collect_answer(message, answer):
    global CURRENT_TIME
    if message._client.users[message._get_user_id()]['name'] == "pix_inspector":
        with open('question_samples/' + CURRENT_TIME + '.txt', 'a') as f:
            f.write(answer)
            f.write('\n')
        CURRENT_TIME = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        hey(message)



## 當 quizmaster 丟出 "機器人小朋友請搶答"，請儘速把答案丟到 channel     
@listen_to(r'機器人小朋友請搶答$')
def hello_send(message):
    # message.send('ANS:')
    if message._client.users[message._get_user_id()]['name'] != "quizmaster":
        reply_ans = ""
        for idx, ans in enumerate(ANSWER_LIST):
            reply_ans += str(idx + 1) + " : " + ans + ", "
        message.send("<@%s>: %s %s" % (PIX_INSPECTOR, '請給分 ', reply_ans[:-2]))
        ANSWER_LIST[:] = []
    


# 幫按讚
@listen_to(r'題號(.*)')
def hey(message):
    message.react('+1')



