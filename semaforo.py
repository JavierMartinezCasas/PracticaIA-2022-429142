import csv

# Constantes
NUM_ESTADOS = 0
NUM_ACCIONES = 0
COSTE = 0
ESTADO_OBJETIVO = 0
EPSILON = 0.001  # Umbral para la diferencia entre los valores esperados en ciclos consecutivos
LIMITE_CICLOS = 5000  # Límite de ciclos para evitar posible bucle infinito
NOMBRE_FICHERO_ENTRADA = 'Data.csv'

# Variables Principales
""" Vector (lista en Python) para los costes """
costes = [0 for ac in range(NUM_ACCIONES)]
""" Matriz de 3 dimensiones (lista de lista de lista en Python) para la función de transición """
probabilidad = [[[0 for ed in range(NUM_ESTADOS)] for eo in range(NUM_ESTADOS)] for ac in range(NUM_ACCIONES)]
""" Vector (lista en Python) para la los valores esperados de los estados """
valores = [0 for eo in range(NUM_ESTADOS)]
""" Vector (lista en Python) para la las acciones óptimas de cada estado """
politicaOptima = [-1 for eo in range(NUM_ESTADOS)]


# Funciones
def obtenerProbabilidades():
    return


def calcularCostes():
    return


def obtenerValoresEsperados(costes):
    return


def obtenerPoliticaOptima(costes, probabilidad, valores):
    return


# Llamada a Funciones
probabilidad = obtenerProbabilidades()

costes = calcularCostes()

valores = obtenerValoresEsperados(costes)
print(valores)

politicaOptima = obtenerPoliticaOptima(costes, probabilidad, valores)
print(politicaOptima)

"""
with open(NOMBRE_FICHERO_ENTRADA) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1

        else:
            print(row)

    print(f'Processed {line_count} lines.')
"""
