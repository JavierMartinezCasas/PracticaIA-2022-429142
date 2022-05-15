import pandas as pd     # Utilizado para leer el fichero .csv

# ----------------------Definición de constantes---------------------------------
NUM_ESTADOS = 8
NUM_ACCIONES = 3
COSTE = 1  # Coste seleccionado para las acciones
ESTADO_OBJETIVO = 0     # Estado absorbente
LIMITE_CICLOS = 5000   # Límite de iteraciones permitidas
EPSILON = 0.001  # Umbral para la diferencia entre los valores esperados en ciclos consecutivos
NOMBRE_FICHERO = 'Data.csv'


def obtenerProbabilidades():
    ocurrencias = [[[0 for ed in range(NUM_ESTADOS)] for eo in range(NUM_ESTADOS)] for ac in range(NUM_ACCIONES)]
    probabilidad = [[[0 for ed in range(NUM_ESTADOS)] for eo in range(NUM_ESTADOS)] for ac in range(NUM_ACCIONES)]

    columns = ['Initial traffic level N', 'Initial traffic level E', 'Initial traffic level W', 'Green traffic light',
               'Final traffic level N', 'Final traffic level E', 'Final traffic level W']  # Columnas a obtener del fichero

    df = pd.read_csv(NOMBRE_FICHERO, sep=";", usecols=columns)      # Lectura del fichero .csv

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

        ocurrencias[ac][eo][ed] = ocurrencias[ac][eo][ed] + 1  # Actualizar la matriz ocurrencias

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
                    probabilidad[ac][eo][ed] = ocurrencias[ac][eo][ed] / total  # Obtención de la probabilidad

    return probabilidad  # Devuelve la matriz de probabilidades


# -------------------------Introducción de los costes para cada acción----------------------------
def calcularCostes():
    costes = [COSTE for ac in range(NUM_ACCIONES)]  # Introduce la variable COSTE en la tupla de costes
    return costes


# ------------------------Cambia los valores de accción por una string----------------------------
def changeAction(ac):
    if ac == 0:
        action = "N"
    elif ac == 1:
        action = "E"
    elif ac == 2:
        action = "W"

    return action


# ----------------Cálculo de las iteraciones sobre las ecuaciones de Bellman y la Política Óptima-----------------
def obtenerValoresEsperados(costes, probabilidad):
    VO = [0 for eo in range(NUM_ESTADOS)]  # Lista de valores iniciales (eo)
    VF = [0 for eo in range(NUM_ESTADOS)]  # Lista de valores siguientes (ed)
    PL = [0 for eo in range(NUM_ESTADOS)]  # Lista para guardar la política óptima
    PL[0] = None  # Valor None para la política óptima del estado meta el estado meta
    sumatorio = 0  # Sumatorio de las probabilidades * valores para cada acción
    minVal = 1000000  # Valor mínimo para comparar entre acciones
    difMax = 1000000  # Diferencia máxima para convergencia
    ciclo = 0  # Contador del nº de iteración
    fin = False  # Comprueba si el programa debe terminar o no

    while ciclo < LIMITE_CICLOS:  # Iteramos sobre las ecuaciones un número determinado de veces
        if fin:  # Si se cumple la condición de parada sale del bucle y termina el programa
            break
            difMax = 100000

        for eo in range(NUM_ESTADOS):   # Recorremos el bucle para cada uno de los estados
            minVal = 100000
            for ac in range(NUM_ACCIONES):  # Recorremos bucles para cada acción
                sumatorio = 0
                if eo == ESTADO_OBJETIVO:  # Eliminamos el estado absorbente de los cálculos
                    continue
                else:
                    for ed in range(NUM_ESTADOS):
                        p = probabilidad[ac][eo][ed]    # Obtiene el valor de la matriz de probabilidades
                        v = VO[ed]  # Obtiene el valor del estado anterior
                        sumatorio += p * v  # Sumatorio de probabilidades por los valores
                    valorAccion = costes[ac] + sumatorio  # Suma el coste de cada acción a sumatorio

                if valorAccion < minVal:    # Comprobamos si el valor incipiente es menor que el guardado
                    PL[eo] = changeAction(ac)  # Asignación de la acción óptima para el estado
                    minVal = round(valorAccion, 2)
                    VF[eo] = minVal

            dif = abs(VF[eo] - VO[eo])  # Obtenemos la diferencia entre los valores obtenidos
            if dif > difMax:    # Comprobamos si la diferencia entre valores es mayor que la máxima obtenida
                difMax = dif

        VO = VF.copy()  # Copiamos la matriz con los valores siguientes a los anteriores
        ciclo += 1  # Añadimos uno al nº de iteraciones
        if difMax < EPSILON or ciclo > LIMITE_CICLOS:   # Comprobamos si los valores han convergido o se ha superado el máximo nº de iteraciones permitidas
            fin = True  # Variable que se comprueba al inicio del for para ver si debe seguir o no (tb puede hacerse break)

    # --------------------------Impresión de los resultados por pantalla---------------------------
    print()
    print("¡Éxito!")
    print("Los valores convergen tras: ", ciclo, "iteraciones")
    print("Coste seleccionado: ", costes[0])
    print()
    print("-------------------------------------RESULTADOS-------------------------------------")
    print("La lista de valores esperados es: ", VO)
    print()
    print("La lista de politica óptima es: ", PL)
    print()
    return VO   # Devuelve la lista de valores esperados


probabilidad = obtenerProbabilidades()  # Llama a la función que obtiene la tabla de probabilidades
costes = calcularCostes()   # Llama a la función que asigna los costes a las acciones

obtenerValoresEsperados(costes, probabilidad)   # Llama a la función que obtiene los valores esperados y la política óptima
