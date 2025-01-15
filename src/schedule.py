import json

def get_week_data(group_id: int, groups: list):
    filename = ""
    for group in groups:
        if group_id == group[0]: filename = group[2]

    data = []
    with open("db/groups/" + filename, "r") as json_file:
        data = json.load(json_file)

    return data

def get_day_schedule_text(week_data: list, day: str, week_type: str):
    chars = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
    text = ""
    day_data = week_data[day][week_type]
    day_lect = day_data.keys()

    for lect in day_lect:
        text += chars[int(lect)] + " <b>[" + day_data[lect][2] + "]</b> " + \
            "<i>" + day_data[lect][0] + "</i> (" + day_data[lect][1] + ')\n'

    return text

def get_week_schedule_text(group_id: int, groups: list, week_type: str):
    week_data = get_week_data(group_id, groups)

    mon_text = get_day_schedule_text(week_data, "mon", week_type)
    tue_text = get_day_schedule_text(week_data, "tue", week_type)
    wed_text = get_day_schedule_text(week_data, "wed", week_type)
    thu_text = get_day_schedule_text(week_data, "thu", week_type)
    fri_text = get_day_schedule_text(week_data, "fri", week_type)
    sat_text = get_day_schedule_text(week_data, "sat", week_type)

    text = "🗓Понедельник\n{}\n🗓Вторник\n{}\n🗓Среда\n{}\n🗓Четверг\n{}\n🗓Пятница\n{}\n🗓Суббота\n{}".format(mon_text, tue_text, wed_text, thu_text, fri_text, sat_text)

    if week_type == "ch": text = "<b>Числитель</b>\n\n" + text
    else: text = "<b>Знаменатель</b>\n\n" + text

    return text
