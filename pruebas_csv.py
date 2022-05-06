import csv
import pandas as pd

states = ['HHH', 'HHL', 'HLH', 'LHH', 'LLH', 'LHL', 'HLL', 'LLL'] # Los estados posibles (se pueden representar de 0 a 7)
contadorvHHH

file = open('Data.csv')
type(file)

csvreader = csv.reader(file)

rows = []
for row in csvreader:
    rows.append(row)

columns = ['Initial traffic level N', 'Initial traffic level E', 'Initial traffic level W', 'Final traffic level N', 'Final traffic level E', 'Final traffic level W']

df = pd.read_csv('Data.csv', sep=";", usecols=columns)
print(df)

# Hay que coger toda la fila, contar las veces que aparece, y dividarla entre el número total de filas [len(rows)]

for i in range(len(rows)):


for i in range(len(rows)):
    initialN = df['Initial traffic level N']
    if initialN[i] == 'High':
        _initialN = 'H'
    else:
        _initialN = 'L'

    initialE = df['Initial traffic level E']
    if initialE[i] == 'High':
        _initialE = 'H'
    else:
        _initialE = 'L'

    initialW = df['Initial traffic level W']
    if initialW[i] == 'High':
        _initialW = 'H'
    else:
        _initialW = 'L'

    finalN = df['Final traffic level N']
    if finalN[i] == 'High':
        _finalN = 'H'
    else:
        _finalN = 'L'

    finalE = df['Final traffic level E']
    if finalE[i] == 'High':
        _finalE = 'H'
    else:
        _finalE = 'L'

    finalW = df['Final traffic level W']
    if finalW[i] == 'High':
        _finalW = 'H'
    else:
        _finalW = 'L'

    initial = _initialN + _initialE + _initialW
    final = _finalN + _finalE + _finalW
    print(initial)
    print(final)

file.close()

