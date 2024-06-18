import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

# Datos iniciales
datos = np.array(
    [
        [2, 8],
        [2, 10],
        [2, 12],
        [2, 15],
        [2, 16],
        [3, 11],
        [3, 13],
        [3, 17],
        [5, 7],
        [5, 19],
        [5, 24],
        [5.5, 5],
        [6, 4],
        [6, 5],
        [6, 7],
        [6, 17],
        [6, 16],
        [6, 19],
        [6, 22],
        [7, 4],
        [7, 6],
        [7, 18],
        [7, 20],
    ]
)

# Centroides iniciales
centroides_iniciales = np.array([[3, 13], [6, 4], [6, 16]])

# Configuración de KMeans
kmeans = KMeans(n_clusters=3, init=centroides_iniciales, n_init=1, max_iter=4)

# Ajuste del modelo
kmeans.fit(datos)

# Resultados
centroides = kmeans.cluster_centers_
etiquetas = kmeans.labels_

# Mostrar valores de los centroides en cada iteración
print("Valores de los centroides en cada iteración:")
for i in range(len(centroides)):
    print(f"Centroide C{i+1}: {centroides[i]}")

# Gráfico de los resultados
plt.figure(figsize=(8, 6))
colores = ["r", "g", "b"]
for i in range(3):
    # Puntos del clúster
    puntos_cluster = datos[etiquetas == i]
    plt.scatter(
        puntos_cluster[:, 0], puntos_cluster[:, 1], c=colores[i], label=f"Cluster {i}"
    )
    # Centroides
    plt.scatter(centroides[i][0], centroides[i][1], c=colores[i], marker="x", s=100)

# Dibujar las líneas perpendiculares que separan los clústeres
x_min, x_max = datos[:, 0].min() - 1, datos[:, 0].max() + 1
y_min, y_max = datos[:, 1].min() - 1, datos[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01), np.arange(y_min, y_max, 0.01))

# Predecir el clúster de cada punto en la malla
Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# Dibujar las fronteras de decisión
plt.contour(
    xx, yy, Z, colors="k", linewidths=0.5
)  # Cambio aquí para solo dibujar las líneas

plt.title("Resultados de KMeans con líneas perpendiculares")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.show()
