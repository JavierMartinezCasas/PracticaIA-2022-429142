import csv
import pandas as pd

# ----------------------Definición de constantes---------------------------------
NUM_ESTADOS = 8
NUM_ACCIONES = 3
COSTE = 1
ESTADO_OBJETIVO = 0
LIMITE_CICLOS = 5000


def obtenerProbabilidades():
    ocurrencias = [[[0 for ed in range(NUM_ESTADOS)] for eo in range(NUM_ESTADOS)] for ac in range(NUM_ACCIONES)]
    probabilidad = [[[0 for ed in range(NUM_ESTADOS)] for eo in range(NUM_ESTADOS)] for ac in range(NUM_ACCIONES)]

    filename = 'Data.csv'  # Abrir fichero
    csvreader = csv.reader(filename)

    rows = []
    for row in csvreader:  # Recorrer cada linea
        rows.append(row)

    columns = ['Initial traffic level N', 'Initial traffic level E', 'Initial traffic level W', 'Green traffic light',
               'Final traffic level N', 'Final traffic level E', 'Final traffic level W']   # Columnas a obtener

    df = pd.read_csv('Data.csv', sep=";", usecols=columns)

    # -------------------Asignación de valores decimales a las acciones -----------------------------
    for i in range(8785):  # Parra recorrer todas las filas del fichero de datos
        action = df['Green traffic light']
        if action[i] == 'N':  # Comprueba qué semáforo está encendiendo
            ac = 0  # Le asigna un valor (del 0 al 2)
        if action[i] == 'E':
            ac = 1
        if action[i] == 'W':
            ac = 2

        # ----------------Asignación de valores binarios a los estados-------------------------------
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

        # ----------------Unión de valores para los estados------------------
        initial = str(_initialN) + str(_initialE) + str(_initialW)  # Número en binario del estado origen
        final = str(_finalN) + str(_finalE) + str(_finalW)  # Número en binario del estado destino

        eo = int(initial, 2)  # Número en decimal del estado origen
        ed = int(final, 2)  # Número en decimal del estado destino

        ocurrencias[ac][eo][ed] = ocurrencias[ac][eo][
                                      ed] + 1  # Actualizar la matriz ocurrencias con las ocurrencias de cada linea

    # -------------------Obtención de la matriz de probabilidades-----------------------
    for ac in range(NUM_ACCIONES):
        for eo in range(NUM_ESTADOS):
            total = 0
            for ed in range(NUM_ESTADOS):
                total += ocurrencias[ac][eo][ed]
            for ed in range(NUM_ESTADOS):
                if total == 0:
                    probabilidad[ac][eo][ed] = -1
                else:
                    probabilidad[ac][eo][ed] = ocurrencias[ac][eo][ed] / total

    return probabilidad # Devuelve la matriz de probabilidades


# -------------------------Introducción de los costes para cada acción----------------------------
def calcularCostes():
    costes = [COSTE for ac in range(NUM_ACCIONES)]  # Introduce la variable COSTE en la tupla de costes
    return costes


# Esta función itera sobre las ecuaciones de Bellman un número determinado de veces y devuelve una tabla con los valores
def obtenerValoresEsperados(costes, probabilidad):
    valores = [0 for eo in range(NUM_ESTADOS)]
    valores_aux = [0 for eo in range(NUM_ESTADOS)]
    verdeN = costes[0]
    verdeE = costes[1]
    verdeW = costes[2]

    valorN = [0 for i in range(NUM_ESTADOS)]   # Tablas específicas para cada acción
    valorE = [0 for j in range(NUM_ESTADOS)]
    valorW = [0 for k in range(NUM_ESTADOS)]

    # Meter aquí un while para que itere solo 5000 veces
    for ac in range(len(probabilidad)):  # ac es 0, 1 o 2 para cada acción
        if ac == 0:
            cost = verdeN
            for eo in range(len(probabilidad[ac])):
                for ed in range(len(probabilidad[ac][eo])):  # Cada elemento de aquí es un probabilidad[ac][eo][ed]
                    #print(valorN[ed])
                    valor = cost + probabilidad[ac][eo][ed] * valorN[ed]
                    print(valor)
                    valorN[ed] = valor

        if ac == 1:
            cost = verdeE
            for eo in range(len(probabilidad[ac])):
                for ed in range(len(probabilidad[ac][eo])):  # Cada elemento de aquí es un probabilidad[ac][eo][ed]
                    valor = cost + probabilidad[ac][eo][ed] * valorE[ed]
                    valorE[ed] = valor

        if ac == 2:
            cost = verdeW
            for eo in range(len(probabilidad[ac])):
                for ed in range(len(probabilidad[ac][eo])):  # Cada elemento de aquí es un probabilidad[ac][eo][ed]
                    valor = cost + probabilidad[ac][eo][ed] * valorW[ed]
                    valorW[ed] = valor

    for i in range(len(valores)):
        valores[i] = min(valorN[i], valorE[i], valorW[i])

    return valores


probabilidad = obtenerProbabilidades()  # Obtener las probabilidades para las ecuaciones
costes = calcularCostes()
valores = obtenerValoresEsperados(costes, probabilidad)

print(valores)
print(probabilidad)