import csv
import pandas as pd

# Los estados posibles (se pueden representar de 0 a 7)
states = ['HHH', 'HHL', 'HLH', 'LHH', 'LLH', 'LHL', 'HLL', 'LLL']

matrizE = [[]]
matrizW = [[]]

file = open('Data.csv')
csvreader = csv.reader(file)

rows = []
for row in csvreader:
    rows.append(row)

columns = ['Initial traffic level N', 'Initial traffic level E', 'Initial traffic level W', 'Green traffic light',
           'Final traffic level N', 'Final traffic level E', 'Final traffic level W']

df = pd.read_csv('Data.csv', sep=";", usecols=columns)

# Hacer funciones para cada acción para reducir el número de variables que declarar

# Hay que coger toda la fila, contar las veces que aparece, y dividarla entre el número total de filas [len(rows)]

total1 = 0
total2 = 0
total3 = 0
total4 = 0
total5 = 0
total6 = 0
total7 = 0

parcialN1 = 0

matParcial = [[]]

for i in range(8785):
    action = df['Green traffic light']
    _action = action[i]

    initialN = df['Initial traffic level N']
    if initialN[i] == 'High':
        _initialN = 1  # H
    else:
        _initialN = 0  # L

    initialE = df['Initial traffic level E']
    if initialE[i] == 'High':
        _initialE = 1
    else:
        _initialE = 0

    initialW = df['Initial traffic level W']
    if initialW[i] == 'High':
        _initialW = 1
    else:
        _initialW = 0

    finalN = df['Final traffic level N']
    if finalN[i] == 'High':
        _finalN = 1
    else:
        _finalN = 0

    finalE = df['Final traffic level E']
    if finalE[i] == 'High':
        _finalE = 1
    else:
        _finalE = 0

    finalW = df['Final traffic level W']
    if finalW[i] == 'High':
        _finalW = 1
    else:
        _finalW = 0

    initial = str(_initialN) + str(_initialE) + str(_initialW)  # Número en binario
    final = str(_finalN) + str(_finalE) + str(_finalW)

    _initial = int(initial, 2)
    _final = int(final, 2)

    # print("Row " + str(i) + ":")
    # print("Initial value: " + initial)
    # print("Action: " + _action)
    # print("Final value: " + final)
    # print("-------------------")

    """
    Fijar primero la acción, luego el estado incial de los semáforos (contamos el total)
    y finalmente el estado final (dónde contamos las ocurrencias)
    """

    # Solo 2 contadores (total y parcial), se reinician cada vez que el array vuelve
    # y sus valores se meten directamente en la matriz con la probabilidad??

    # Hacer una matriz a parte solo con los valores parciales y una lista con los totales

    # Obtener los datos para la acción N y añadir para la matrizN las probs. de la misma [columnas[filas]]
    if action[i] == "N":  # Fijamos la acción
        if _initial == 1:  # Fijamos el estado inicial con LLH (001 == 1)
            total1 += 1
            for j in range(8785):  # Recorremos los datos para buscar los que el estado inicial sea LLL (000)
                if _final == 1:
                    #matParcial[0][0] += 1
                    parcialN1 += 1

        if int(_initial) == 2:
            total2 += 1

    """
    elif action[i] == "E":
        print()

    elif action[i] == "W":
        print()
    """
print(total1)
print(total2)
print(matParcial[0])

file.close()


def countN():
    matrizN = [[]]
    print(initial)
