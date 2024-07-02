from Trayecto import MatrizTrayectos
import random

matriz_trayectos = MatrizTrayectos()
matriz_trayectos.crear_matriz_distancias()
dist_matrix = matriz_trayectos.get_matriz()

# Función objetivo (minimización de ruta). Se trabaja en tabu_search
def calculate_total_distance(route, dist_matrix):
    total_distance = 0
    for i in range(len(route)):
        total_distance += dist_matrix[route[i-1]][route[i]]
    return total_distance

# Algoritmo de Nearest Neighbor para generar una buena solucion inicial
def nearest_neighbor_solution(dist_matrix):
    n = len(dist_matrix)
    start = random.randint(0, n - 1)
    unvisited = set(range(n))
    unvisited.remove(start)
    current = start
    solution = [current]
    
    while unvisited:
        next_city = min(unvisited, key=lambda city: dist_matrix[current][city])
        unvisited.remove(next_city)
        solution.append(next_city)
        current = next_city
    
    return solution

# Generar vecinos mediante un intercambio aleatorio entre dos ciudades, fomentando la exploracion
def generate_neighbors(solution, num_neighbors=100):
    neighbors = []
    for _ in range(num_neighbors):
        i, j = random.sample(range(len(solution)), 2)
        neighbor = solution[:]
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        neighbors.append((neighbor, (i, j)))
    return neighbors

# Función principal que emula e invoca la metaheuristica TS
def tabu_search(dist_matrix, initial_solution, max_iter, tabu_list_length, num_neighbors=100):
    current_solution = initial_solution
    best_solution = current_solution
    best_distance = calculate_total_distance(current_solution, dist_matrix)
    
    tabu_list = []

    for iteration in range(max_iter):
        neighbors = generate_neighbors(current_solution, num_neighbors)
        
        # Se filtran vecinos tabú y aplicar criterio de aspiración
        neighbors = [(neighbor, move) for neighbor, move in neighbors if move not in tabu_list or calculate_total_distance(neighbor, dist_matrix) < best_distance]

        if not neighbors:
            break

        # Se ordenan los vecinos por distancia total
        neighbors.sort(key=lambda x: calculate_total_distance(x[0], dist_matrix))
        best_neighbor, best_move = neighbors[0]
        best_neighbor_distance = calculate_total_distance(best_neighbor, dist_matrix)

        # Actualización de la mejor solución si es necesario
        if best_neighbor_distance < best_distance:
            best_solution = best_neighbor
            best_distance = best_neighbor_distance

        # Actualización de la solución actual y lista tabú
        current_solution = best_neighbor
        tabu_list.append(best_move)
        if len(tabu_list) > tabu_list_length:
            tabu_list.pop(0)

    return best_solution, best_distance

n_cities = 100
max_iterations = 300        # Maxima cantidad de iteraciones
tabu_list_length = 50       # Longitud lista tabu
num_neighbors = 100         # Número de vecinos a generar en cada iteración

# Generar una solución inicial usando Nearest Neighbor y ejecutar la búsqueda tabú
initial_solution = nearest_neighbor_solution(dist_matrix)
best_solution, best_distance = tabu_search(dist_matrix, initial_solution, max_iterations, tabu_list_length, num_neighbors)

print("=============================== Tabu Search ===============================\n")
print(f"Mejor distancia encontrada: {best_distance:.2f} km")
print(f"Mejor ruta encontrada: {best_solution}")
print("\n")