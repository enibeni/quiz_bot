import os
import re


def get_quiz_data():
    files_data = ""
    for dirpath, dirnames, files in os.walk('questions'):
        for file_name in files:
            with open(f"{dirpath}/{file_name}", "r", encoding="KOI8-R") as file:
                files_data = files_data + file.read()
    questions = []
    answers = []
    data_chunks = files_data.split('\n\n')
    for chunk in data_chunks:
        if "Вопрос " in chunk:
            question = "\n".join(chunk.split("\n")[1:])
            questions.append(question)
        elif "Ответ:" in chunk:
            answer = chunk.split("\n")[1]
            answers.append(answer)

    quiz_data = dict(zip(questions, answers))
    return quiz_data


def check_is_right_answer(qna, user_question, user_answer):
    user_answer = user_answer.lower().strip('.')
    right_answer = qna.get(user_question)
    right_answer = re.split(r'\.|\(|\[', right_answer)
    right_answer = right_answer[0].lower().strip()
    return user_answer == right_answer

