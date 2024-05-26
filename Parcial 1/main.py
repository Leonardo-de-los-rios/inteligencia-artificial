import random

import matplotlib.pyplot as plt
import numpy as np

# Definición de los subrectángulos
subrectangulos = [(1,1),(2,3),(3,4),(7,3),(8,3)] # Población 4000 - Generaciones 50
# subrectangulos = [(1,1),(1,1),(1,1),(1,1),(1,1),(1,1),(1,1),(1,1),(1,1),(1,1)] # Población 1000 - Generaciones 100
# subrectangulos = [(1,1),(10,9),(9,1)] # Población 2000 - Generaciones 1
# subrectangulos = [(2,2),(3,3),(1,1),(4,4)] # Población 2000 - Generaciones 20
# subrectangulos = [(5,1), (6,1)] # Población 10 - Generaciones 1000

# Dimensiones del contenedor
contenedor_ancho = 10
contenedor_alto = 10

# Parámetros del algoritmo genético
probabilidad_seleccion = 1
probabilidad_crossover = 0.8
probabilidad_mutacion = 0.01
poblacion_tamano = 4000
generaciones = 50

def generar_individuo(subrectangulos, contenedor_ancho, contenedor_alto):
    individuo = []

    # creacion de individuos aleatorios pero que entren en el contenedor
    for ancho, alto in subrectangulos:
        x = random.randint(0, contenedor_ancho - ancho)
        y = random.randint(0, contenedor_alto - alto)
        individuo.append((x, y, ancho, alto))

    return individuo

def inicializar_poblacion(tamano, subrectangulos, contenedor_ancho, contenedor_alto):
    return [generar_individuo(subrectangulos, contenedor_ancho, contenedor_alto) for _ in range(tamano)]

def solapamiento(individuo):
    matriz_aux = np.zeros((contenedor_ancho, contenedor_alto))
    solapamientos = 0
    
    for x, y, ancho, alto in individuo:
        for i in range(alto*ancho):
            x_aux = x + i%ancho
            y_aux = y + i//ancho
            if(matriz_aux[contenedor_alto-y_aux-1][x_aux] == 0):
                matriz_aux[contenedor_alto-y_aux-1][x_aux] = 1
            else:
                solapamientos += 1
        
    return solapamientos

def altura_maxima_individuo(individuo):
    return max(y + alto for _, y, _, alto in individuo)

def calcular_fitness(individuo, contenedor_alto):
    penalizacion_solapamiento = 999999999  # Penalización por solapamiento alta
    altura_maxima = altura_maxima_individuo(individuo) # altura del subrectángulo más alto
    penalizacion = 0
    aptitud = 0
    acum_superficie = 0
    
    solapamientos = solapamiento(individuo)
    penalizacion = penalizacion_solapamiento*solapamientos
    
    for _, y, ancho, alto in individuo:
        for i in range(alto):
            acum_superficie += ancho*abs(contenedor_alto-y-i)

    aptitud = (contenedor_alto - altura_maxima)*10000 + acum_superficie - penalizacion

    return aptitud

def seleccion(poblacion, contenedor_alto):
    # Selección por torneo
    seleccionados = []
    for _ in range(len(poblacion)):
        i, j = random.sample(range(len(poblacion)), 2)
        if calcular_fitness(poblacion[i], contenedor_alto) > calcular_fitness(poblacion[j], contenedor_alto):
            seleccionados.append(poblacion[i])
        else:
            seleccionados.append(poblacion[j])
    return seleccionados

def crossover(ind1, ind2):
    if random.random() < probabilidad_crossover:
        punto = random.randint(1, len(ind1) - 1)
        hijo1 = ind1[:punto] + ind2[punto:]
        hijo2 = ind2[:punto] + ind1[punto:]
        return hijo1, hijo2
    return ind1, ind2

def mutacion(individuo, contenedor_ancho, contenedor_alto):
    for i in range(len(individuo)):
        if random.random() < probabilidad_mutacion:
            x = random.randint(0, contenedor_ancho - individuo[i][2])
            y = random.randint(0, contenedor_alto - individuo[i][3])
            individuo[i] = (x, y, individuo[i][2], individuo[i][3])
    return individuo

def algoritmo_genetico(subrectangulos, contenedor_ancho, contenedor_alto, generaciones):
    poblacion = inicializar_poblacion(poblacion_tamano, subrectangulos, contenedor_ancho, contenedor_alto)
    mejor_fitness_global = float('-inf')
    mejor_individuo = None
    historial_fitness = []
    mejor_generacion = 0

    for generacion in range(generaciones):
        poblacion = seleccion(poblacion, contenedor_alto)
        nueva_poblacion = []

        for i in range(0, len(poblacion), 2):
            ind1, ind2 = poblacion[i], poblacion[i + 1]
            hijo1, hijo2 = crossover(ind1, ind2)
            nueva_poblacion.append(mutacion(hijo1, contenedor_ancho, contenedor_alto))
            nueva_poblacion.append(mutacion(hijo2, contenedor_ancho, contenedor_alto))
        
        poblacion = nueva_poblacion

        # Evaluar y encontrar el mejor individuo
        mejor_individuo_actual = None
        mejor_fitness_actual = float('-inf')
        for individuo in poblacion:
            fitness = calcular_fitness(individuo, contenedor_alto)
            if fitness >= mejor_fitness_actual:
                mejor_fitness_actual = fitness
                mejor_individuo_actual = individuo
        
        historial_fitness.append(mejor_fitness_actual)
        print(f"Generación {generacion + 1}: {mejor_individuo_actual} Mejor Fitness = {mejor_fitness_actual}")

        # Actualizar la mejor solución global encontrada
        if mejor_fitness_actual >= mejor_fitness_global:
            if mejor_fitness_actual > mejor_fitness_global:
                mejor_generacion = generacion + 1
                print(f"\nMejor solución encontrada. Generación: {mejor_generacion} - Aptitud: {mejor_fitness_actual}\n")
            mejor_fitness_global = mejor_fitness_actual
            mejor_individuo = mejor_individuo_actual

    print("\nLa mejor solución global se encontró en la generación: ", mejor_generacion)
    print(f"Mejor Solución encontrada: {mejor_individuo} con aptitud {mejor_fitness_global}")
    print("Altura maxima del individuo: ", altura_maxima_individuo(mejor_individuo))
    return mejor_individuo, mejor_fitness_global, historial_fitness


def graficar_resultado(mejor_individuo, historial_fitness, contenedor_ancho, contenedor_alto):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Grafica del mejor individuo
    for rect in mejor_individuo:
        x, y, ancho, alto = rect
        ax1.add_patch(plt.Rectangle((x, y), ancho, alto, edgecolor='blue', facecolor='blue', alpha=0.5))
    ax1.set_xlim(0, contenedor_ancho)
    ax1.set_ylim(0, contenedor_alto)
    ax1.set_aspect('equal')

    # Dibujar la línea roja a la altura del subrectángulo más alto
    altura_maxima = altura_maxima_individuo(mejor_individuo)
    ax1.axhline(y=altura_maxima, color='red', linestyle='--')

    ax1.set_title('Mejor Solución')

    if historial_fitness:
        # Grafica de la evolución del fitness
        ax2.plot(historial_fitness)
        ax2.set_title('Evolución de la Aptitud')
        ax2.set_xlabel('Generaciones')
        ax2.set_ylabel('Aptitud')
        ax2.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    mejor_individuo, mejor_fitness, historial_fitness = algoritmo_genetico(subrectangulos, contenedor_ancho, contenedor_alto, generaciones)
    graficar_resultado(mejor_individuo, historial_fitness, contenedor_ancho, contenedor_alto)

# tests
# individuo = [(3, 6, 1, 1), (8, 0, 2, 3), (7, 3, 3, 4), (1, 6, 7, 3), (0, 0, 8, 3)]
# fitness = calcular_fitness(individuo, contenedor_alto)
# print("Fitness: ", fitness)
# graficar_resultado(individuo, None, contenedor_ancho, contenedor_alto)

# individuo = [(8, 0, 2, 3), (8, 0, 1, 1)]
# solapamiento = solapamiento(individuo)
# print("Solapamiento: ", solapamiento)