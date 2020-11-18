import os
import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from quiz_helper import get_quiz_data, check_is_right_answer
from redis_helper import RedisHelper

REDIS_DB = RedisHelper().connection

DB_USER_PREFIX = "vk-"

QUIZ_DATA = get_quiz_data()


def echo(event, vk_api):
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        if event.text == "Начать":
            vk_api.messages.send(
                user_id=event.user_id,
                message="Привет, я бот для викторин!",
                keyboard=keyboard.get_keyboard(),
                random_id=random.randint(1, 1000)
            )
        elif event.text == "Сдаться":
            user_question = REDIS_DB.get(event.user_id)
            right_answer = QUIZ_DATA.get(user_question)
            vk_api.messages.send(
                user_id=event.user_id,
                message=right_answer,
                keyboard=keyboard.get_keyboard(),
                random_id=random.randint(1, 1000)
            )
        elif event.text == "Новый вопрос":
            question = random.choice(list(QUIZ_DATA.keys()))
            REDIS_DB.set(f"{DB_USER_PREFIX}{event.user_id}", question)
            vk_api.messages.send(
                user_id=event.user_id,
                message=question,
                keyboard=keyboard.get_keyboard(),
                random_id=random.randint(1, 1000)
            )
        else:
            user_question = REDIS_DB.get(event.user_id)
            user_answer = event.text
            if check_is_right_answer(QUIZ_DATA, user_question, user_answer):
                vk_api.messages.send(
                    user_id=event.user_id,
                    message="Правильный ответ!",
                    keyboard=keyboard.get_keyboard(),
                    random_id=random.randint(1, 1000)
                )
            else:
                vk_api.messages.send(
                    user_id=event.user_id,
                    message="Неравильный ответ!",
                    keyboard=keyboard.get_keyboard(),
                    random_id=random.randint(1, 1000)
                )


if __name__ == "__main__":

    vk_session = vk_api.VkApi(token=os.getenv("VK_TOKEN_QUIZ_BOT"))
    vk_api = vk_session.get_api()

    keyboard = VkKeyboard()

    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)

    keyboard.add_line()
    keyboard.add_button('Мой счет', color=VkKeyboardColor.POSITIVE)

    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)
