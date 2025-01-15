from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from creds import token
from database import check_user_existence, get_groups, delete_user, add_user
from schedule import get_week_data, get_day_schedule_text

bot = TeleBot(token=token, parse_mode="HTML")
groups = get_groups()

def register(telegram_id: int):
    buttons = InlineKeyboardMarkup()
    text = "Выберите группу из списка:"

    for group in groups:
        buttons.add(InlineKeyboardButton(text=group[1], 
                                         callback_data="add_"+str(group[0])))

    bot.send_message(chat_id=telegram_id, text=text, reply_markup=buttons)

def send_schedule(telegram_id: int):
    buttons = InlineKeyboardMarkup()
    text = get_day_schedule_text(get_week_data(1, groups), "mon", "ch")
    buttons.add(
        InlineKeyboardButton(text="Числитель", callback_data="ch"),
        InlineKeyboardButton(text="Знаменатель", callback_data="zn"),
    )
    bot.send_message(chat_id=telegram_id, text=text, reply_markup=buttons)

def update_schedule(telegram_id: int, message_id: int):
    buttons = InlineKeyboardMarkup()
    text = get_day_schedule_text(get_week_data(1, groups), "mon", "ch")
    buttons.add(
        InlineKeyboardButton(text="Числитель", callback_data="ch"),
        InlineKeyboardButton(text="Знаменатель", callback_data="zn"),
    )
    bot.edit_message_text(chat_id=telegram_id, message_id=message_id, 
                          text=text, reply_markup=buttons)

@bot.message_handler(commands=["start"])
def start(msg: Message):
    telegram_id = msg.from_user.id
    user_exists = check_user_existence(telegram_id)

    if user_exists:
        send_schedule(telegram_id)
    else:
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
        update_schedule(telegram_id, message_id)

bot.infinity_polling()
