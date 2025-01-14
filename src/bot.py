from telebot import TeleBot
from telebot.types import InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from creds import token
from database import *
from web import *
from schedule import *

bot = TeleBot(token=token, parse_mode="HTML")
groups = get_groups()

group_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
for group in groups:
    group_buttons.add(InlineKeyboardButton(group[1]))

greeting_text="Выберите группу из списка:\n\nНИКАКОЙ ГАРАНТИИ ПРАВИЛЬНОСТИ ДАННЫХ И РАБОТОСПОСОБНОСТИ БОТА НЕ ПРЕДОСТАВЛЯЕТСЯ"
user_already_in_db_text="Вы уже в базе данных.\nИспользуйте /reset для сброса данных о себе"
user_successfully_added_text="Вы были успешно удалены из базы данных. Для продожения введите /start"
user_not_in_db_text="Вы не в базе данных"

# @TODO
def send_current_schedule(id: int):
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(InlineKeyboardButton(text="Расписание"))
    return bot.send_message(chat_id=id, text="placeholder", reply_markup=markup).id

@bot.message_handler(commands=["start"])
def start(message):
    id = message.from_user.id

    if check_user_existence(id): send_current_schedule(id)
    else: bot.send_message(chat_id=id, text=greeting_text, reply_markup=group_buttons)

@bot.message_handler(commands=["reset"])
def reset(message):
    id = message.from_user.id

    if check_user_existence(id):
        delete_user(id)
        bot.send_message(chat_id=id, text=user_successfully_added_text,
                         reply_markup=ReplyKeyboardRemove())
    else: bot.send_message(chat_id=id, text=user_not_in_db_text)

@bot.message_handler()
def message_handler(message):
    id = message.from_user.id
    text = message.text

    if text == "Расписание" and check_user_existence(id):
        send_current_schedule(id)
    else:
        for group in groups:
            if text == group[1]:
                add_user(id, group[0])
                send_current_schedule(id)

bot.infinity_polling()
