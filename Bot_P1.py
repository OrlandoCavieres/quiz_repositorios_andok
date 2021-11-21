from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.ext.dispatcher import run_async
import requests
import re


def get_url():
    return requests.get('https://random.dog/woof.json').json()['url']


def get_image_url():
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''
    url = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$", url()).group(1).lower()
    return url


@run_async
def bop(update, context):
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id = chat_id, photo = get_url())


def main():
    updater = Updater('2145587260:AAHERLnOnFYRrM2ymJT0vH4PL28yDaUQKqk', use_context = True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop', bop))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
