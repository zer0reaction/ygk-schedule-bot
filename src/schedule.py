import json
from database import get_user_group_id, get_group_row
from datetime import datetime
from constants import *

# Returns formatted text for one day (without day name)
def get_day_schedule_text(week_dict: dict, week_day: str, week_type: str) -> str:
    text = ""
    day_dict = week_dict[week_day][week_type]
    emojis = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

    for day_key in day_dict.keys():
        text += emojis[int(day_key)]
        text += " <b>{}</b> ".format(day_dict[day_key][2])
        text += "<i>{}</i> ".format(day_dict[day_key][0])
        text += "{}".format(day_dict[day_key][1])
        text += '\n'

    return text

# Returns formatted text of constant schedule
def get_week_schedule_text(group_id: int, week_type: str) -> str:
    data = get_group_row(group_id)
    if data[0] == ERROR_DATABASE:
        return "Что-то пошло не так..."

    filename = data[1][2]

    week_dict = []
    with open("./db/groups/" + filename, "r") as json_file:
        week_dict = json.load(json_file)

    text = ""

    if week_type == "ch":
        text += "<b>Числитель\n\n</b>"
    elif week_type == "zn":
        text += "<b>Знаменатель\n\n</b>"

    text += "Понедельник\n" + get_day_schedule_text(week_dict, "mon", week_type) + '\n'
    text += "Вторник\n" + get_day_schedule_text(week_dict, "tue", week_type) + '\n'
    text += "Среда\n" + get_day_schedule_text(week_dict, "wed", week_type) + '\n'
    text += "Четверг\n" + get_day_schedule_text(week_dict, "thu", week_type) + '\n'
    text += "Пятница\n" + get_day_schedule_text(week_dict, "fri", week_type) + '\n'
    text += "Суббота\n" + get_day_schedule_text(week_dict, "sat", week_type)

    return text

def get_changed_day_text(date: datetime, week_dict: dict, week_type: str) -> str:
    day_name = ""

    match date.weekday():
        case 0: day_name = "mon"
        case 1: day_name = "tue"
        case 2: day_name = "wed"
        case 3: day_name = "thu"
        case 4: day_name = "fri"
        case 5: day_name = "sat"

    day_dict = week_dict[day_name][week_type]
