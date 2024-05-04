;---------------------------------------------------------
; Item 2
;---------------------------------------------------------
; Confeccione un programa que a través de reglas indique:
; • Dos personas con nombres diferentes
; • Nadie se llama pedro
; • Todo el mundo es mayor de edad
;---------------------------------------------------------

(deftemplate persona
  (slot nombre (type STRING))
  (slot edad (type INTEGER)(range 0 100))
)

(deffacts nombres
  (persona (nombre "Juan") (edad 20))
  (persona (nombre "Paco") (edad 35))
  (persona (edad 18) (nombre "Julieta"))
)

(defrule nombres-diferentes
  (declare (salience -10))   ;para ser el ultimo en ejecutarse
  (persona (nombre ?n1))
  (persona (nombre ?n2&:(neq ?n2 ?n1)))
  => 
  (printout t "Dos Personas con nombres diferentes! Nombre:" ?n1 ", Nombre: " ?n2 crlf)
  (halt)                     ;detiene la ejecucion y no muestra otros nombres
)

(defrule Pedro-no
  (not (persona (nombre "Pedro")))
  =>
  (printout t "Nadie se llama Pedro" crlf)
)

(defrule todos-mayores
  (forall (persona (edad ?n)) (test (> ?n 17))) 
  => 
  (printout t "Todos son mayores de edad" crlf)
)
