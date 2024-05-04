(deftemplate jarra
  (slot contenido (type INTEGER) (default ?NONE))
  (slot capacidad (type INTEGER) (default ?DERIVE))
)

(deftemplate ultimo-visitado
  (slot jarra_a (type SYMBOL) (default ?NONE))
  (slot jarra_b (type SYMBOL) (default ?NONE))
)

(deffacts jarras-iniciales
  (jarra (contenido 0) (capacidad 5))
  (jarra (contenido 0) (capacidad 11))
  (jarra (contenido 0) (capacidad 13))
  (jarra (contenido 24) (capacidad 24))
)

(deffacts ultima-visita-inicial
  (ultimo-visitado (jarra_a x) (jarra_b y)) ; valores de jarras inexistentes
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

; Regla 1: [Volcar todo G en 1] = [J1, J2, J3, JG] / R=JG+J1, R<=5, JG>0 => [R, J2, J3, 0]
(defrule regla_1
  ?jarraG <- (jarra (contenido ?JG) (capacidad 24))
  ?jarra1 <- (jarra (contenido ?J1) (capacidad 5))
  (not (ultimo-visitado (jarra_a J1) (jarra_b JG)))
  ?visitado <- (ultimo-visitado)
  (test (> ?JG 0))
  (test (< ?J1 5))
  (test (<= (+ ?JG ?J1) 5))
  =>
  (bind ?R (+ ?JG ?J1))
  (modify ?jarraG (contenido 0))
  (modify ?jarra1 (contenido ?R))
  (modify ?visitado (jarra_a J1) (jarra_b JG))
)

; Regla 2: [Volcar todo G en 2] = [J1, J2, J3, JG] / R=JG+J2, R<=11, JG>0 => [J1, R, J3, 0]
(defrule regla_2
  ?jarraG <- (jarra (contenido ?JG) (capacidad 24))
  ?jarra2 <- (jarra (contenido ?J2) (capacidad 11))
  (not (ultimo-visitado (jarra_a J2) (jarra_b JG)))
  ?visitado <- (ultimo-visitado)
  (test (> ?JG 0))
  (test (< ?J2 11))
  (test (<= (+ ?JG ?J2) 11))
  =>
  (bind ?R (+ ?JG ?J2))
  (modify ?jarraG (contenido 0))
  (modify ?jarra2 (contenido ?R))
  (modify ?visitado (jarra_a J2) (jarra_b JG))
)

; Regla 3: [Volcar todo G en 3] = [J1, J2, J3, JG] / R=JG+J3, R<=13, JG>0 => [J1, J2, R, 0]
(defrule regla_3
  ?jarraG <- (jarra (contenido ?JG) (capacidad 24))
  ?jarra3 <- (jarra (contenido ?J3) (capacidad 13))
  (not (ultimo-visitado (jarra_a J3) (jarra_b JG)))
  ?visitado <- (ultimo-visitado)
  (test (> ?JG 0))
  (test (< ?J3 13))
  (test (<= (+ ?JG ?J3) 13))
  =>
  (bind ?R (+ ?JG ?J3))
  (modify ?jarraG (contenido 0))
  (modify ?jarra3 (contenido ?R))
  (modify ?visitado (jarra_a J3) (jarra_b JG))
)

; Regla 4: [Volcar todo 1 en 2] = [J1, J2, J3, JG] / R=J1+J2, R<=11, J1>0 => [0, R, J3, JG]
(defrule regla_4
  ?jarra1 <- (jarra (contenido ?J1) (capacidad 5))
  ?jarra2 <- (jarra (contenido ?J2) (capacidad 11))
  (not (ultimo-visitado (jarra_a J1) (jarra_b J2)))
  ?visitado <- (ultimo-visitado)
  (test (> ?J1 0))
  (test (< ?J2 11))
  (test (<= (+ ?J1 ?J2) 11))
  =>
  (bind ?R (+ ?J1 ?J2))
  (modify ?jarra1 (contenido 0))
  (modify ?jarra2 (contenido ?R))
  (modify ?visitado (jarra_a J1) (jarra_b J2))
)

; Regla 5: [Volcar todo 1 en 3] = [J1, J2, J3, JG] / R=J1+J3, R<=13, J1>0 => [0, J2, R, JG]
(defrule regla_5
  ?jarra1 <- (jarra (contenido ?J1) (capacidad 5))
  ?jarra3 <- (jarra (contenido ?J3) (capacidad 13))
  (not (ultimo-visitado (jarra_a J1) (jarra_b J3)))
  ?visitado <- (ultimo-visitado)
  (test (> ?J1 0))
  (test (< ?J3 13))
  (test (<= (+ ?J1 ?J3) 13))
  =>
  (bind ?R (+ ?J1 ?J3))
  (modify ?jarra1 (contenido 0))
  (modify ?jarra3 (contenido ?R))
  (modify ?visitado (jarra_a J1) (jarra_b J3))
)

; Regla 6: [Volcar todo 1 en G] = [J1, J2, J3, JG] / R=J1+JG, R<=24, J1>0 => [0, J2, J3, R]
(defrule regla_6
  ?jarra1 <- (jarra (contenido ?J1) (capacidad 5))
  ?jarraG <- (jarra (contenido ?JG) (capacidad 24))
  (not (ultimo-visitado (jarra_a J1) (jarra_b JG)))
  ?visitado <- (ultimo-visitado)
  (test (> ?J1 0))
  (test (< ?JG 24))
  (test (<= (+ ?J1 ?JG) 24))
  =>
  (bind ?R (+ ?J1 ?JG))
  (modify ?jarra1 (contenido 0))
  (modify ?jarraG (contenido ?R))
  (modify ?visitado (jarra_a J1) (jarra_b JG))
)

; Regla 7: [Volcar todo 2 en 1] = [J1, J2, J3, JG] / R=J2+J1, R<=5, J2>0 => [R, 0, J3, JG]
(defrule regla_7
  ?jarra2 <- (jarra (contenido ?J2) (capacidad 11))
  ?jarra1 <- (jarra (contenido ?J1) (capacidad 5))
  (not (ultimo-visitado (jarra_a J1) (jarra_b J2)))
  ?visitado <- (ultimo-visitado)
  (test (> ?J2 0))
  (test (< ?J1 5))
  (test (<= (+ ?J2 ?J1) 5))
  =>
  (bind ?R (+ ?J2 ?J1))
  (modify ?jarra2 (contenido 0))
  (modify ?jarra1 (contenido ?R))
  (modify ?visitado (jarra_a J1) (jarra_b J2))
)

; Regla 8: [Volcar todo 2 en 3] = [J1, J2, J3, JG] / R=J2+J3, R<=13, J2>0 => [J1, 0, R, JG]
(defrule regla_8
  ?jarra2 <- (jarra (contenido ?J2) (capacidad 11))
  ?jarra3 <- (jarra (contenido ?J3) (capacidad 13))
  (not (ultimo-visitado (jarra_a J2) (jarra_b J3)))
  ?visitado <- (ultimo-visitado)
  (test (> ?J2 0))
  (test (< ?J3 13))
  (test (<= (+ ?J2 ?J3) 13))
  =>
  (bind ?R (+ ?J2 ?J3))
  (modify ?jarra2 (contenido 0))
  (modify ?jarra3 (contenido ?R))
  (modify ?visitado (jarra_a J2) (jarra_b J3))
)

; Regla 9: [Volcar todo 2 en G] = [J1, J2, J3, JG] / R=J2+JG, R<=24, J2>0 => [J1, 0, J3, R]
(defrule regla_9
  ?jarra2 <- (jarra (contenido ?J2) (capacidad 11))
  ?jarraG <- (jarra (contenido ?JG) (capacidad 24))
  (not (ultimo-visitado (jarra_a J2) (jarra_b JG)))
  ?visitado <- (ultimo-visitado)
  (test (> ?J2 0))
  (test (< ?JG 24))
  (test (<= (+ ?J2 ?JG) 24))
  =>
  (bind ?R (+ ?J2 ?JG))
  (modify ?jarra2 (contenido 0))
  (modify ?jarraG (contenido ?R))
  (modify ?visitado (jarra_a J2) (jarra_b JG))
)

; Regla 10: [Volcar todo 3 en 1] = [J1, J2, J3, JG] / R=J3+J1, R<=5, J3>0 => [R, J2, 0, JG]
(defrule regla_10
  ?jarra3 <- (jarra (contenido ?J3) (capacidad 13))
  ?jarra1 <- (jarra (contenido ?J1) (capacidad 5))
  (not (ultimo-visitado (jarra_a J1) (jarra_b J3)))
  ?visitado <- (ultimo-visitado)
  (test (> ?J3 0))
  (test (< ?J1 5))
  (test (<= (+ ?J3 ?J1) 5))
  =>
  (bind ?R (+ ?J3 ?J1))
  (modify ?jarra3 (contenido 0))
  (modify ?jarra1 (contenido ?R))
  (modify ?visitado (jarra_a J1) (jarra_b J3))
)

; Regla 11: [Volcar todo 3 en 2] = [J1, J2, J3, JG] / R=J3+J2, R<=11, J3>0 => [J1, R, 0, JG]
(defrule regla_11
  (declare (salience 1000))
  ?jarra3 <- (jarra (contenido ?J3) (capacidad 13))
  ?jarra2 <- (jarra (contenido ?J2) (capacidad 11))
  (not (ultimo-visitado (jarra_a J2) (jarra_b J3)))
  ?visitado <- (ultimo-visitado)
  (test (> ?J3 0))
  (test (< ?J2 11))
  (test (<= (+ ?J3 ?J2) 11))
  =>
  (bind ?R (+ ?J3 ?J2))
  (modify ?jarra3 (contenido 0))
  (modify ?jarra2 (contenido ?R))
  (modify ?visitado (jarra_a J2) (jarra_b J3))
)

; Regla 12: [Volcar todo 3 en G] = [J1, J2, J3, JG] / R=J3+JG, R<=24, J3>0 => [J1, J2, 0, R]
(defrule regla_12
  ?jarra3 <- (jarra (contenido ?J3) (capacidad 13))
  ?jarraG <- (jarra (contenido ?JG) (capacidad 24))
  (not (ultimo-visitado (jarra_a J3) (jarra_b JG)))
  ?visitado <- (ultimo-visitado)
  (test (> ?J3 0))
  (test (< ?JG 24))
  (test (<= (+ ?J3 ?JG) 24))
  =>
  (bind ?R (+ ?J3 ?JG))
  (modify ?jarra3 (contenido 0))
  (modify ?jarraG (contenido ?R))
  (modify ?visitado (jarra_a J3) (jarra_b JG))
)








; Regla 13: [Volcar G en 1 llene] = [J1, J2, J3, JG] / R=JG+J1, R>5, JG>0, D=R-5 => [5, J2, J3, D]
(defrule regla_13
  ?jarraG <- (jarra (contenido ?JG) (capacidad 24))
  ?jarra1 <- (jarra (contenido ?J1) (capacidad 5))
  (not (ultimo-visitado (jarra_a J1) (jarra_b JG)))
  ?visitado <- (ultimo-visitado)
  (test (< ?J1 5))
  (test (> ?JG 0))
  (test (> (+ ?JG ?J1) 5))
  =>
  (bind ?R (+ ?JG ?J1))
  (bind ?D (- ?R 5))
  (modify ?jarraG (contenido ?D))
  (modify ?jarra1 (contenido 5))
  (modify ?visitado (jarra_a J1) (jarra_b JG))
)

; Regla 14: [Volcar G en 2 llene] = [J1, J2, J3, JG] / R=JG+J2, R>11, JG>0, D=R-11 => [J1, 11, J3, D]
(defrule regla_14
  ?jarraG <- (jarra (contenido ?JG) (capacidad 24))
  ?jarra2 <- (jarra (contenido ?J2) (capacidad 11))
  (not (ultimo-visitado (jarra_a J2) (jarra_b JG)))
  ?visitado <- (ultimo-visitado)
  (test (< ?J2 11))
  (test (> ?JG 0))
  (test (> (+ ?JG ?J2) 11))
  =>
  (bind ?R (+ ?JG ?J2))
  (bind ?D (- ?R 11))
  (modify ?jarraG (contenido ?D))
  (modify ?jarra2 (contenido 11))
  (modify ?visitado (jarra_a J2) (jarra_b JG))
)

; Regla 15: [Volcar G en 3 llene] = [J1, J2, J3, JG] / R=JG+J3, R>13, JG>0, D=R-13 => [J1, J2, 13, D]
(defrule regla_15
  (declare (salience 100))
  ?jarraG <- (jarra (contenido ?JG) (capacidad 24))
  ?jarra3 <- (jarra (contenido ?J3) (capacidad 13))
  (not (ultimo-visitado (jarra_a J3) (jarra_b JG)))
  ?visitado <- (ultimo-visitado)
  (test (< ?J3 13))
  (test (> ?JG 0))
  (test (> (+ ?JG ?J3) 13))
  =>
  (bind ?R (+ ?JG ?J3))
  (bind ?D (- ?R 13))
  (modify ?jarraG (contenido ?D))
  (modify ?jarra3 (contenido 13))
  (modify ?visitado (jarra_a J3) (jarra_b JG))
)