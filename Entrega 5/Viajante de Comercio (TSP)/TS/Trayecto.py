class Trayecto:
    def __init__(self, ciudad_origen, ciudad_destino, distancia):
        self.__ciudad_origen = ciudad_origen
        self.__ciudad_destino = ciudad_destino
        self.__distancia = distancia
    def getOrigen (self):
        return self.__ciudad_origen
    def getDestino (self):
        return self.__ciudad_destino
    def getDistancia (self):
        return self.__distancia

class MatrizTrayectos:
    def __init__(self):
        self.__n = 100
        self.__trayectos = []
        with open ("DIST100.TXT", 'r') as f:
            for linea in f:
                partes = linea.split()
                self.__trayectos.append(Trayecto(int(partes[1]), int(partes[2]), float(partes[3])))

    def crear_matriz_distancias(self):
        self.__matriz = [[0]*self.__n for _ in range(self.__n)]          #crea una matriz bidireccional nxn [n][n]
        for trayecto in self.__trayectos:
            self.__matriz[trayecto.getOrigen() - 1][trayecto.getDestino() - 1] = trayecto.getDistancia()
            self.__matriz[trayecto.getDestino() - 1][trayecto.getOrigen() - 1] = trayecto.getDistancia()  # Simétrica

    def mostrar_matriz_distancias(self):
        for orig in range(self.__n):
            for dest in range(self.__n):
                print(f"Origen:{orig+1} - Destino: {dest+1} - Distancia: {self.__matriz[orig][dest]}")
            print("\n")

    def get_matriz (self):
        return self.__matriz
