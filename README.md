# Бот для просмотра расписания ЯГК

## Основная информация

**Телеграм:** @ygkschedule\_bot

**На данный момент доступны следующие опции:**
- Просмотр расписания на неделю (без замен)
- Просмотр расписания на день (с заменами)

**Список добавленных групп:**
- АР1-22

## Для разработчиков

**Список пакетов pip:**
- telebot
- bs4
- requests

**Запуск**:
Для работы бота необходимо создать файл src/creds.py и ввести туда API токен бота:

*src/creds.py*
```python
token="ваш токен"
```

Linux:
```console
cd ygk-schedule-bot
python -m venv ./
bin/pip3 install telebot bs4 requests
bin/python3 src/bot.py
```
