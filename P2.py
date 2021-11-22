import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Poll
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, PollHandler
import time
import random


questions = [
    [
        '¿Como se puede saber si una rama ya se le ha hecho un merge a master mediante comandos de línea?',
        ['git branch --merged / --unmerged', 'git status', 'git log --inline branch status'],
        [0],
        ['git branch --merged / --unmerged']
    ],
    [
        'De las siguientes opciones, ¿Cuál o cuales contiene un objeto tipo commit? Seleccione 2',
        ['Un identificador único de 40 carácteres', 'Referencia a los commits hijos',
         'Un conjunto de archivos como estado del proyecto'],
        [0, 2],
        ['Un identificador único de 40 carácteres', 'Un conjunto de archivos como estado del proyecto']
    ],
    [
        '¿Qué comando se emplea para estipular el email del usuario actual que usará git?',
        ['git user set --email=""', 'git add user.email', 'git config -global user.email'],
        [2],
        ['git config -global user.email']
    ],
    [
        '¿Qué función realiza el comando clone de git?',
        ['Copia un commit a una nueva rama', 'Realiza una copia local del respositorio', 'Crea un nuevo repositorio'],
        [1],
        ['Realiza una copia local del respositorio']
    ],
    [
        '¿Cuál es la forma correcta de crear un nuevo tag en un commit?',
        ['git new-tag [nombre] [commit]', 'git tag [commitID]', 'git tag -l [nombre]'],
        [1], ['Realiza una copia local del respositorio']
    ],
    ['6', ['water', 'ice', 'wine'], [0, 2], 'wine'],
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
    add_text_message(update, context, f"Pregunta {count + 1} de 6")
    quizz_question = random.choice(questions)
    while quizz_question in ya_preguntadas:
        quizz_question = random.choice(questions)
    count += 1
    print(f'Pregunta N°{count}')
    ya_preguntadas.append(quizz_question)
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
    global count, ya_preguntadas, correct_answers
    print(f"question : {update.poll.question}")
    print(f"correct option : {update.poll.correct_option_id}")
    print(f"option #1 : {update.poll.options[0]}")
    print(f"option #2 : {update.poll.options[1]}")
    print(f"option #3 : {update.poll.options[2]}")

    if update.poll.allows_multiple_answers:
        print(f'Permite respuesta multiple')
        answers = update.poll.options
        contestadas = []
        for answer in answers:
            if answer.voter_count == 1:
                contestadas.append(answer.text)

        print(ya_preguntadas[count - 1][3])
        print(contestadas)
        correctas_question = 0
        for contestada in contestadas:
            if contestada in ya_preguntadas[count - 1][3]:
                correctas_question += 1
        add_typing(update, context)
        if correctas_question == 2:
            add_text_message(update, context, f"Respuesta correcta al completo.")
            correct_answers += 1
        elif correctas_question == 1:
            add_text_message(update, context, f"1 de 2 seleccionadas es correcta.")
            correct_answers += 0.5
        else:
            add_text_message(update, context, f"Respuesta incorrecta")
    else:
        user_answer = get_answer(update)
        print(f'Respuesta: {user_answer}')
        add_typing(update, context)
        if is_answer_correct(update):
            add_text_message(update, context, f"Respuesta correcta")
            correct_answers += 1
        else:
            add_text_message(update, context, f"Respuesta incorrecta")

    if count == 6:
        add_text_message(update, context, f"Tu nota final corresponde a {correct_answers + 1}")
        count = 0
        correct_answers = 0
        ya_preguntadas = []
    else:
        start_handler(update, context)


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
