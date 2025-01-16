from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from creds import token
from database import *
from schedule import *
from web import *

bot = TeleBot(token=token, parse_mode="HTML")
groups = get_groups()

def register(telegram_id: int):
    buttons = InlineKeyboardMarkup()
    text = "Выберите группу из списка:"

    for group in groups:
        buttons.add(InlineKeyboardButton(text=group[1], callback_data="add_"+str(group[0])))

    bot.send_message(chat_id=telegram_id, text=text, reply_markup=buttons)

def week_schedule(telegram_id: int, message_id: int):
    buttons = InlineKeyboardMarkup()
    week_type = get_web_ch_zn(get_html_text())
    text = get_week_schedule_text(get_user_group_id(telegram_id), groups, week_type)

    buttons.add(InlineKeyboardButton(text="День с заменой", callback_data="zamena"))

    bot.edit_message_text(chat_id=telegram_id, text=text, message_id=message_id, reply_markup=buttons)

def day_schedule(telegram_id: int, message_id: int):
    buttons = InlineKeyboardMarkup()

    html_text=get_html_text()
    data = get_all_data(html_text)
    text = get_day_zamena_text(telegram_id, data, get_web_date(html_text))

    buttons.add(InlineKeyboardButton(text="Неделя", callback_data="week"))
    
    bot.edit_message_text(chat_id=telegram_id, text=text, message_id=message_id, reply_markup=buttons)

@bot.message_handler(commands=["start"])
def start(msg: Message):
    telegram_id = msg.from_user.id
    user_exists = check_user_existence(telegram_id)

    if not user_exists:
        register(telegram_id)

@bot.message_handler(commands=["reset"])
def reset(msg: Message):
    telegram_id = msg.from_user.id
    user_exists = check_user_existence(telegram_id)

    if user_exists:
        delete_user(telegram_id)
        bot.send_message(chat_id=telegram_id, text="Вы были удалены из базы данных")
    else:
        bot.send_message(chat_id=telegram_id, text="Вы не в базе данных")

@bot.callback_query_handler()
def handle_callbacks(call: CallbackQuery):
    telegram_id = call.from_user.id
    message_id = call.message.id
    data = call.data

    if data.startswith("add_"):
        group_id = data.split('_')[1]
        add_user(telegram_id, group_id)
        week_schedule(telegram_id, message_id)
        bot.answer_callback_query(call.id)
    elif data == "week":
        week_schedule(telegram_id, message_id)
        bot.answer_callback_query(call.id)
    elif data == "zamena":
        day_schedule(telegram_id, message_id)
        bot.answer_callback_query(call.id)

bot.infinity_polling()
