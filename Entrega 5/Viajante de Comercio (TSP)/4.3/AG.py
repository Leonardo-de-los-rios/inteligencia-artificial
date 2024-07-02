from sko.GA import GA_TSP
import numpy as np

def leer_distancias(filename, num_ciudades):
    '''Lee un archivo de texto que contiene la distancia que separa cada una de las
    ciudades, desde el archivo filename. La matriz resultante que devuelve pordra
    ser simetrica o no, dependiendo de si no es lo mismo ir de A a B que de B a A'''
    distancias= np.zeros((num_ciudades,num_ciudades))
    with open(filename, 'r') as file: 
        for line in file:
            partes = line.split()
            distancias[int(partes[1])-1][int(partes[2])-1] = float(partes[3])
    return distancias

# Función aptitud(fitness) para calcular la distancia total de una ruta
def cal_total_distance(ruta):
    limite_distancia = 15000
    total_distance = 0
    for i in range(1,len(ruta)):
        total_distance += matriz_distancias[ruta[i-1]][ruta[i]]
    if total_distance > limite_distancia:
        total_distance = 10000000
    return total_distance


#Main
num_ciudades = 100
matriz_distancias = leer_distancias("DIST100.txt", num_ciudades)
#print(matriz_distancias)
ndim = 50
mutacion = 0.3
niter = 1500
size = 50
print("===============================Algoritmos Geneticos===============================")
print(f"Numero de ciudades testeado:",ndim, ". Probabilidad de mutacion: ", mutacion, "Iteraciones: ", niter, ". Population", size)
# Instancia de GA para TSP (Población = 50, Generaciones = 1500, Prob Mutacion = 0.3)
ga_tsp = GA_TSP(func=cal_total_distance, n_dim=ndim, size_pop=size, max_iter=niter, prob_mut=mutacion)

#Se obtiene la mejor ruta conformada por todas las ciudades y la mejor distancia.
mejor_ruta, mejor_distancia = ga_tsp.run()

for i in range(len(mejor_ruta)):
    mejor_ruta[i] += 1

print(f"Mejor distancia encontrada: {mejor_distancia} km.")
print(f"Mejor ruta encontrada: {mejor_ruta}")