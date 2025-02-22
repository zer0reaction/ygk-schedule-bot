import openpyxl
import json
from openpyxl.cell.cell import MergedCell

week = {
    'name': '',
    'mon': { 'ch': {}, 'zn': {} },
    'tue': { 'ch': {}, 'zn': {} },
    'wed': { 'ch': {}, 'zn': {} },
    'thu': { 'ch': {}, 'zn': {} },
    'fri': { 'ch': {}, 'zn': {} },
    'sat': { 'ch': {}, 'zn': {} }
}

wb = openpyxl.load_workbook('./file.xlsx')
ws = wb.active

data = []

for row in ws.rows:
    data.append([row[0], row[1], row[5], row[8]])

for i, row in enumerate(data):
    for j, cell in enumerate(row):
        if type(cell) == MergedCell:
            data[i][j] = 'Merged'
        else:
            data[i][j] = str(cell.value)

group_name = data[0][0]
data = data[2:]

i = 0
while i < len(data) - 1:
    if data[i][0] in [str(x) for x in range(10)]:
        data[i].append('ch')
        data[i + 1].append('zn')
        data[i + 1][0] = data[i][0]
        i += 1
    else:
        data[i].append('day')
    i += 1

i = 0
while i < len(data) - 1:
    if data[i][-1] == 'day':
        i += 1
        continue

    for j, cell in enumerate(data[i]):
        if data[i][j] == 'Merged':
            data[i][j] = data[i + 1][j]
        elif data[i + 1][j] == 'Merged':
            data[i + 1][j] = data[i][j]

    i += 2

week['name'] = group_name

for row in data:
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

    if not 'None' in row:
        week[day_key][row[-1]][row[0]] = []
        week[day_key][row[-1]][row[0]].append(row[1].replace('\n', ', '))
        week[day_key][row[-1]][row[0]].append(row[2].replace('\n', ', '))
        week[day_key][row[-1]][row[0]].append(row[3].replace('\n', ', '))


file_name = input('input file name (without .json): ')
file_name += '.json'
path = './db/groups/' + file_name

with open(path, 'w') as file:
    json.dump(week, file, indent=4, ensure_ascii=False)

print(f'{path} written')
