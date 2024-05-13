(deftemplate combinacion
  (slot letra)
  (slot numero (type INTEGER))
)

(defrule definicion_de_hechos_iniciales
  =>
  (printout t "============== Inicio de la ejecución =============" crlf)
  (printout t "Mensaje: SAL+MAS=ALLA" crlf)
  (printout t "Sin acarreo: 100*S+10*A+L+100*M+10*A+S = 1000*A+100*L+10*L+A" crlf)
  (printout t "A = 1 pues dos numeros de tres cifras da como maximo 1998 = 999+999" crlf)
  (printout t "S y M no pueden ser 0, pues comienzan una palabra" crlf)
  (printout t "Como L+S = A (+10) = 11, puesto que A = 1 y debe sumársele 10, caso contrario," crlf
   "S debiera ser 1 y L, 0. Pero A = 1 y todas las letras representan numeros distintos. Luego," crlf
    "el numero 0 queda descartado" crlf)
  (printout t "===================================================" crlf)
  (assert (numero_valido 2))
  (assert (numero_valido 3))
  (assert (numero_valido 4))
  (assert (numero_valido 5))
  (assert (numero_valido 6))
  (assert (numero_valido 7))
  (assert (numero_valido 8))
  (assert (numero_valido 9))
  (assert (letra S))
  (assert (letra A))
  (assert (letra L))
  (assert (letra M))
  (assert (combinacion (letra A) (numero 1)))
)

(defrule combinaciones 
  (letra ?letra&~A)
  (numero_valido ?num)
  =>
  (assert (combinacion (letra ?letra) (numero ?num)))
)

(defrule func_objetivo 
  ;comenzamos por las unidades
  (combinacion (letra A) (numero ?numA)) ;lo traigo aqui para usar de referencia
  (combinacion (letra L) (numero ?numL&~?numA)) 
  (combinacion (letra S) (numero ?numS&~?numL&~?numA))
  (test (= (mod (+ ?numL ?numS) 10) ?numA)) ;mod 10 debe dar A = 1;

  ;combinacion para las decenas:
  (test (= (mod (+ (* 20 ?numA) ?numL ?numS) 100) (+ (* 10 ?numL) ?numA)))

  ;el resto de la division entera para 20A+L+S debe ser 10L+A
  ;combinacion para las centenas:
  (combinacion (letra M) (numero ?numM&~?numS&~?numL&~?numA))
  (test (= (mod (+ (* 100 (+ ?numS ?numM)) (* 20 ?numA) ?numL ?numS) 1000) (+ (* 110 ?numL) ?numA)))
  =>
  (printout t "Una solucion posible es:" crlf)
  (printout t "A = " ?numA ", ")
  (printout t "L = " ?numL ", ")
  (printout t "S = " ?numS ", ")
  (printout t "M = " ?numM ", " crlf)
  (printout t "SAL+MAS=ALLA" crlf)
  (printout t ?numS ?numA ?numL"+" ?numM ?numA ?numS"="?numA ?numL ?numL ?numA crlf)
  (halt)
)