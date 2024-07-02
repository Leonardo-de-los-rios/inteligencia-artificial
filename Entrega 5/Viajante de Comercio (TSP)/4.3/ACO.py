# imports
import random

import numpy as np

# Parámetros del algoritmo
num_hormigas = 100  # Numero de Caminos a analizar
num_iteraciones = 80  # Ciudades tomadas
feromona_inicial = 1.0
limite_distancia = 15000
rho = 0.1  # Factor de evaporación
alfa = 2.0  # Importancia de la feromona
beta = 5.0  # Importancia de la heurística

# Las iteraciones marcan la longitud del camino analizado
# El numero de hormigas da los posibles caminos a evaluar


# Extraccion de distancias del documento de texto
def leer_distancias(filename, num_ciudades):
    """Lee un archivo de texto que contiene la distancia que separa cada una de las
    ciudades, desde el archivo filename. La matriz resultante que devuelve pordra
    ser simetrica o no, dependiendo de si no es lo mismo ir de A a B que de B a A"""
    distancias = np.zeros((num_ciudades, num_ciudades))
    with open(filename, "r") as file:
        for line in file:
            partes = line.split()
            distancias[int(partes[1]) - 1][int(partes[2]) - 1] = float(partes[3])
    return distancias


def crear_posicion_inicial(num_ciudades, hormigas):
    posiciones = []
    for i in range(hormigas):
        posiciones.append((random.randint(0, num_ciudades - 1)))
    return posiciones


def construccion_heuristicas(distancias, num_ciudades):
    heuristicas = np.zeros((num_ciudades, num_ciudades))
    for i in range(num_ciudades):
        for j in range(num_ciudades):
            if i == j and distancias[i][j] == 0:
                heuristicas[i][j] = 0
            else:
                heuristicas[i][j] = float(1 / distancias[i][j])
    return heuristicas


# Actualizar las feromonas
# ACTUALIZAR
def actualizar_feromonas(feromonas, costos, pos_inicial, pos_final):
    """Actualiza la feromona luego de que todas las hormigas generen su recorrido.
    Un recorrido equivale a una iteracion. La feromona se actualiza debido a la nueva
    que van dejando las hormigas que pasan por cierto recorrido"""
    # calculo de actuliazr feromonas
    for i in range(num_ciudades):
        for j in range(num_ciudades):
            feromonas[i][j] *= 1 - rho  # toda feromona se desvanece
    for i in range(num_hormigas):
        r = int(pos_inicial[i])
        s = int(pos_final[i])
        feromonas[s][r] += 1 / costos[i]
    return feromonas


def calculo_probabilidad(posicion, heuristicas, feromonas):
    prob = np.zeros((num_hormigas, num_ciudades))
    for i in range(num_hormigas):
        sumatoria = 0
        x = int(posicion[i])
        for j in range(num_ciudades):
            prob[i, j] = heuristicas[x][j] ** beta * feromonas[x, j] ** alfa
            sumatoria += prob[i, j]
        for j in range(num_ciudades):
            prob[i, j] /= sumatoria
    return prob


def calculo_probabilidad_v2(posicion, heuristicas, feromonas, ruta_hormigas):
    prob = np.zeros((num_hormigas, num_ciudades))
    for i in range(num_hormigas):
        sumatoria = 0
        ruta_parcial = ruta_hormigas[:, i]
        x = int(posicion[i])
        for j in range(num_ciudades):
            if (
                j not in ruta_parcial
            ):  # si la ciudad j no ha sido ya visitada por la i-esima hormiga
                prob[i, j] = heuristicas[x][j] ** beta * feromonas[x, j] ** alfa
                sumatoria += prob[i, j]
            else:
                prob[i, j] = 0
        for j in range(num_ciudades):
            if prob[i, j] != 0:
                prob[i, j] /= sumatoria
    return prob


def cal_total_distance(ruta):
    limite_distancia = 15000
    total_distance = 0
    for i in range(1, len(ruta)):
        total_distance += matriz_distancias[int(ruta[i - 1])][int(ruta[i])]
    if total_distance > limite_distancia:
        total_distance = 10000000
    return total_distance


# Funcion principal

# Las iteraciones marcan la longitud del camino analizado
# El numero de hormigas da los posibles caminos a evaluar


def ACO(
    distancias, heuristicas, feromonas, num_ciudades, num_hormigas, num_iteraciones
):
    posicion_inicial = crear_posicion_inicial(num_ciudades, num_hormigas)
    mejor_distancia = float("inf")
    mejor_ruta = None
    ruta_hormigas = np.zeros((num_iteraciones, num_hormigas))

    for i in range(num_iteraciones):
        ruta_hormigas[i, :] = posicion_inicial
        # Calcular probabilidades de transicion de las hormigas
        if i == 0:
            probabilidades = calculo_probabilidad(
                posicion_inicial, heuristicas, feromonas
            )
        else:
            probabilidades = calculo_probabilidad_v2(
                posicion_inicial, heuristicas, feromonas, ruta_hormigas[0 : (i + 1), :]
            )

        posicion_actual = []
        costo = []
        for j in range(num_hormigas):
            # Seleccionar la transicion de maxima posibilidad
            maximo = np.max(
                probabilidades[j, :]
            )  # maxima probabilidad de la j-esima hormiga
            indice_max = np.where(probabilidades[j, :] == maximo)[0][
                0
            ]  # numero de ciudad de la probabilidad maxima
            posicion_actual.append(
                indice_max
            )  # se adjunta la posicion actual, para la j-esima hormiga
            costo.append(distancias[int(posicion_inicial[j])][indice_max])
            # el costo de esta iteracion, para la j-esima hormiga, es la distancia recorrida por
            # la j-esima hormiga, desde su posicion inicial hasta su posicion actual
        # Actualizacion de feromonas
        feromonas = actualizar_feromonas(
            feromonas, costo, posicion_inicial, posicion_actual
        )
        # Actualizacion de posicion inicial
        posicion_inicial = posicion_actual
    # Evaluación de la solucion obtenida: termina el camino de la hormiga
    ruta_hormigas = np.transpose(ruta_hormigas)
    for i in range(num_hormigas):
        dist_total = cal_total_distance(ruta_hormigas[i, :])
        # Actualizacion condicional del mejor
        if dist_total < mejor_distancia:
            mejor_distancia = dist_total
            mejor_ruta = ruta_hormigas[i, :]

    return mejor_distancia, mejor_ruta


# Main
num_ciudades = 100
matriz_distancias = leer_distancias("DIST100.txt", num_ciudades)
matriz_heuristicas = construccion_heuristicas(matriz_distancias, num_ciudades)
feromonas = np.ones((num_ciudades, num_ciudades)) * feromona_inicial
mejor_distancia, mejor_ruta = ACO(
    matriz_distancias,
    matriz_heuristicas,
    feromonas,
    num_ciudades,
    num_hormigas,
    num_iteraciones,
)
for i in range(len(mejor_ruta)):
    mejor_ruta[i] += 1
print(
    "================Algoritmo de Optimizacion por Colonia de Hormiga================"
)
print("----PARAMETROS:----")
print("Hormigas utilizadas (caminos analizados): ", num_hormigas)
print("Numero de iteraciones (ciudades tomadas): ", num_iteraciones)
print(
    "Mejor distancia encontrada: ***",
    mejor_distancia,
    "*** en ",
    num_iteraciones,
    " ciudades",
)
print("Mejor ruta:", mejor_ruta)
