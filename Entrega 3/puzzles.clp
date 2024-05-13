(deftemplate MAIN::nodo 
   (multislot estado)
   (slot heuristica) 
   (slot clase (default abierto)))

(defglobal MAIN 
   ?*estado-inicial* = (create$ H 2 3 4 5 6 7 8 9 ) 
   ?*estado-final* = (create$ 4 9 2 3 5 7 8 H 6  )
)

;Heuristica
(deffunction MAIN::heuristica ($?estado) 
   (bind ?res 0) 
   (loop-for-count (?i 1 9) 
    (if (neq (nth$ ?i ?estado) (nth$ ?i ?*estado-final*)) 
         then (bind ?res (+ ?res 1)) 
     ) 
    ) 
   ?res)


;Estado inicial
(defrule MAIN::inicial 
   => 
   (assert (nodo (estado ?*estado-inicial*) 
                  (heuristica (heuristica ?*estado-inicial*)) 
                  (clase cerrado)))
)


;Movimientos del espacio blanco
(defrule MAIN::arriba 
   (nodo (estado $?a ?b ?c ?d H $?e) 
          (clase cerrado)) 
=> 
   (bind $?nuevo-estado (create$  $?a H ?c ?d ?b $?e)) 
   (assert (nodo (estado $?nuevo-estado) 
                 (heuristica (heuristica $?nuevo-estado))))
)


(defrule MAIN::abajo 
   (nodo (estado $?a H ?b ?c ?d  $?e) 
          (clase cerrado)) 
=> 
   (bind $?nuevo-estado (create$ $?a ?d ?b ?c H $?e)) 
   (assert (nodo (estado $?nuevo-estado) 
                 (heuristica (heuristica $?nuevo-estado))))
)


(defrule MAIN::derecha 
   (nodo (estado $?a H ?b 
                 $?c&:(neq (mod (length$ $?c) 3) 2)) 
          (clase cerrado)) 
 => 
   (bind $?nuevo-estado (create$ $?a ?b H $?c)) 
   (assert (nodo (estado $?nuevo-estado) 
                 (heuristica (heuristica $?nuevo-estado))))
)


(defrule MAIN::izquierda 
   (nodo (estado $?a&:(neq (mod (length$ $?a) 3) 2) 
                   ?b H $?c) 
          (clase cerrado)) 
=> 
   (bind $?nuevo-estado (create$ $?a H ?b $?c)) 
   (assert (nodo (estado $?nuevo-estado) 
                 (heuristica (heuristica $?nuevo-estado))))
)


(defrule MAIN::ponderar
   (declare (salience -10)) 
   ?nodo <- (nodo (clase abierto) 
                  (heuristica ?h1)) 
   (not (nodo (clase abierto) 
              (heuristica ?h2&:(< ?h2 ?h1)))) 
=> 
   (modify ?nodo (clase cerrado))
)


;Solución (se encuentra al tener la heurIstica con valor 0 y el estado coincide)
(defrule MAIN::encuentra-solucion 
   
   (nodo (heuristica ?h) (estado $?estado))
   (test(eq ?estado ?*estado-final*))
   (test(eq ?h 0))
 =>  
   (assert (solucion $?estado))
)


(defrule MAIN::escribe-solucion 
   (solucion $?estado) 
  => 
   (printout t "Solucion: 4 9 2 3 5 7 8 H 6" crlf)
 (halt) 
) 
