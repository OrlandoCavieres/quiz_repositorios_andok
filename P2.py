import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Poll
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, PollHandler
import time
import random


questions = [
    [
        '¿Como se puede saber si una rama ya se le ha hecho un merge a master mediante comandos de línea?',
        ['git branch --merged / --unmerged', 'git status', 'git log --inline branch status'],
        [0, 1],
        ['git branch --merged / --unmerged']
    ],
    # ['2', ['water', 'ice', 'wine'], [0, 2], 'wine'],
    # ['3', ['water', 'ice', 'wine'], [0, 2], 'wine'],
    # ['4', ['water', 'ice', 'wine'], [0, 2], 'wine'],
    # ['5', ['water', 'ice', 'wine'], [0, 2], 'wine'],
    # ['6', ['water', 'ice', 'wine'], [0, 2], 'wine'],
    # ['7', ['water', 'ice', 'wine'], [0, 2], 'wine'],
    # ['8', ['water', 'ice', 'wine'], [0, 2], 'wine'],
    # ['9', ['water', 'ice', 'wine'], [0, 2], 'wine'],
    # ['10', ['water', 'ice', 'wine'], [0, 2], 'wine'],
    # ['11', ['water', 'ice', 'wine'], [0, 2], 'wine'],
    # ['12', ['water', 'ice', 'wine'], [0, 2], 'wine'],
]

count = 0
correct_answers = 0
ya_preguntadas = []


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
    global count, ya_preguntadas
    add_typing(update, context)
    add_text_message(update, context, f"Pregunta 1 de 6")
    quizz_question = random.choice(questions)
    while quizz_question in ya_preguntadas:
        quizz_question = random.choice(questions)
    count += 1
    print(count)
    ya_preguntadas.append(quizz_question)
    print(ya_preguntadas)
    add_quiz_question(update, context, quizz_question)


def add_quiz_question(update, context, quiz_question):
    message = context.bot.send_poll(
        chat_id = get_chat_id(update, context),
        question = quiz_question[0],
        options = quiz_question[1],
        type = Poll.REGULAR if len(quiz_question[2]) > 1 else Poll.QUIZ,
        allows_multiple_answers = len(quiz_question[2]) > 1,
        correct_option_id = None if len(quiz_question[2]) > 1 else quiz_question[2][0]
    )
    context.bot_data.update({message.poll.id: message.chat.id})


def add_typing(update, context):
    context.bot.send_chat_action(
        chat_id = get_chat_id(update, context),
        action = telegram.ChatAction.TYPING,
        timeout = 1
    )
    time.sleep(1)


def poll_handler(update, context):
    print(f"question : {update.poll.question}")
    print(f"correct option : {update.poll.correct_option_id}")
    print(f"option #1 : {update.poll.options[0]}")
    print(f"option #2 : {update.poll.options[1]}")
    print(f"option #3 : {update.poll.options[2]}")

    user_answer = get_answer(update)
    if update.poll.allows_multiple_answers:
        print(f'Permite respuesta multiple')
    print(f'Respuesta: {user_answer}')
    print(f"Opción Correcta: {is_answer_correct(update)}")

    add_typing(update, context)
    add_text_message(update, context, f"LLevas 1 de 6 preguntas")


def add_text_message(update, context, message):
    context.bot.send_message(chat_id = get_chat_id(update, context), text = message)


def get_answer(update):
    answers = update.poll.options

    ret = ''
    for answer in answers:
        if answer.voter_count == 1:
            ret = answer.text

    return ret


def is_answer_correct(update):
    answers = update.poll.options

    ret = False
    counter = 0

    for answer in answers:
        if answer.voter_count == 1 and update.poll.correct_option_id == counter:
            ret = True
            break

        counter += 1

    return ret


def main_handler(update, context):
    pass


def main():
    updater = Updater('2103805315:AAG1rrpy0lWIx1lq3CVV2U1_ykYNi0qBvOY', use_context = True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('help', help_handler))
    dp.add_handler(CommandHandler('start', start_handler))

    dp.add_handler(MessageHandler(Filters.text, main_handler))

    dp.add_handler(PollHandler(poll_handler, pass_chat_data = True, pass_user_data = True))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
