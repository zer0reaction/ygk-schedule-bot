from bs4 import BeautifulSoup
from constants import *
import requests
from datetime import datetime

# Get the raw html text of the first
def get_html_text_first():
    try:
        r = requests.get("https://menu.sttec.yar.ru/timetable/rasp_first.html")
        r.encoding = "utf-8"
        return (OK, r.text)
    except Exception as e:
        print("Error in web:get_html_text")
        print(f"    {e}")
        return (ERROR_WEB, )

# Get the raw html text of the second
def get_html_text_second():
    try:
        r = requests.get("https://menu.sttec.yar.ru/timetable/rasp_second.html")
        r.encoding = "utf-8"
        return (OK, r.text)
    except Exception as e:
        print("Error in web:get_html_text")
        print(f"    {e}")
        return (ERROR_WEB, )

# Get data about the changes
def get_changes(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    row_tags = soup.find_all("tr")[1:]
    changes = []

    for tag in row_tags:
        contents = tag.find_all("td")
        change = {
            "group_name": contents[1].text,
            "pair_number": contents[2].text,
            "scheduled": contents[3].text,
            "changed_to": contents[4].text,
            "classroom": contents[5].text,
        }
        changes.append(change)

    return changes

# TODO: fix potential bug
# web date can crash
# Get the date displayed on the website (datetime)
def get_web_date(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    text = soup.find_all("div")[2].text

    date_list = text.split()[3:6]

    day = int(date_list[0])
    year = int(date_list[2])
    month = 0

    match date_list[1]:
        case "января":      month = 1
        case "февраля":     month = 2
        case "марта":       month = 3
        case "апреля":      month = 4
        case "мая":         month = 5
        case "июня":        month = 6
        case "июля":        month = 7
        case "августа":     month = 8
        case "сентября":    month = 9
        case "октября":     month = 10
        case "ноября":      month = 11
        case "декабря":     month = 12

    date = datetime(year, month, day, 0, 0, 0)

    return date

# Get if the displayed changes are for chislitel or znamenatel
def get_web_week_type(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    text = soup.find_all("div")[3].text

    if "Числитель" in text:
        return (OK, "ch")
    elif "Знаменатель" in text:
        return (OK, "zn")
    else:
        return (ERROR_WEB, )
