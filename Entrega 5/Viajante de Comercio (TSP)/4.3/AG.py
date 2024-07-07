import numpy as np
from sko.GA import GA_TSP


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


def calcular_ndim(distancias, max_distancia):
    num_ciudades = len(distancias)
    mejor_ndim = 0
    mejor_ruta = None
    mejor_distancia = 0

    for ndim in range(2, num_ciudades + 1):
        ruta, distancia = metodo_genetico(distancias, ndim)
        if distancia <= max_distancia:
            mejor_ndim = ndim
            mejor_ruta = ruta
            mejor_distancia = distancia
        else:
            break

    return mejor_ndim, mejor_ruta, mejor_distancia


def metodo_genetico(distancias, ndim):
    num_points = ndim

    def cal_total_distance(routine):
        routine = np.concatenate([routine, [routine[0]]])
        return sum(
            [
                distancias[routine[i % num_points], routine[(i + 1) % num_points]]
                for i in range(num_points)
            ]
        )

    ga_tsp = GA_TSP(
        func=cal_total_distance,
        n_dim=num_points,
        size_pop=50,
        max_iter=500,
        prob_mut=0.1,
    )
    best_points, best_distance = ga_tsp.run()

    best_route = np.concatenate([best_points, [best_points[0]]])
    return best_route, best_distance


# Main
distancias = leer_distancias("DIST100.TXT")
max_distancia = 15000
ndim, mejor_ruta, mejor_distancia = calcular_ndim(distancias, max_distancia)
print(f"Cantidad máxima de ciudades: {ndim}")
print(f"Mejor ruta: {mejor_ruta}")
print(f"Distancia recorrida: {mejor_distancia} km.")
