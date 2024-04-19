(deftemplate persona
  (slot nombre (type STRING)) 
  (slot edad (type INTEGER)(range 0 100))
)

(deffacts nombres
  (persona (nombre "Juan") (edad 20))
  (persona (nombre "Paco") (edad 35))
  (persona (edad 18) (nombre "Julieta"))
)

(defrule Pedro-no
  (not(persona (nombre "Pedro") ))
  => 
  (printout t "Nadie se llama Pedro" crlf)
)

(defrule todos-mayores
  (forall (persona (edad ?n)) (test (> ?n 17))) 
  => 
  (printout t "Todos son mayores de edad" crlf)
)

(defrule nombres-diferentes
    (exists (persona (nombre ?n1))
            (persona (nombre ?n2&:(neq ?n1 ?n2))))
  => 
    (printout t "Existen dos personas con nombres diferentes" crlf)
)
