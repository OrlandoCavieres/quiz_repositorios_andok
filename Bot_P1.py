from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.ext.dispatcher import run_async
import requests
import re


def get_url():
    return requests.get('https://random.dog/woof.json').json()['url']

