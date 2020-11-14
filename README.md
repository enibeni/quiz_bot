# Quiz bot
Create your own quizzes with this quiz bot.

### How to install
To use this script you should provide certain keys as environment variables in the .env file.
The keys you need to provide:
- VK_TOKEN_QUIZ_BOT - vk bot api key
- TG_TOKEN_QUIZ_BOT - telegram bot api key
- REDIS_DB_HOST - redis url endpoint
- REDIS_DB_PORT - redis url port
- REDIS_DB_PASSWORD - redis db password

to get REDIS credential create redis account on https://redislabs.com/

Python3 should be already installed.
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

# Quickstart

run telegram bot:
```bash
$ python3 tg_bot.py
```

run vk bot:
```bash
$ python3 vk_bot.py
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).