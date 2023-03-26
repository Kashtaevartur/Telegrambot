import telebot
import requests
import os
import json

with open('cities.json', 'r') as f:
    data = json.load(f)

names = []
for city in data['city']:
    city_id = city['city_id']
    country_id = city['country_id']
    region_id = city['region_id']
    name = city['name']
    names.append(name)



#TOKEN = '6247166648:AAFszyev0r03NLcvcrgZOpwsT-KwwQMAyzQ'
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Привет!
Я бот который поиграет с тобой в города
но я знаютолько русский язык(
С тебя первый город')
Поехали... \
""")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    word = message.text

    if word[0].islower():
        word = word.capitalize()

    stripped_word = word.rstrip(',. ')
    if stripped_word in names:
        last_leter = stripped_word[-1]
        for name in names:
            if name.startswith(last_leter.upper()):
                bot.reply_to(message, {names})
                exit()


    else:
        bot.reply_to(message, "Такого города нет")


bot.infinity_polling()

