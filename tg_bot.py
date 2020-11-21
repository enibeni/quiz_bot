import os
import json
from enum import Enum
from random import choice
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from quiz_helper import get_quiz_data, check_is_right_answer
from redis_helper import RedisHelper

REPLY_MARKUP = ReplyKeyboardMarkup(
    [['Новый вопрос', 'Сдаться'],
     ['Мой счет']]
)

DB_USER_PREFIX = "tg-"

QUIZ_DATA = get_quiz_data()


class States(Enum):
    QUESTION = 1
    ANSWER = 2
    KAPITULATION = 3


def start(bot, update):
    update.message.reply_text('Привет, я бот для викторин!', reply_markup=REPLY_MARKUP)
    return States.QUESTION


def handle_new_question_request(bot, update):
    question, answer = choice(list(QUIZ_DATA.items()))
    REDIS_DB.set(f"{DB_USER_PREFIX}{update.message.chat_id}", json.dumps({question: answer}))
    update.message.reply_text(text=question, reply_markup=REPLY_MARKUP)
    return States.ANSWER


def handle_solution_attempt(bot, update):
    db_quiz_data = json.loads(REDIS_DB.get(f"{DB_USER_PREFIX}{update.message.chat_id}"))
    for item in db_quiz_data.items():
        _, right_answer = item
    user_answer = update.message.text
    if check_is_right_answer(right_answer, user_answer):
        update.message.reply_text(text="Правильный ответ!", reply_markup=REPLY_MARKUP)
    else:
        update.message.reply_text(text="Неправильный ответ!", reply_markup=REPLY_MARKUP)
    return States.QUESTION


def handle_kapitulation(bot, update):
    db_quiz_data = json.loads(REDIS_DB.get(f"{DB_USER_PREFIX}{update.message.chat_id}"))
    for item in db_quiz_data.items():
        _, right_answer = item
    update.message.reply_text(text=right_answer, reply_markup=REPLY_MARKUP)
    return States.QUESTION


def main():
    load_dotenv()
    global REDIS_DB
    REDIS_DB = RedisHelper().connection

    updater = Updater(os.getenv("TG_TOKEN_QUIZ_BOT"))
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            RegexHandler('^Новый вопрос$', handle_new_question_request)
        ],
        states={

            States.QUESTION: [RegexHandler('^Новый вопрос$', handle_new_question_request)],

            States.ANSWER: [
                RegexHandler('^Сдаться$', handle_kapitulation),
                MessageHandler(Filters.text, handle_solution_attempt)
            ],
        },

        fallbacks=[RegexHandler('^Сдаться$', handle_kapitulation)]
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
