from sko.GA import GA_TSP
from Trayecto import MatrizTrayectos

matriz_trayectos = MatrizTrayectos()
matriz_trayectos.crear_matriz_distancias()
# matriz_trayectos.mostrar_matriz_distancias()
matriz_distancias = matriz_trayectos.get_matriz()

# Función aptitud(fitness) para calcular la distancia total de una ruta
def cal_total_distance(ruta):
    total_distance = 0
    for i in range(len(ruta)):
        total_distance += matriz_distancias[ruta[i-1]][ruta[i]]
    return total_distance

# Instancia de GA para TSP (Población = 100, Generaciones = 1500, Prob Mutacion = 0.2)
ga_tsp = GA_TSP(func=cal_total_distance, n_dim=100, size_pop=100, max_iter=1500, prob_mut=0.2)

#Se obtiene la mejor ruta conformada por todas las ciudades y la mejor distancia.
mejor_ruta, mejor_distancia = ga_tsp.run()

print("===============================Algoritmos Geneticos===============================")
print(f"Mejor distancia encontrada: {mejor_distancia} km.")
print(f"Mejor ruta encontrada: {mejor_ruta}")