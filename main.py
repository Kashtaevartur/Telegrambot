import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os
import json
import random

with open('cities.json', 'r') as f:
    data = json.load(f)


names1 = []
for city in data['city']:
    city_id = city['city_id']
    country_id = city['country_id']
    region_id = city['region_id']
    name = city['name']
    names1.append(name)


#TOKEN = '6247166648:AAFszyev0r03NLcvcrgZOpwsT-KwwQMAyzQ'
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

# Создаем клавиатуру с одной кнопкой
button_text = 'Попробуй заново'
button = KeyboardButton(button_text)
keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button)

# Отправляем сообщение с клавиатурой
# message_text = 'Игра началась'
# bot.send_message(chat_id=bot.get_updates()[-1].message.chat.id, text=message_text, reply_markup=keyboard)
def reset():
    global names_old
    names_old = [1111, 1111]

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    reset()
    bot.reply_to(message, """\
Привет!
Я бот который поиграет с тобой в города
но я знаю только русский язык(
С тебя первый город:'
Поехали... \
""")


names_old = [1111, 1111]



@bot.message_handler(func=lambda message: True)
def echo_message(message):
    names = names1.copy()
    random.shuffle(names)

    word = str(message.text)

    if word[0].islower():
        word = word.capitalize()
    stripped_word = word.rstrip(',. ')
    is_non_russian_letter = True
    for char in stripped_word:
        if ord('а') <= ord(char) <= ord('я') or ord('А') <= ord(char) <= ord('Я') or char == ' ' or char == '-' or char == 'ё':
            continue
        else:
            bot.reply_to(message, "Введите город на русском языке", reply_markup=keyboard)
            return

    if len(names_old) <= 2:
        if word == 'лошара':
            reset()
            bot.reply_to(message, "Ok, давай сначала)\nПиши город:", reply_markup=keyboard)
            return
        if stripped_word in names:
            if stripped_word not in names_old:
                names_old.append(stripped_word)
                last_leter1 = str(names_old[-1])[-1]
                if last_leter1 == 'ь' or last_leter1 == 'ъ' or last_leter1 == 'ы':
                    last_leter1 = str(names_old[-1])[-2]
                for name in names:
                    if name not in names_old:
                        if name.startswith(last_leter1.upper()):
                            bot.reply_to(message, {name}, reply_markup=keyboard)
                            names_old.append(name)
                            return


                else:
                    bot.reply_to(message, f"Не жульничай, город {stripped_word} уже был, давай другой город на букву '{str(names_old[-1])[-1].upper()}'", reply_markup=keyboard)
                    return
        else:
            bot.reply_to(message, "Такого города нет", reply_markup=keyboard)
            return
    else:
        if word == 'Попробуй заново':
            reset()
            bot.reply_to(message, "Ok, давай сначала)\nПиши город:", reply_markup=keyboard)
            return

        if str(names_old[-1])[-1] == 'ь' or str(names_old[-1])[-1] == 'ъ' or str(names_old[-1])[-1] == 'ы':
            if stripped_word.startswith(str(names_old[-1])[-2].upper()):
                # добавляем в массив использованных слов
                if stripped_word in names:
                    if stripped_word not in names_old:
                        names_old.append(stripped_word)
                        last_leter = str(names_old[-1])[-1]
                        if last_leter == 'ь' or last_leter == 'ъ' or last_leter == 'ы':
                            last_leter = str(names_old[-1])[-2]
                        for name in names:
                            if name not in names_old:
                                if name.startswith(last_leter.upper()):
                                    bot.reply_to(message, {name}, reply_markup=keyboard)
                                    names_old.append(name)
                                    return


                    else:
                        bot.reply_to(message,
                                     f"Не жульничай, город {stripped_word} уже был, давай другой город на букву '{str(names_old[-1])[-1].upper()}'", reply_markup=keyboard)
                        return
                else:
                    bot.reply_to(message, "Такого города нет", reply_markup=keyboard)
                    return
            else:
                bot.reply_to(message, f"Тебе нужно написать город на букву '{str(names_old[-1])[-2].upper()}'", reply_markup=keyboard)

        else:
            if stripped_word.startswith(str(names_old[-1])[-1].upper()):
                # добавляем в массив использованных слов
                if stripped_word in names:
                    if stripped_word not in names_old:
                        names_old.append(stripped_word)
                        last_leter = str(names_old[-1])[-1]
                        if last_leter == 'ь' or last_leter == 'ъ' or last_leter == 'ы':
                            last_leter = str(names_old[-1])[-2]
                        for name in names:
                            if name not in names_old:
                                if name.startswith(last_leter.upper()):
                                    bot.reply_to(message, {name}, reply_markup=keyboard)
                                    names_old.append(name)
                                    return


                    else:
                        bot.reply_to(message,
                                     f"Не жульничай, город {stripped_word} уже был, давай другой город на букву '{str(names_old[-1])[-1].upper()}'",
                                     reply_markup=keyboard)
                        return
                else:
                    bot.reply_to(message, "Такого города нет", reply_markup=keyboard)
                    return
            else:
                bot.reply_to(message, f"Тебе нужно написать слово на букву '{str(names_old[-1])[-1].upper()}'",
                             reply_markup=keyboard)

bot.infinity_polling()
