import json
import openpyxl as xl

wb = xl.load_workbook('./test.xlsx')
ws = wb.active

raw_data = tuple(ws.values)
normalized_data = []

# step 1: remove unnecesary 'None's
for row in raw_data:
    t = []
    t.append(row[0])
    t.append(row[1])
    t.append(row[5])
    t.append(row[8])
    normalized_data.append(t)

# step 2: replace 'None's with numbers where needed
for i in range(len(normalized_data) - 1):
    if normalized_data[i][0] in range(10) and \
       normalized_data[i + 1][0] == None:
        normalized_data[i + 1][0] = normalized_data[i][0]

# step 3: add ch zn
for i in range(len(normalized_data) - 1):
    if normalized_data[i][0] == normalized_data[i + 1][0]:
        normalized_data[i].append('ch')
        normalized_data[i + 1].append('zn')

week = {
    'mon': { 'ch': {}, 'zn': {} },
    'tue': { 'ch': {}, 'zn': {} },
    'wed': { 'ch': {}, 'zn': {} },
    'thu': { 'ch': {}, 'zn': {} },
    'fri': { 'ch': {}, 'zn': {} },
    'sat': { 'ch': {}, 'zn': {} }
}

for row in normalized_data:
    if row[0] == 'Понедельник':
        day_key = 'mon'
        continue
    elif row[0] == 'Вторник':
        day_key = 'tue'
        continue
    elif row[0] == 'Среда':
        day_key = 'wed'
        continue
    elif row[0] == 'Четверг':
        day_key = 'thu'
        continue
    elif row[0] == 'Пятница':
        day_key = 'fri'
        continue
    elif row[0] == 'Суббота':
        day_key = 'sat'
        continue

    if row[1] != None:
        week[day_key][row[4]][str(row[0])] = []
        week[day_key][row[4]][str(row[0])].append(row[1])
        week[day_key][row[4]][str(row[0])].append(row[2])
        week[day_key][row[4]][str(row[0])].append(row[3])

filename = input('Input file name: ')

with open(filename, 'w') as file:
    json.dump(week, file, ensure_ascii=False, indent=4)
