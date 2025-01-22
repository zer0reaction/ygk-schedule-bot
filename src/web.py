from bs4 import BeautifulSoup
from constants import *
import requests
import datetime

# Get the raw html text
def get_html_text():
    try:
        r = requests.get("https://menu.sttec.yar.ru/timetable/rasp_first.html")
        r.encoding = "utf-8"
        return (OK, r.text)
    except Exception as e:
        print("Error in web:get_html_text")
        print("    {}".format(e))
        return (ERROR_WEB, )

# Get data about all the changes
def get_all_changes(html_text):
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

# Get the date displayed on the website (datetime)
def get_web_date(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    text = soup.find_all("div")[2].text

    date_list = text.split()[3:6]

    date = datetime
    date.day = int(date_list[0])
    date.year = int(date_list[2])

    match date_list[1]:
        case "января":      date.month = 0
        case "февраля":     date.month = 1
        case "марта":       date.month = 2
        case "апреля":      date.month = 3
        case "мая":         date.month = 4
        case "июня":        date.month = 5
        case "июля":        date.month = 6
        case "августа":     date.month = 7
        case "сентября":    date.month = 8
        case "октября":     date.month = 9
        case "ноября":      date.month = 10
        case "декабря":     date.month = 11

    return date

# Get if the displayed changes are for chislitel or znamenatel
def get_web_ch_zn(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    text = soup.find_all("div")[3].text

    if "Числитель" in text:
        return "ch"
    else: return "zn"
