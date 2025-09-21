import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime
import os
import json
import csv
import random

# Глобальные переменные
names_old = []
first_turn = True  # Инициализация переменной

# Функция для логирования информации о пользователе и его запросах
def log_user_interaction(user_id, user_name, username, message_text):
    file_exists = os.path.isfile('user_logs.csv')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Текущая дата и время

    with open('user_logs.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['User ID', 'Name', 'Username', 'Message', 'Date and Time'])
        writer.writerow([user_id, user_name, username, message_text, current_time])

# Чтение списка городов
with open('cities_ua.json', 'r') as f:
    data = json.load(f)

names1 = [city['name'] for city in data['city']]

def read_file(file_name):
    with open(file_name, 'r') as file:
        return file.read()

# Чтение токена бота
TOKEN = read_file('token.txt')
bot = telebot.TeleBot(TOKEN)

# Создаем клавиатуру с одной кнопкой
button = KeyboardButton('🔄 Спробуй заново')
button1 = KeyboardButton('💡 Підказка')
keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button, button1)

# Функция для сброса использованных городов
def reset():
    global names_old, first_turn
    names_old = []
    first_turn = True

# Обработчик команды /start и /help
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    reset()
    user = message.from_user
    username = user.username if user.username else 'Не вказан'
    log_user_interaction(user.id, user.first_name, username, '/start')  # Логирование при старте
    bot.reply_to(message, "Вітаю!\nЯ бот, який пограє з тобою у міста.\nЗ тебе перше місто: Поїхали...")

# Основной обработчик сообщений
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    global first_turn, names_old

    names = names1.copy()
    random.shuffle(names)

    word = str(message.text)
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    username = message.from_user.username if message.from_user.username else 'Не вказан'

    # Логирование каждого сообщения пользователя
    log_user_interaction(user_id, user_name, username, word)



    if word[0].islower():
        word = word.capitalize()
    stripped_word = word.rstrip(',. ')

    # Проверка на использование украинских букв и игнорирование эмодзи
    allowed_characters = ' абвгґдеєжзиіїйклмнопрстуфхцчшщьюяАБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ\'-'

    # Добавляем эмодзи, которые нужно игнорировать
    allowed_characters += '💡🔄'

    if not all(char in allowed_characters for char in stripped_word):
        bot.reply_to(message, "Ти взагалі на якій мові розмовляєш? Пиши українською!", reply_markup=keyboard)
        return

    # Логика игры в города
    if first_turn:
        if word == '🔄 Спробуй заново':
            reset()
            bot.reply_to(message, "Ok, давай спочатку)\nПиши місто:", reply_markup=keyboard)
            return

        if word == '💡 Підказка':
            bot.reply_to(message, "Напиши яке-небудь місто українською", reply_markup=keyboard)
            return
        if stripped_word in names:
            names_old.append(stripped_word)
            if stripped_word[-1] in 'ьґjarиudkbgl)s':
                last_letter = stripped_word[-2]
            else:
                last_letter = stripped_word[-1]
            i = 0

            while i < len(names):  # Проходим по списку городов
                if names[i][0] == last_letter.upper():  # Проверяем первую букву города
                    bot.reply_to(message, names[i], reply_markup=keyboard)
                    names_old.append(names[i])
                    first_turn = False
                    break  # Если совпадение найдено, завершаем цикл
                i += 1  # Переходим к следующему городу

            # for name in names:
            #     bot.reply_to(message, name, reply_markup=keyboard)
            #     names_old.append(name)
            #     first_turn = False
            #     return
        else:
            bot.reply_to(message, f"Дітька лисого а не {stripped_word} давай щось реальне", reply_markup=keyboard)
            return
    else:

        last_letter = names_old[-1][-1]
        if last_letter in 'ьґjarиudkbgl)s':
            last_letter = names_old[-1][-2]

        if word == '🔄 Спробуй заново':
            reset()
            bot.reply_to(message, "Ok, давай спочатку)\nПиши місто:", reply_markup=keyboard)
            return

        if word == '💡 Підказка':
            if last_letter in 'ьґjaruиdkbgl)s':
                last_letter = stripped_word[-2]
                for name in names:
                    if name not in names_old and name.startswith(last_letter.upper()):
                        bot.reply_to(message, name, reply_markup=keyboard)
                        return
            else:
                for name in names:
                    if name not in names_old and name.startswith(last_letter.upper()):
                        bot.reply_to(message, name, reply_markup=keyboard)
                        return

        if stripped_word in names_old:
            bot.reply_to(message, f"Ти хочеш намахати мене, місто {stripped_word} вже було, напиши інше на букву '{last_letter.upper()}'", reply_markup=keyboard)
            return

        if stripped_word.startswith(last_letter.upper()):
            if stripped_word in names and stripped_word not in names_old:
                names_old.append(stripped_word)
                last_letter = stripped_word[-1]
                if last_letter in 'ьґjarиudkbgl)s':
                    last_letter = stripped_word[-2]
                for name in names:
                    if name not in names_old and name.startswith(last_letter.upper()):
                        bot.reply_to(message, name, reply_markup=keyboard)
                        names_old.append(name)
                        return
            else:
                if stripped_word in names_old:
                    bot.reply_to(message, f"Ти хочеш намахати мене, місто {stripped_word} вже було, напиши інше на букву '{last_letter.upper()}'", reply_markup=keyboard)
                    return
                if stripped_word not in names:
                    bot.reply_to(message, f"Дітька лисого а не {stripped_word} давай щось реальне", reply_markup=keyboard)
                    return
        else:
            bot.reply_to(message, f"Що ти там тицяєш? Пиши місто на букву '{last_letter.upper()}'", reply_markup=keyboard)

bot.infinity_polling()
