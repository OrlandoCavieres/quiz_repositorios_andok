import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Poll
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, PollHandler
import time


def help_handler(update, _):
    update.message.reply_text('Escribe solamente /start en un nuevo mensaje y solo.')


def get_chat_id(update, context):
    chat_id = -1
    if update.message is not None:
        chat_id = update.message.chat_id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat_id
    elif update.poll is not None:
        chat_id = context.bot_data[update.poll.id]

    return chat_id


def start_handler(update, context):
    add_typing(update, context)
    pass


def add_typing(update, context):
    context.bot.send_chat_action(
        chat_id = get_chat_id(update, context),
        action = telegram.ChatAction.TYPING,
        timeout = 1
    )
    time.sleep(1)


def poll_handler(update, context):
    pass


def main():
    updater = Updater('2103805315:AAG1rrpy0lWIx1lq3CVV2U1_ykYNi0qBvOY', use_context = True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('help', help_handler))
    dp.add_handler(CommandHandler('start', start_handler))

    dp.add_handler(PollHandler(poll_handler, pass_chat_data = True, pass_user_data = True))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
