class Camino:
    __id_camino = 0
    __ciudades = ''
    __km = 0
    __duracion = 0
    __peaje = bool
    __trafico = 0.0
    __h = 0.0                   #heuristica
    def __init__(self, id_camino, ciudades, km, duracion, peaje, trafico):
        self.__id_camino = id_camino
        self.__ciudades = ciudades
        self.__km = km
        self.__duracion = duracion
        self.__peaje = peaje
        self.__trafico = trafico

    def get_id_camino(self):
        return self.__id_camino

    def get_ciudades(self):
        return self.__ciudades

    def get_km(self):
        return self.__km

    def get_duracion(self):
        return self.__duracion

    def get_peaje(self):
        return self.__peaje

    def get_trafico(self):
        return self.__trafico

    def peso_ciudades (self):
        acumulador = 0
        lista_ciudades = self.__ciudades.split('-')
        for ciudad in lista_ciudades:
            if ciudad == "San Luis":
                acumulador += 1
            elif ciudad == "San Juan" or ciudad == "Villa Mercedes":
                acumulador += 0.8
            elif ciudad == "Villa Dolores":
                acumulador += 0.6
            elif ciudad == "Caucete":
                acumulador += 0.4    
            elif ciudad == "Mina Clavero":
                acumulador += 0.2
            elif ciudad == "Chepes":
                acumulador += 0.2       
            elif ciudad == "Quines":
                acumulador += 0.1
            elif ciudad == "Taninga":
                acumulador += 0.01
            else:             #para el caso de las rutas,no influye la ciudad en el transito
                acumulador += 0.01
        return acumulador

    def heuristica_camino (self):
        if self.__peaje == True:
            self.__h= (self.__km * 0.6) + (self.peso_ciudades()) + (self.__duracion * 1) + 0.2 + (self.__trafico * 0.4) 
        else:
            self.__h= (self.__km * 0.6) + (self.peso_ciudades()) + (self.__duracion * 1) + (self.__trafico * 0.4) 
        
        self.__h = round(self.__h, 2)

    def get_heuristica_camino (self):
        return self.__h

    def __lt__ (self, otro):           #sobrecarga para ordenar caminos
        if type(self) == type(otro):
            return self.get_heuristica_camino() < otro.get_heuristica_camino()
