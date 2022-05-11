import csv
import pandas as pd

# Constantes
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
               'Final traffic level N', 'Final traffic level E', 'Final traffic level W']

    df = pd.read_csv('Data.csv', sep=";", usecols=columns)

    for i in range(8785):  # Parra recorrer todas las filas del fichero de datos
        action = df['Green traffic light']
        if action[i] == 'N':  # Comprueba que semáforo está encendiendo
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

        initial = str(_initialN) + str(_initialE) + str(_initialW)  # Número en binario del estado origen
        final = str(_finalN) + str(_finalE) + str(_finalW)  # Número en binario del estado destino

        eo = int(initial, 2)  # Número en decimal del estado origen
        ed = int(final, 2)  # Número en decimal del estado destino

        ocurrencias[ac][eo][ed] = ocurrencias[ac][eo][
                                      ed] + 1  # Actualizar la matriz ocurrencias con las ocurrencias de cada linea

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

    return probabilidad


# Esta funbción genera una tupla con los costes correspondientes para cada acción
def calcularCostes():
    costes = [COSTE for ac in range(NUM_ACCIONES)]
    return costes


# Esta función itera sobre las ecuaciones de Bellman un número determinado de veces y devuelve una tabla con los valores
def obtenerValoresEsperados(costes, probabilidad):
    valores = [0 for eo in range(NUM_ESTADOS)]
    verdeN = costes[0]
    verdeE = costes[1]
    verdeW = costes[2]

    for ac in range(len(probabilidad)):  # ac es 0, 1 o 2 para cada acción
        if ac == 0:
            cost = verdeN
        elif ac == 1:
            cost = verdeE
        elif ac == 2:
            cost = verdeW

        for eo in range(len(probabilidad[ac])):
            # print(eo)
            for ed in range(len(probabilidad[ac][eo])):  # Cada elemento de aquí es un probabilidad[ac][eo][ed]
                # print(ed)
                valor = cost + probabilidad[ac][eo][ed] * valores[ed]
                valores[ed] = valor

    """
    # Plantear las ecuaciones de Bellman
    for ac in range(probabilidad):  #Recorremos para los 3 diferentes estados
        if ac == 0:
            cost = verdeN   # Asignamos el coste de la tupla costes
        for eo in range(probabilidad):
            for ed in range(probabilidad):
                print(probabilidad[ac][eo][ed])

        if ac == 1:
            cost = verdeE
        for eo in range(probabilidad):
            for ed in range(probabilidad):
                print(probabilidad[ac][eo][ed])

        if ac == 2:
            cost = verdeW
        for eo in range(probabilidad):
            for ed in range(probabilidad):
                print(probabilidad[ac][eo][ed])
    """
    return valores


probabilidad = obtenerProbabilidades()  # Obtener las probabilidades para las ecuaciones
costes = calcularCostes()
valores = obtenerValoresEsperados(costes, probabilidad)

print(valores)
