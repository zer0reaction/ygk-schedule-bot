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


def get_week_schedule_text(group_id: int, groups: list):
    ...
