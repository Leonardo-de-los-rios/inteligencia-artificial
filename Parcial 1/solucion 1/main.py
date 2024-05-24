import random

import matplotlib.pyplot as plt
import numpy as np
from deap import algorithms, base, creator, tools

# Definición del problema de optimización
WIDTH = 10

def input_rectangles():
    num_rectangles = int(input("Ingrese la cantidad de rectángulos: "))
    rectangles = []
    for i in range(num_rectangles):
        width = int(input(f"Ingrese el ancho del rectángulo {i + 1}: "))
        height = int(input(f"Ingrese el alto del rectángulo {i + 1}: "))
        rectangles.append((width, height))
    return rectangles

rectangles = input_rectangles()

# Crear el tipo de individuo
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=len(rectangles)*2)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def eval_layout(individual):
    layout = []
    current_width = 0
    current_height = 0
    max_height = 0
    for i in range(0, len(individual), 2):
        rect_index = i // 2
        rect_width, rect_height = rectangles[rect_index]
        if individual[i] == 1:  # Rotate rectangle
            rect_width, rect_height = rect_height, rect_width
        if current_width + rect_width > WIDTH:
            current_height += max_height
            current_width = 0
            max_height = 0
        if current_height == 0:
            max_height = max(max_height, rect_height)
        layout.append((current_width, current_height, rect_width, rect_height))
        current_width += rect_width
    total_height = current_height + max_height
    used_area = sum(w * h for _, _, w, h in layout)
    total_area = WIDTH * total_height
    unused_area = total_area - used_area
    return unused_area

toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", eval_layout)

def main():
    random.seed(42)
    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=50, stats=stats, halloffame=hof, verbose=True)
    
    best_ind = hof[0]
    print("Best individual is: %s\nwith fitness: %s" % (best_ind, best_ind.fitness.values))
    
    layout = []
    current_width = 0
    current_height = 0
    max_height = 0
    for i in range(0, len(best_ind), 2):
        rect_index = i // 2
        rect_width, rect_height = rectangles[rect_index]
        if best_ind[i] == 1:  # Rotate rectangle
            rect_width, rect_height = rect_height, rect_width
        if current_width + rect_width > WIDTH:
            current_height += max_height
            current_width = 0
            max_height = 0
        if current_height == 0:
            max_height = max(max_height, rect_height)
        layout.append((current_width, current_height, rect_width, rect_height))
        current_width += rect_width
    total_height = current_height + max_height
    
    print(f"Total area used: {WIDTH * total_height}")
    print(f"Unused area: {best_ind.fitness.values[0]}")
    print(f"Total height of the layout: {total_height}")

    fig, ax = plt.subplots()
    for (x, y, w, h) in layout:
        ax.add_patch(plt.Rectangle((x, y), w, h, edgecolor='black', facecolor='blue', alpha=0.5))
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, total_height)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

if __name__ == "__main__":
    main()
