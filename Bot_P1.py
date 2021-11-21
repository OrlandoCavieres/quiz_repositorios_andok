from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.ext.dispatcher import run_async
import requests
import re


def get_url():
    return requests.get('https://random.dog/woof.json').json()['url']


@run_async
def bop(update, context):
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id = chat_id, photo = get_url())


