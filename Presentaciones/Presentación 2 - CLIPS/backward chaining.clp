(deftemplate animal
    (slot nombre)
)

(deftemplate es-reptil
    (slot nombre)
)

(deftemplate es-ave
    (slot nombre)
)

(deftemplate es-pez
    (slot nombre)
)

(deftemplate es-mamifero
    (slot nombre)
)

(deffacts hechos-iniciales
    (animal (nombre lagarto))
    (animal (nombre canario))
    (animal (nombre tiburon))
    (animal (nombre perro))
    (es-reptil (nombre lagarto))
    (es-ave (nombre canario))
    (es-pez (nombre tiburon))
)

(defrule es-mamifero
    (animal (nombre ?animal))
    (not (es-reptil (nombre ?animal)))
    (not (es-ave (nombre ?animal)))
    (not (es-pez (nombre ?animal)))
    =>
    (assert (es-mamifero (nombre ?animal)))
)

(defrule verificar-mamifero
    (es-mamifero (nombre ?animal))
    =>
    (printout t ?animal " es un mamifero." crlf)
)