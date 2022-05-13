import csv
import pandas as pd

# ----------------------Definición de constantes---------------------------------
NUM_ESTADOS = 8
NUM_ACCIONES = 3
COSTE = 1
ESTADO_OBJETIVO = 0
LIMITE_CICLOS = 5000
EPSILON = 0.001
NOMBRE_FICHERO = 'Data.csv'


def obtenerProbabilidades():
    ocurrencias = [[[0 for ed in range(NUM_ESTADOS)] for eo in range(NUM_ESTADOS)] for ac in range(NUM_ACCIONES)]
    probabilidad = [[[0 for ed in range(NUM_ESTADOS)] for eo in range(NUM_ESTADOS)] for ac in range(NUM_ACCIONES)]

    columns = ['Initial traffic level N', 'Initial traffic level E', 'Initial traffic level W', 'Green traffic light',
               'Final traffic level N', 'Final traffic level E', 'Final traffic level W']  # Columnas a obtener

    df = pd.read_csv(NOMBRE_FICHERO, sep=";", usecols=columns)

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

        ocurrencias[ac][eo][ed] = ocurrencias[ac][eo][ed] + 1  # Actualizar la matriz ocurrencias con las ocurrencias de cada linea

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

    return probabilidad  # Devuelve la matriz de probabilidades


# -------------------------Introducción de los costes para cada acción----------------------------
def calcularCostes():
    costes = [COSTE for ac in range(NUM_ACCIONES)]  # Introduce la variable COSTE en la tupla de costes
    return costes


# ---------------------Cálculo de las iteraciones sobre las ecuaciones de Bellman-------------------
def obtenerValoresEsperados(costes, probabilidad):
    VO = [0 for eo in range(NUM_ESTADOS)]   # Lista de valores iniciales (eo)
    VF = [0 for eo in range(NUM_ESTADOS)]   # Lista de valores siguientes (ed)
    sumatorio = 0
    minVal = 10
    difMax = 0
    ciclo = 0
    fin = False

    while ciclo < LIMITE_CICLOS:    # Iteramos sobre las ecuaciones un número determinado de veces
        if fin:     # Si se cumple la condición de parada sale del bucle y termina el programa
            break

        for ac in range(NUM_ACCIONES):  # Recorremos bucles para la matriz de probabilidad
            for eo in range(NUM_ESTADOS):
                if eo == 0:     # Eliminamos el estado absorbente de los cálculos
                    continue    # Pasa al siguiente estado origen
                else:
                    for ed in range(NUM_ESTADOS):
                        p = probabilidad[ac][eo][ed]
                        v = VO[ed]
                        sumatorio = sumatorio + p * v   # Calcula el valor siguiente teniendo en cuenta el anterior
                    valorAccion = costes[ac] + sumatorio

                    if valorAccion < minVal:
                        minVal = valorAccion

            VF[eo] = minVal

            dif = abs(VF[eo] - VO[eo])
            if dif > difMax:
                difMax = dif

        VO = VF.copy()
        ciclo += 1
        if difMax < EPSILON or ciclo > LIMITE_CICLOS:
            fin = True  # Variable que se comprueba al inicio del for para ver si debe seguir o no (tb puede hacerse break)

    return VO


probabilidad = obtenerProbabilidades()
costes = calcularCostes()

print(obtenerValoresEsperados(costes, probabilidad))
