import csv
from claseCamino import Camino
class ListaCamino:
    __listaCamino = []
    def __init__ (self):
        self.__listaCamino = []
    def agregarCamino (self, camino):
        self.__listaCamino.append(camino)

    def testListaCamino (self):
        archivo = open ('tabla.csv', 'r')
        Reader = csv.reader (archivo, delimiter=';')
        band = True
        for fila in Reader:
            #fila[0] es Identificador del camino, fila[1] es Ciudades, fila[2] es Km, fila[3] es Duración;fila[4] es Peajes;fila[5] es Tráfico
            if band:
                #salteamos la cabecera
                band = not band
            else:
                id_c = int(fila[0])
                ciudades = fila[1]
                km = int(fila[2])
                duracion = int(fila[3])
                peaje = bool(fila[4])
                trafico = float(fila[5])
                camino = Camino (id_c,ciudades,km,duracion,peaje,trafico)
                self.agregarCamino(camino)              
        archivo.close()
    
    def calcular_heuristica (self):
        for camino in self.__listaCamino:
            camino.heuristica_camino()
        self.__listaCamino.sort()       #ordeno la lista en forma ascendente

    def mostrar_caminos (self):
        for camino in self.__listaCamino:
            print(f"Id Camino: {camino.get_id_camino()}\nCiudades: {camino.get_ciudades()}\nKilometros: {camino.get_km()} km\nDuracion: {camino.get_duracion()} min\nPeaje: {camino.get_peaje()}\n")
            print(f"Peso heuristica: {camino.get_heuristica_camino()}")
            print("==================================================================")

if __name__ == '__main__':
    lista = ListaCamino()
    lista.testListaCamino()
    lista.calcular_heuristica()
    print("Se muestra la lista de caminos posibles ordenadas por heurística:\n")
    print("==================================================================")
    lista.mostrar_caminos()
