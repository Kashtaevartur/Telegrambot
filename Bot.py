from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import json

# Настраиваем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Функция для сохранения данных о пользователях
def log_user_data(update: Update, context):
    user = update.message.from_user
    user_data = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "message": update.message.text,
        "date": str(update.message.date)
    }
    
    # Записываем данные в файл
    with open("user_data.json", "a") as f:
        f.write(json.dumps(user_data) + "\n")
    
    # Ответ бота
    update.message.reply_text(f"Привет, {user.first_name}!")

# Основная функция запуска бота
def main():
    # Вставь свой токен сюда
    bot_token = 'YOUR_BOT_TOKEN'
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    # Обработчик сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, log_user_data))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
