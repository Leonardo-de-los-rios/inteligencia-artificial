import random

import matplotlib.pyplot as plt
import numpy as np
from deap import algorithms, base, creator, tools

# Definición del problema de optimización
ANCHO = 10

def input_rectangulos():
    num_rectangulos = int(input("Ingrese la cantidad de rectángulos: "))
    rectangulos = []
    for i in range(num_rectangulos):
        ancho = int(input(f"Ingrese el ancho del rectángulo {i + 1}: "))
        alto = int(input(f"Ingrese el alto del rectángulo {i + 1}: "))
        rectangulos.append((ancho, alto))
    return rectangulos

rectangulos = input_rectangulos()

# Crear el tipo de individuo
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=len(rectangulos)*2)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def eval_distribucion(individual):
    distribucion = []
    ancho_actual = 0
    alto_actual = 0
    max_alto = 0
    for i in range(0, len(individual), 2):
        indice_rect = i // 2
        rect_ancho, rect_alto = rectangulos[indice_rect]
        if individual[i] == 1:  # Rotar rectángulo
            rect_ancho, rect_alto = rect_alto, rect_ancho
        if ancho_actual + rect_ancho > ANCHO:
            alto_actual += max_alto
            ancho_actual = 0
            max_alto = 0
        if alto_actual == 0:
            max_alto = max(max_alto, rect_alto)
        distribucion.append((ancho_actual, alto_actual, rect_ancho, rect_alto))
        ancho_actual += rect_ancho
    alto_total = alto_actual + max_alto
    area_utilizada = sum(w * h for _, _, w, h in distribucion)
    area_total = ANCHO * alto_total
    area_sin_usar = area_total - area_utilizada
    return area_sin_usar,

toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", eval_distribucion)

def main():
    random.seed(42)
    poblacion = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    estadisticas = tools.Statistics(lambda ind: ind.fitness.values)
    estadisticas.register("avg", np.mean)
    estadisticas.register("std", np.std)
    estadisticas.register("min", np.min)
    estadisticas.register("max", np.max)

    algorithms.eaSimple(poblacion, toolbox, cxpb=0.5, mutpb=0.2, ngen=50, stats=estadisticas, halloffame=hof, verbose=True)
    
    mejor_ind = hof[0]
    print("El mejor individuo es: %s\ncon fitness: %s" % (mejor_ind, mejor_ind.fitness.values))
    
    distribucion = []
    ancho_actual = 0
    alto_actual = 0
    max_alto = 0
    for i in range(0, len(mejor_ind), 2):
        indice_rect = i // 2
        rect_ancho, rect_alto = rectangulos[indice_rect]
        if mejor_ind[i] == 1:  # Rotar rectángulo
            rect_ancho, rect_alto = rect_alto, rect_ancho
        if ancho_actual + rect_ancho > ANCHO:
            alto_actual += max_alto
            ancho_actual = 0
            max_alto = 0
        if alto_actual == 0:
            max_alto = max(max_alto, rect_alto)
        distribucion.append((ancho_actual, alto_actual, rect_ancho, rect_alto))
        ancho_actual += rect_ancho
    alto_total = alto_actual + max_alto
    
    print(f"Área total utilizada: {ANCHO * alto_total}")
    print(f"Área sin usar: {mejor_ind.fitness.values[0]}")
    print(f"Altura total de la distribución: {alto_total}")

    fig, ax = plt.subplots()
    for (x, y, w, h) in distribucion:
        ax.add_patch(plt.Rectangle((x, y), w, h, edgecolor='black', facecolor='blue', alpha=0.5))
    ax.set_xlim(0, ANCHO)
    ax.set_ylim(0, alto_total)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

if __name__ == "__main__":
    main()
