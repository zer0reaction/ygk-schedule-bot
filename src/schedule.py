import json
from database import get_user_group_id, get_group_row
from web import get_html_text_first, get_html_text_second, get_web_date, get_all_changes, get_web_week_type
from datetime import datetime
from constants import *

# Returns formatted text for one day (without day name)
def get_day_schedule_text(day_dict: dict) -> str:
    text = ""
    emojis = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']

    for day_key in day_dict.keys():
        text += emojis[int(day_key)]
        text += " <b>[{}]</b> ".format(day_dict[day_key][2])
        text += "<i>{}</i> ".format(day_dict[day_key][0])
        text += "({})".format(day_dict[day_key][1])
        text += '\n'

    return text

# Returns formatted text of constant schedule
def get_week_schedule_text(group_id: int) -> str:
    group_row = get_group_row(group_id)
    if group_row[0] == ERROR_DATABASE:
        return "Что-то пошло не так..."
    else:
        group_row = group_row[1]

    # TODO: fix potential bug
    # file can be missing
    week_dict = []
    with open("./db/groups/" + group_row[2], "r") as json_file:
        week_dict = json.load(json_file)

    html_text_first = get_html_text_first()
    html_text_second = get_html_text_second()
    if html_text_first[0] == ERROR_WEB or html_text_second[0] == ERROR_WEB:
        return "Что-то пошло не так..."
    html_text_first = html_text_first[1]
    html_text_second = html_text_second[1]

    if group_row[3] == "first":
        week_type = get_web_week_type(html_text_first)
    elif group_row[3] == "second":
        week_type = get_web_week_type(html_text_second)
    else:
        return "Что-то пошло не так..."

    if week_type[0] == ERROR_WEB:
        return "Что-то пошло не так..."
    week_type = week_type[1]

    if week_type == "ch":
        text = "<b>Числитель</b>\n\n"
    elif week_type == "zn":
        text = "<b>Знаменатель</b>\n\n"

    text += "🔴 Понедельник\n" + get_day_schedule_text(week_dict["mon"][week_type]) + '\n'
    text += "🟠 Вторник\n" +     get_day_schedule_text(week_dict["tue"][week_type]) + '\n'
    text += "🟡 Среда\n" +       get_day_schedule_text(week_dict["wed"][week_type]) + '\n'
    text += "🟢 Четверг\n" +     get_day_schedule_text(week_dict["thu"][week_type]) + '\n'
    text += "🔵 Пятница\n" +     get_day_schedule_text(week_dict["fri"][week_type]) + '\n'
    text += "🟣 Суббота\n" +     get_day_schedule_text(week_dict["sat"][week_type])

    return text

def get_changed_day_text(group_id: int) -> str:
    html_text_first = get_html_text_first()
    html_text_second = get_html_text_second()
    if html_text_first[0] == ERROR_WEB or html_text_second[0] == ERROR_WEB:
        return "Что-то пошло не так..."
    html_text_first = html_text_first[1]
    html_text_second = html_text_second[1]

    changes = get_all_changes(html_text_first, html_text_second)

    group_row = get_group_row(group_id)
    if group_row[0] == ERROR_DATABASE:
        return "Что-то пошло не так..."
    group_row = group_row[1]

    if group_row[3] == "first":
        date = get_web_date(html_text_first)
        week_type = get_web_week_type(html_text_first)
        if week_type[0] == ERROR_WEB:
            return "Что-то пошло не так..."
        week_type = week_type[1]
    elif group_row[3] == "second":
        date = get_web_date(html_text_second)
        week_type = get_web_week_type(html_text_second)
        if week_type[0] == ERROR_WEB:
            return "Что-то пошло не так..."
        week_type = week_type[1]
    else:
        return "Что-то пошло не так..."

    # TODO: fix potential bug
    # file can be missing
    week_dict = []
    with open("./db/groups/" + group_row[2], "r") as json_file:
        week_dict = json.load(json_file)

    match date.weekday():
        case 0:
            day_name = "mon"
            day_display_name = "Понедельник"
        case 1:
            day_name = "tue"
            day_display_name = "Вторник"
        case 2:
            day_name = "wed"
            day_display_name = "Среда"
        case 3:
            day_name = "thu"
            day_display_name = "Четверг"
        case 4:
            day_name = "fri"
            day_display_name = "Пятница"
        case 5:
            day_name = "sat"
            day_display_name = "Суббота"
        case _:
            return "Что-то пошло не так..."

    day_dict = week_dict[day_name][week_type]

    for change in changes:
        if group_row[1] in change["group_name"]:
            pairs_string = change["pair_number"]
            pair_numbers = []

            if ',' in pairs_string:
                pair_numbers = pairs_string.split(',')
            elif '-' in pairs_string:
                split = pairs_string.split('-')
                for i in range(int(split[0]), int(split[1]) + 1):
                    pair_numbers.append(str(i))
            else:
                pair_numbers.append(pairs_string.replace(' ', ''))

            for pair_number in pair_numbers:
                try:
                    day_dict[pair_number][0] = change["changed_to"]
                    day_dict[pair_number][1] = "⚠️ЗАМЕНА⚠️"
                    day_dict[pair_number][2] = change["classroom"]
                except:
                    day_dict[pair_number] = ['', '', '']
                    day_dict[pair_number][0] = change["changed_to"]
                    day_dict[pair_number][1] = "⚠️ЗАМЕНА⚠️"
                    day_dict[pair_number][2] = change["classroom"]

    return f"<b>Расписание на {date.day}.{date.month}.{date.year} ({day_display_name})</b>\n\n" + get_day_schedule_text(day_dict)
