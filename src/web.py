from bs4 import BeautifulSoup
import requests

# Номер в списке
# Группа
# Номер пары
# По расписанию
# Замена
# Аудитория

def get_all_data():
    r = requests.get("https://menu.sttec.yar.ru/timetable/rasp_first.html")
    r.encoding = r.apparent_encoding

    soup = BeautifulSoup(r.text, "html.parser")
    all = soup.find_all("td")[6:]

    parsed = []

    for i in range(0, len(all), 6):
        d = {
            "group": all[i+1].text,
            "para": all[i+2].text,
            "rasp": all[i+3].text,
            "zamena": all[i+4].text,
            "aud": all[i+4].text,
        }
        parsed = parsed + [d]

    return parsed
