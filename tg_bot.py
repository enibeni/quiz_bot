import os
from enum import Enum
from random import choice
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
import redis
from quiz_helper import get_quiz_data, check_is_right_answer


load_dotenv()

redis_db = redis.Redis(
        host=os.getenv("REDIS_DB_HOST"),
        port=os.getenv("REDIS_DB_PORT"),
        db=0,
        password=os.getenv("REDIS_DB_PASSWORD"),
        charset="KOI8-R",
        decode_responses=True,
)

custom_keyboard = [['Новый вопрос', 'Сдаться'],
                   ['Мой счет']]
reply_markup = ReplyKeyboardMarkup(custom_keyboard)

quiz_data = get_quiz_data()


class States(Enum):
    QUESTION = 1
    ANSWER = 2
    KAPITULATION = 3


def start(bot, update):
    update.message.reply_text('Привет, я бот для викторин!', reply_markup=reply_markup)
    return States.QUESTION


def handle_new_question_request(bot, update):
    question = choice(list(quiz_data.keys()))
    redis_db.set(update.message.chat_id, question)
    update.message.reply_text(text=question, reply_markup=reply_markup)
    return States.ANSWER


def handle_solution_attempt(bot, update):
    user_question = redis_db.get(update.message.chat_id)
    user_answer = update.message.text
    if check_is_right_answer(quiz_data, user_question, user_answer):
        update.message.reply_text(text="Правильный ответ!", reply_markup=reply_markup)
    else:
        update.message.reply_text(text="Неправильный ответ!", reply_markup=reply_markup)
    return States.QUESTION


def handle_kapitulation(bot, update):
    user_question = redis_db.get(update.message.chat_id)
    right_answer = quiz_data.get(user_question)
    update.message.reply_text(text=right_answer, reply_markup=reply_markup)
    return States.QUESTION


def main():
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
