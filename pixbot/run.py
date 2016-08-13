from slackbot.bot import Bot
from slackbot import settings
from slackbot_settings import *
import os

settings.API_TOKEN = os.environ['PIX_BOT']
# settings.DEFAULT_REPLY = ""

def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()

