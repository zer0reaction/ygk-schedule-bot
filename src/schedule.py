import json
from database import get_user_group_id, get_group_row
from web import get_html_text, get_web_date, get_all_changes, get_web_week_type
from datetime import datetime
from constants import *

# Returns formatted text for one day (without day name)
def get_day_schedule_text(day_dict: dict) -> str:
    text = ""
    emojis = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

    for day_key in day_dict.keys():
        text += emojis[int(day_key)]
        text += " <b>{}</b> ".format(day_dict[day_key][2])
        text += "<i>{}</i> ".format(day_dict[day_key][0])
        text += "{}".format(day_dict[day_key][1])
        text += '\n'

    return text

# Returns formatted text of constant schedule
def get_week_schedule_text(group_id: int) -> str:
    filename = get_group_row(group_id)
    if filename[0] == ERROR_DATABASE:
        return "Что-то пошло не так..."
    else: filename = filename[1][2]

    week_dict = []
    with open("./db/groups/" + filename, "r") as json_file:
        week_dict = json.load(json_file)

    html_text = get_html_text()
    if html_text[0] == ERROR_WEB:
        return "Что-то пошло не так..."
    else: html_text = html_text[1]

    text = ""
    week_type = get_web_week_type(html_text)

    if week_type == "ch":
        text += "<b>Числитель</b>\n\n"
    elif week_type == "zn":
        text += "<b>Знаменатель</b>\n\n"

    text += "Понедельник\n" + get_day_schedule_text(week_dict["mon"][week_type]) + '\n'
    text += "Вторник\n" +     get_day_schedule_text(week_dict["tue"][week_type]) + '\n'
    text += "Среда\n" +       get_day_schedule_text(week_dict["wed"][week_type]) + '\n'
    text += "Четверг\n" +     get_day_schedule_text(week_dict["thu"][week_type]) + '\n'
    text += "Пятница\n" +     get_day_schedule_text(week_dict["fri"][week_type]) + '\n'
    text += "Суббота\n" +     get_day_schedule_text(week_dict["sat"][week_type])

    return text

def get_changed_day_text(group_id: int) -> str:
    html_text = get_html_text()
    if html_text[0] == ERROR_WEB:
        return "Что-то пошло не так..."
    else: html_text = html_text[1]

    date = get_web_date(html_text)
    changes = get_all_changes(html_text)
    week_type = get_web_week_type(html_text)

    group_row = get_group_row(group_id)
    if group_row[0] == ERROR_DATABASE:
        return "Что-то пошло не так..."
    group_row = group_row[1]

    week_dict = []
    with open("./db/groups/" + group_row[2], "r") as json_file:
        week_dict = json.load(json_file)

    day_name = ""
    match date.weekday():
        case 0: day_name = "mon"
        case 1: day_name = "tue"
        case 2: day_name = "wed"
        case 3: day_name = "thu"
        case 4: day_name = "fri"
        case 5: day_name = "sat"

    if day_name == "":
        return "Что-то пошло не так..."

    day_dict = week_dict[day_name][week_type]

    for change in changes:
        if change["group_name"] == group_row[1]:
            pairs_string = change["pair_number"]
            pair_numbers = []

            if ',' in pairs_string:
                pair_numbers = pairs_string.split(',')
            elif '-' in pairs_string:
                split = pairs_string.split('-')
                for i in range(int(split[0]), int(split[1]) + 1):
                    pair_numbers.append(str(i))
            else:
                pair_numbers.append(pairs_string)

            for pair_number in pair_numbers:
                try:
                    day_dict[pair_number][0] = change["changed_to"]
                    day_dict[pair_number][1] = "⚠️ЗАМЕНА⚠️"
                    day_dict[pair_number][2] = change["classroom"]
                except:
                    return "Что-то пошло не так..."


    return get_day_schedule_text(day_dict)
