from telebot import TeleBot
from telebot.types import InlineKeyboardButton, ReplyKeyboardMarkup
from creds import token
from web import *
from database import *

# initializing some important variables
bot = TeleBot(token=token, parse_mode="HTML")
groups = get_groups()

buttons = ReplyKeyboardMarkup(resize_keyboard=True)
for group in groups:
    #                                group_name 
    buttons.add(InlineKeyboardButton(group[1]))

greeting_text="Выберите группу из списка:\n\nНИКАКОЙ ГАРАНТИИ ПРАВИЛЬНОСТИ ДАННЫХ И РАБОТОСПОСОБНОСТИ БОТА НЕ ПРЕДОСТАВЛЯЕТСЯ"
user_already_in_db_text="Вы уже в базе данных.\nИспользуйте /reset для сброса данных о себе"
# -------------------------------------


def send_current_schedule(id: int):
    markup=InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Расписание", callback_data="schedule"))
    return bot.send_message(chat_id=id, text="placeholder", reply_markup=markup).id


@bot.message_handler(commands=["start"])
def start(message):
    id = message.from_user.id

    if check_user_existence(id):
        send_current_schedule(id)
    else:
        bot.send_message(chat_id=id, text=greeting_text, reply_markup=buttons)


@bot.message_handler(commands=["reset"])
def reset(message):
    id = message.from_user.id

    if check_user_existence(id):
        delete_user(id)
        bot.send_message(chat_id=id, text="Вы были успешно удалены из базы данных. Для продожения введите /start")
    else:
        bot.send_message(chat_id=id, text="Вы не в базе данных")


bot.infinity_polling()