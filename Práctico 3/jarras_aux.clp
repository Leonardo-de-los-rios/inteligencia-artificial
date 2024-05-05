(deftemplate jarra
  (slot contenido (type INTEGER) (default ?NONE))
  (slot capacidad (type INTEGER) (default ?DERIVE))
)

(deffacts jarras-iniciales
  (jarra (contenido 0) (capacidad 5))
  (jarra (contenido 0) (capacidad 11))
  (jarra (contenido 0) (capacidad 13))
  (jarra (contenido 24) (capacidad 24))
)

; Regla 0: [Finalizar programa] = [J1, J2, J3, JG] => [0, 8, 8, 8]
(defrule regla_0
  (declare (salience 10000))
  (jarra (contenido 8) (capacidad 11))
  (jarra (contenido 8) (capacidad 13))
  (jarra (contenido 8) (capacidad 24))
  =>
  (printout t "J1: 0L de 5L." crlf)
  (printout t "J2: 8L de 11L." crlf)
  (printout t "J3: 8L de 13L." crlf)
  (printout t "JG: 8L de 24L." crlf)
  (halt)
)

; Regla 15: [Volcar G en 3 llene] = [J1, J2, J3, JG] / R=JG+J3, R>13, JG>0, D=R-13 => [J1, J2, 13, D]
(defrule regla_15
  ?jarraG <- (jarra (contenido ?JG) (capacidad 24))
  ?jarra3 <- (jarra (contenido ?J3) (capacidad 13))
  (test (< ?J3 13))
  (test (> ?JG 0))
  (test (> (+ ?JG ?J3) 13))
  =>
  (bind ?R (+ ?JG ?J3))
  (bind ?D (- ?R 13))
  (modify ?jarraG (contenido ?D))
  (modify ?jarra3 (contenido 13))
)

; Regla 13: [Volcar G en 1 llene] = [J1, J2, J3, JG] / R=JG+J1, R>5, JG>0, D=R-5 => [5, J2, J3, D]
(defrule regla_13
  ?jarraG <- (jarra (contenido ?JG) (capacidad 24))
  ?jarra1 <- (jarra (contenido ?J1) (capacidad 5))
  (test (< ?J1 5))
  (test (> ?JG 0))
  (test (> (+ ?JG ?J1) 5))
  =>
  (bind ?R (+ ?JG ?J1))
  (bind ?D (- ?R 5))
  (modify ?jarraG (contenido ?D))
  (modify ?jarra1 (contenido 5))
)

; Regla 14: [Volcar G en 2 llene] = [J1, J2, J3, JG] / R=JG+J2, R>11, JG>0, D=R-11 => [J1, 11, J3, D]
(defrule regla_14
  ?jarraG <- (jarra (contenido ?JG) (capacidad 24))
  ?jarra2 <- (jarra (contenido ?J2) (capacidad 11))
  (test (< ?J2 11))
  (test (> ?JG 0))
  (test (> (+ ?JG ?J2) 11))
  =>
  (bind ?R (+ ?JG ?J2))
  (bind ?D (- ?R 11))
  (modify ?jarraG (contenido ?D))
  (modify ?jarra2 (contenido 11))
)

