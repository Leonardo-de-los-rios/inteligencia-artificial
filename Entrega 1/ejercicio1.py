def ecuacion(x, y):
    return 2**x + 3**y

def buscarSolucion_3_decimales():
    minimo_error = 9999999999                                 # Minimo error con un valor infinito
    x= -10.0
    while x <= 0:
        y = -10.0
        while y <= 0:
            suma = ecuacion(x,y)
            error = abs(suma - 1)                               # Error absoluto
            if error < minimo_error:  
                minimo_error = error  
                mejor_solucion = (round(x,3), round(y,3), minimo_error)
            y += 0.001
        x += 0.001
    return mejor_solucion

def buscarSolucion_5_decimales(x_inicial, x_final, y_inicial, y_final):
    minimo_error = 99999999999 
    x= x_inicial
    while x <= x_final:                 
        y = y_inicial
        while y <= y_final:                                     #se acota rango de x e y en función de la solución con 3 decimales
            suma = ecuacion(x,y)
            error = abs(suma - 1)  
            if error < minimo_error:  
                minimo_error = error  
                mejor_solucion = (round(x,5), round(y,5), minimo_error)
            y += 0.00001
        x += 0.00001
    return mejor_solucion

if __name__ == '__main__':
    mejorSolucion = buscarSolucion_3_decimales()
    valor_x = mejorSolucion[0]
    valor_y = mejorSolucion[1]
    if mejorSolucion:
        print("Mejor solución encontrada con 3 decimales:")
        print("x =", valor_x, ", y =", valor_y, "con un error de = ", mejorSolucion[2])

    otraSolucion = buscarSolucion_5_decimales(valor_x-0.001, valor_x+0.001, valor_y-0.001, round(valor_y+0.001,3))
    if otraSolucion:
        print("\nMejor solución encontrada con 5 decimales:")
        print("x =", otraSolucion[0], ", y =", otraSolucion[1], "con un error de = ", otraSolucion[2])

