# Бот для просмотра расписания ЯГК

## Основная информация

**Телеграм:** @ygkschedule\_bot

**На данный момент доступны следующие опции:**
- Просмотр расписания на неделю (без замен)
- Просмотр расписания на день (с заменами)

**Список добавленных групп:**
- АР1-22
- ИС1-35

## Для разработчиков

### Запуск:
Для работы бота необходимо создать файл src/creds.py и ввести туда API токен бота:

```python
# src/creds.py
token="ваш токен"
```

Также Вам потребуется файл базы данных db/base.db. Комманды для создания таблиц:
```sql
CREATE TABLE "groups" (
	"group_id"	INTEGER NOT NULL,
	"group_name"	TEXT NOT NULL,
	"file_name"	TEXT NOT NULL,
	PRIMARY KEY("group_id" AUTOINCREMENT)
);

CREATE TABLE "users" (
	"telegram_id"	INTEGER NOT NULL,
	"group"	INTEGER NOT NULL,
	PRIMARY KEY("telegram_id"),
	FOREIGN KEY("group") REFERENCES "groups"("group_id")
);
```

Linux:
```console
cd ygk-schedule-bot
python -m venv ./
bin/pip3 install telebot bs4 requests
bin/python3 src/bot.py
```
