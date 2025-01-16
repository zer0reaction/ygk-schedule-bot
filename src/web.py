from bs4 import BeautifulSoup
import requests
import datetime

# 0 Номер в списке
# 1 Группа
# 2 Номер пары
# 3 По расписанию
# 4 Замена
# 5 Аудитория

def get_html_text():
    r = requests.get("https://menu.sttec.yar.ru/timetable/rasp_first.html")
    r.encoding = r.apparent_encoding
    return r.text

def get_all_data(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    all = soup.find_all("td")[6:]

    parsed = []

    for i in range(0, len(all), 6):
        d = {
            "group":  all[i+1].text,
            "para":   all[i+2].text,
            "rasp":   all[i+3].text,
            "zamena": all[i+4].text,
            "aud":    all[i+5].text,
        }
        parsed = parsed + [d]

    return parsed

def get_web_date(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    text = soup.find_all("div")[2].text
    return text.split(' ')[3] + " " + text.split(' ')[4]

def get_web_ch_zn(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    text = soup.find_all("div")[3].text

    if "Числитель" in text:
        return "ch"
    else: return "zn"
