from sys import exit
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from creds import token
from database import *
from schedule import *
from web import *

bot = TeleBot(token=token, parse_mode="HTML")

groups = get_groups()
if groups[0] == ERROR_DATABASE:
    print("Error getting groups!")
    exit(1)
else:
    groups = groups[1]

def register(telegram_id: int):
    buttons = InlineKeyboardMarkup()
    text = "Выберите группу из списка:"

    for group in groups:
        buttons.add(InlineKeyboardButton(text=group[1], callback_data="add_"+str(group[0])))

    bot.send_message(chat_id=telegram_id, text=text, reply_markup=buttons)

def week_schedule(telegram_id: int, message_id: int):
    buttons = InlineKeyboardMarkup()
    group_id = get_user_group_id(telegram_id)
    buttons.add(InlineKeyboardButton(text="День с заменами", callback_data="zamena"))

    if group_id[0] == ERROR_DATABASE:
        bot.edit_message_text(chat_id=telegram_id, text="Что-то пошло не так...", message_id=message_id)
    else:
        group_id = group_id[1]
        text = get_week_schedule_text(group_id)
        bot.edit_message_text(chat_id=telegram_id, text=text, message_id=message_id, reply_markup=buttons)

def day_schedule(telegram_id: int, message_id: int):
    buttons = InlineKeyboardMarkup()
    group_id = get_user_group_id(telegram_id)
    buttons.add(InlineKeyboardButton(text="Неделя", callback_data="week"))

    if group_id[0] == ERROR_DATABASE:
        bot.edit_message_text(chat_id=telegram_id, text="Что-то пошло не так...", message_id=message_id)
    else:
        group_id = group_id[1]
        text = get_changed_day_text(group_id)
        bot.edit_message_text(chat_id=telegram_id, text=text, message_id=message_id, reply_markup=buttons)

@bot.message_handler(commands=["start"])
def start(msg: Message):
    telegram_id = msg.from_user.id

    user_exists = check_user_existence(telegram_id)
    if user_exists[0] == ERROR_DATABASE:
        bot.send_message(chat_id=telegram_id, text="Произошла ошибка")
        return
    else: user_exists = user_exists[1]

    if not user_exists:
        register(telegram_id)

@bot.message_handler(commands=["reset"])
def reset(msg: Message):
    telegram_id = msg.from_user.id

    user_exists = check_user_existence(telegram_id)
    if user_exists[0] == ERROR_DATABASE:
        bot.send_message(chat_id=telegram_id, text="Произошла ошибка")
        return
    else: user_exists = user_exists[1]

    if user_exists:
        if delete_user(telegram_id) == ERROR_DATABASE:
            bot.send_message(chat_id=telegram_id, text="Произошла ошибка")
            return
        bot.send_message(chat_id=telegram_id, text="Вы были удалены из базы данных. Для продолжения введите /start")
    else:
        bot.send_message(chat_id=telegram_id, text="Вы не в базе данных")

@bot.callback_query_handler()
def handle_callbacks(call: CallbackQuery):
    telegram_id = call.from_user.id
    message_id = call.message.id
    data = call.data

    if data.startswith("add_"):
        user_exists = check_user_existence(telegram_id)
        if user_exists[0] == ERROR_DATABASE:
            bot.edit_message_text(chat_id=telegram_id, text="Что-то пошло не так...", message_id=message_id)
        else: user_exists = user_exists[1]

        if not user_exists:
            # TODO: if week_schedule fails, nothing gets displayed, but user gets in the database
            add_user(telegram_id, int(call.data.split('_')[1]))
            week_schedule(telegram_id, message_id)
            bot.answer_callback_query(call.id)
        else:
            bot.edit_message_text(chat_id=telegram_id, text="Вы уже в базе данных", message_id=message_id)
            bot.answer_callback_query(call.id)
    elif data == "week":
        week_schedule(telegram_id, message_id)
        bot.answer_callback_query(call.id)
    elif data == "zamena":
        day_schedule(telegram_id, message_id)
        bot.answer_callback_query(call.id)

bot.infinity_polling()
