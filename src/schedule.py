import json

def get_week_shedule(group_id: int, groups: list):
    filename = ""
    for group in groups:
        if group_id == group[0]: filename = group[2]

    data = []
    with open("db/groups/" + filename, "r") as json_file:
        data = json.load(json_file)

    return data
