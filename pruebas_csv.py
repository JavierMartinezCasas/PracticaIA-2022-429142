import csv
import pandas as pd

file = open('Data.csv')
type(file)

csvreader = csv.reader(file)

header = []
header = next(csvreader)
print(header)

rows = []
for row in csvreader:
    rows.append(row)

data = pd.read_csv('Data.csv', sep=";")
data_top = data.head
print(data_top)

states = []
columns = ['Initial traffic level N', 'Initial traffic level E']
for i in range(len(rows)):
    if not rows[i]:  # Elimina las filas vacias
        continue
    else:
        str_row = str(rows[i])
        s0 = str_row[2:16]
        sf = str_row[1:2]

        # print(s0)
        # print(sf)

        # print(rows[i]) # Imprime las filas llenas

df = pd.read_csv('Data.csv', sep=";", usecols=columns)
print(df)
initialN = df['Initial traffic level N']
print(initialN[0])

file.close()
