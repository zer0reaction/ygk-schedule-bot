from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from creds import token
from web import *
from database import *

bot = TeleBot(token=token, parse_mode="HTML")

@bot.message_handler(commands=["start"])
def start(message):
    id = message.from_user.id
    buttons = InlineKeyboardMarkup()
    groups = get_groups()

    for group in groups:
        buttons.add(InlineKeyboardButton(group[1],
                                         callback_data="useradd_{}_{}".format(id, group[0])))

    bot.send_message(chat_id=id, text="test", reply_markup=buttons)

bot.infinity_polling()
