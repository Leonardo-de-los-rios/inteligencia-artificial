import random
from itertools import combinations

import matplotlib.pyplot as plt

CONTAINER_WIDTH = 10
CONTAINER_HEIGHT = 10
RECTANGLE_SIZES = [1, 2, 3, 4, 5]

def generate_random_solution():
    solution = []
    for size in RECTANGLE_SIZES:
        x = random.randint(0, CONTAINER_WIDTH - size)
        # Forzamos y a 0 para que esté pegado al borde superior
        y = 0
        solution.append((x, y, size, size))
    return solution

def check_overlap(rect1, rect2):
    x_overlap = max(0, min(rect1[0] + rect1[2], rect2[0] + rect2[2]) - max(rect1[0], rect2[0]))
    y_overlap = max(0, min(rect1[1] + rect1[3], rect2[1] + rect2[3]) - max(rect1[1], rect2[1]))
    return x_overlap > 0 and y_overlap > 0

def get_top_enclosed_area(solution):
    highest_top = max(rect[1] + rect[3] for rect in solution)
    top_enclosed_area = 0
    for x in range(CONTAINER_WIDTH):
        is_obstructed = False
        for rect in solution:
            if rect[0] <= x < rect[0] + rect[2] and rect[1] <= highest_top:
                is_obstructed = True
                break
        if is_obstructed:
            top_enclosed_area += 1
    return top_enclosed_area

def evaluate_solution(solution):
    total_area = CONTAINER_WIDTH * CONTAINER_HEIGHT
    covered_area = sum(rect[2] * rect[3] for rect in solution)
    uncovered_area = total_area - covered_area
    
    # Calcular espacio encerrado entre la parte superior del contenedor y el subrectángulo más alto
    highest_top = max(rect[1] + rect[3] for rect in solution)
    top_enclosed_area = get_top_enclosed_area(solution)
    
    # Calcular espacio encerrado entre subrectángulos
    enclosed_area_between_rectangles = 0
    for rect1, rect2 in combinations(solution, 2):
        x_overlap = max(0, min(rect1[0] + rect1[2], rect2[0] + rect2[2]) - max(rect1[0], rect2[0]))
        y_overlap = max(0, min(rect1[1] + rect1[3], rect2[1] + rect2[3]) - max(rect1[1], rect2[1]))
        enclosed_area_between_rectangles += x_overlap * y_overlap
    
    # Calcular espacio encerrado entre subrectángulos y contenedor
    enclosed_area_between_container_and_rectangles = 0
    for rect in solution:
        # Espacio a la izquierda del subrectángulo
        if rect[0] > 0:
            enclosed_area_between_container_and_rectangles += rect[0] * rect[3]
        # Espacio a la derecha del subrectángulo
        if rect[0] + rect[2] < CONTAINER_WIDTH:
            enclosed_area_between_container_and_rectangles += (CONTAINER_WIDTH - rect[0] - rect[2]) * rect[3]
        # Espacio debajo del subrectángulo
        if rect[1] > 0:
            enclosed_area_between_container_and_rectangles += rect[2] * rect[1]
    
    # Calcular desperdicio total
    waste = highest_top * CONTAINER_WIDTH - covered_area
    
    # Calcular penalización por solapamiento
    penalty = 0
    for rect1, rect2 in combinations(solution, 2):
        if check_overlap(rect1, rect2):
            penalty += 1000
    
    aptitud = waste + penalty + enclosed_area_between_rectangles + enclosed_area_between_container_and_rectangles
    return aptitud, uncovered_area, top_enclosed_area

def mutate_solution(solution):
    mutated_solution = solution[:]
    index = random.randint(0, len(mutated_solution) - 1)
    rect = mutated_solution[index]
    new_x = random.randint(0, CONTAINER_WIDTH - rect[2])
    new_y = random.randint(0, CONTAINER_HEIGHT - rect[3])
    mutated_solution[index] = (new_x, new_y, rect[2], rect[3])
    return mutated_solution

def generate_initial_population(population_size):
    population = [generate_random_solution() for _ in range(population_size)]
    return population

def tournament_selection(population, tournament_size):
    tournament = random.sample(population, tournament_size)
    best_solution = min(tournament, key=lambda x: evaluate_solution(x)[0])
    return best_solution

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

def genetic_algorithm(population_size, generations, stop_condition=10):
    population = generate_initial_population(population_size)
    for _ in range(generations):
        new_population = []
        for _ in range(population_size):
            parent1 = tournament_selection(population, 5)
            parent2 = tournament_selection(population, 5)
            child = crossover(parent1, parent2)
            if random.random() < 0.1:
                child = mutate_solution(child)
            new_population.append(child)
        population = new_population
        best_solution = min(population, key=lambda x: evaluate_solution(x)[0])
        if evaluate_solution(best_solution)[0] < stop_condition:
            break
    return best_solution

def visualize_solution(solution):
    plt.figure(figsize=(5, 5))
    plt.gca().add_patch(plt.Rectangle((0, 0), CONTAINER_WIDTH, CONTAINER_HEIGHT, edgecolor='b', facecolor='none'))
    for rect in solution:
        plt.gca().add_patch(plt.Rectangle((rect[0], rect[1]), rect[2], rect[3], edgecolor='r', facecolor='none'))
    plt.xlim(0, CONTAINER_WIDTH)
    plt.ylim(0, CONTAINER_HEIGHT)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

best_solution = genetic_algorithm(population_size=100, generations=100, stop_condition=10)
desperdicio, espacios_huecos, espacio_encerrado_contenedor = evaluate_solution(best_solution)
print("Mejor solución encontrada:", best_solution)
print("Desperdicio:", desperdicio)
print("espacios_huecos:", espacios_huecos)
print("Espacio encerrado entre subrectángulos y contenedor:", espacio_encerrado_contenedor)
visualize_solution(best_solution)
