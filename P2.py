import random
import time

import telegram
from telegram import Poll
from telegram.ext import Updater, CommandHandler, PollHandler

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
        [1],
        ['Realiza una copia local del respositorio']
    ],
    [
        '¿Cómo puedes arreglar un commit realizado de forma errónea?',
        ['Con git commit --fix', 'Con git commit --edit [nuevo mensaje]', 'Con git commit --ammend'],
        [2],
        ['Con git commit --ammend']
    ],
    [
        'Git es un sistema de control de versiones de tipo:',
        ['Distribuido', 'Localizado', 'Centralizado'],
        [0],
        ['Distribuido']
    ],
    [
        '¿Dónde se encuentran en git los archivos a los que se le puede realizar commit?',
        ['En el directorio de trabajo', 'En el área de stage indexados', 'No hay barrera de donde pueden encontrarse'],
        [1],
        ['En el área de stage indexados']
    ],
    [
        '¿Cuál de los siguientes corresponde a un enunciado falso sobre git?',
        ['La operación pull copia los cambios desde un repositorio local a uno remoto',
         'Por default, git tiene una rama master o main',
         'Git necesita de acceso a Internet solo cuando debe publicar u obtener datos de algun repositorio'],
        [0],
        ['La operación pull copia los cambios desde un repositorio local a uno remoto']
    ],
    [
        '¿Qué Git Hook sería más adecuado emplear para corroborar que los tests se encuentran funcionando bien a pesar '
        'de los cambios?',
        ['Pre-push',
         'Pre-commit',
         'Pre-receive'],
        [1],
        ['Pre-commit']
    ],
    [
        'Si deseo copiar un repositorio sin afectar el repositorio original, debo realizar un...',
        ['git clone',
         'git init',
         'git fork'],
        [2],
        ['git fork']
    ],
    [
        '¿Cualés de los siguientes son posibles usos de git cherry pick? Seleccione 2 alternativas',
        ['Introducir un commit en particular en una rama dentro del repositorio a otra rama',
         'Traerse commits específicos de una rama de mantenimiento o sin uso a una rama de desarrollo',
         'Trasladar de a poco todos los commits de otra rama a la actual'],
        [0, 1],
        ['Introducir un commit en particular en una rama dentro del repositorio a otra rama',
         'Traerse commits específicos de una rama de mantenimiento o sin uso a una rama de desarrollo']
    ]
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
