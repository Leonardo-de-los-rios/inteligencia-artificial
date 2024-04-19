(deftemplate persona
  (slot edad)
)

(deffacts datos
  (persona (edad 25))
  (persona (edad 17))
  (persona (edad 30))
)

(defrule persona-mayor-de-edad
  (exists (persona (edad ?edad &:(> ?edad 18))))
  =>
  (printout t "Hay al menos una persona mayor de edad." crlf)
)