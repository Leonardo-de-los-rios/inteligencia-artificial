import random

import numpy as np


def leer_distancias(filename):
    with open(filename, "r") as f:
        data = f.readlines()

    num_ciudades = int(data[-1].split()[1])
    distancias = np.zeros((num_ciudades, num_ciudades))

    for line in data:
        partes = line.split()
        i = int(partes[1]) - 1
        j = int(partes[2]) - 1
        distancia = float(partes[3])
        distancias[i][j] = distancia
        distancias[j][i] = distancia  # Asumimos que la distancia es simétrica

    return distancias


def calcular_num_iteraciones(distancias, max_distancia):
    num_ciudades = len(distancias)
    mejor_iteracion = 0
    mejor_ruta = None
    mejor_distancia = 0

    for iteracion in range(2, num_ciudades + 1):
        ruta, distancia = metodo_aco(distancias, iteracion)
        if distancia <= max_distancia:
            mejor_iteracion = iteracion
            mejor_ruta = ruta
            mejor_distancia = distancia
        else:
            break

    return mejor_iteracion, mejor_ruta, mejor_distancia


def metodo_aco(distancias, num_ciudades):
    num_hormigas = 10
    alfa = 2
    beta = 5
    evaporacion = 0.1
    iteraciones = 500

    pheromones = np.ones((num_ciudades, num_ciudades))

    mejor_ruta = None
    mejor_distancia = float("inf")

    for _ in range(iteraciones):
        rutas = []
        for _ in range(num_hormigas):
            ruta = [random.randint(0, num_ciudades - 1)]
            while len(ruta) < num_ciudades:
                current = ruta[-1]
                probabilidades = [
                    (
                        (pheromones[current][j] ** alfa)
                        * ((1 / distancias[current][j]) ** beta)
                        if j not in ruta
                        else 0
                    )
                    for j in range(num_ciudades)
                ]
                siguiente = random.choices(
                    range(len(probabilidades)), weights=probabilidades
                )[0]
                ruta.append(siguiente)
            ruta.append(ruta[0])
            rutas.append(ruta)

        distancias_rutas = [
            sum(distancias[ruta[i - 1], ruta[i]] for i in range(1, len(ruta)))
            for ruta in rutas
        ]
        mejor_idx = np.argmin(distancias_rutas)
        if distancias_rutas[mejor_idx] < mejor_distancia:
            mejor_ruta = rutas[mejor_idx]
            mejor_distancia = distancias_rutas[mejor_idx]

        pheromones *= 1 - evaporacion
        for ruta in rutas:
            for i in range(len(ruta) - 1):
                pheromones[ruta[i]][ruta[i + 1]] += 1 / distancias[ruta[i]][ruta[i + 1]]

    return mejor_ruta, mejor_distancia


# Código principal
distancias = leer_distancias("DIST100.TXT")
max_distancia = 15000

# Añadir impresiones para depurar
print("Iniciando búsqueda de la mejor ruta...")
num_iteraciones, mejor_ruta, mejor_distancia = calcular_num_iteraciones(
    distancias, max_distancia
)
print(f"Cantidad máxima de iteraciones: {num_iteraciones}")
print(f"Mejor ruta: {mejor_ruta}")
print(f"Distancia recorrida: {mejor_distancia} km.")
