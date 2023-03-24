import telebot
import requests
import os



#TOKEN = '6247166648:AAFszyev0r03NLcvcrgZOpwsT-KwwQMAyzQ'
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Привет!
Как тебя зовут?\
""")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, "Я знаю что ты Енот и тебе пора спать!!!!")




bot.infinity_polling()

