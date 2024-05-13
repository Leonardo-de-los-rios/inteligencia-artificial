(deftemplate combinacion
    (slot letra) (slot numero (type INTEGER))
)

(deftemplate comb_acarreos
    (slot ac) (slot valor (type INTEGER))
)

(defrule definicion_de_hechos_iniciales
  =>
  (printout t "============== Inicio de la ejecución =============" crlf)
  (printout t "Mensaje: SAL+MAS=ALLA" crlf "Con acarreo:" crlf)
   (printout t "R3 R2 R1" crlf "  S A L" crlf "+ M A S " crlf "_____________"
    crlf "A L L A " crlf crlf)
  (printout t "A = 1 pues dos numeros de tres cifras da como maximo 1998 = 999+999" crlf)
  (printout t "S y M no pueden ser 0, pues comienzan una palabra" crlf)
  (printout t "Como L+S = A (+10) = 11, puesto que A = 1 y debe sumársele 10," crlf 
  "caso contrario, S debiera ser 1 y L, 0. " crlf 
  "Pero A = 1 y todas las letras representan numeros distintos. Luego," crlf
    "el numero 0 queda descartado" crlf "De los acarreos, R3 = A = 1" crlf)
  (printout t "===================================================" crlf)
  (assert (numero_valido 2))
  (assert (numero_valido 3))
  (assert (numero_valido 4))
  (assert (numero_valido 5))
  (assert (numero_valido 6))
  (assert (numero_valido 7))
  (assert (numero_valido 8))
  (assert (numero_valido 9))
  (assert (acarreo_valido 0))
  (assert (acarreo_valido 1))
  (assert (acarreo R1))
  (assert (acarreo R2))
  (assert (acarreo R3))
  (assert (letra S))
  (assert (letra A))
  (assert (letra L))
  (assert (letra M))
  (assert (combinacion (letra A) (numero 1)))
  (assert( comb_acarreos (ac R3) (valor 1)  ))
)

(defrule combinaciones_numeros 
    (letra ?letra&~A)
    (numero_valido ?num)
    =>
    (assert( combinacion (letra ?letra) (numero ?num)  ))
)

(defrule combinaciones_acarreos
    (acarreo ?r)
    (acarreo_valido ?acr)
    =>
    (assert( comb_acarreos (ac ?r) (valor ?acr)  ))
)

(defrule func_objetivo 
    ;comenzamos por las unidades
    (combinacion (letra A) (numero ?numA)) ;lo traigo aqui para usar de referencia
    (combinacion (letra L) (numero ?numL&~?numA)) 
    (combinacion (letra S) (numero ?numS&~?numL&~?numA))
    (comb_acarreos (ac R1) (valor ?r1))
    (test (= (+ ?numL ?numS)  (+ ?numA (* 10 ?r1) ) ) )

    ;combinacion para las decenas:
    (comb_acarreos (ac R2) (valor ?r2))
    ;2A +R1 = L + 10 R2
    (test (=  (+ (* 2 ?numA) ?r1 ) (+ (* 10 ?r2) ?numL) ) )
    
    ;combinacion para las centenas:
    (combinacion (letra M) (numero ?numM&~?numS&~?numL&~?numA) ) 
    (comb_acarreos (ac R3) (valor ?r3))
    (test (= (+ ?r2 ?numM ?numS )  (+ (* 10 ?r3) ?numL) ) )
    =>
    (printout t "Una solucion posible es:" crlf)
    (printout t "R3 = " ?r3 ", ")
    (printout t "R2 = " ?r2 ", ")
    (printout t "R1 = " ?r1 ", " crlf)
    (printout t "A = " ?numA ", ")
    (printout t "L = " ?numL ", ")
    (printout t "S = " ?numS ", ")
    (printout t "M = " ?numM ", " crlf)
    (printout t "R3 R2 R1" crlf "   S A L" crlf "+ M A S " crlf "_____________" crlf "A L L A " crlf
    crlf)
    (printout t "SAL+MAS=ALLA" crlf)
    (printout t ?numS ?numA ?numL"+" ?numM ?numA ?numS"="?numA ?numL ?numL ?numA crlf)
)