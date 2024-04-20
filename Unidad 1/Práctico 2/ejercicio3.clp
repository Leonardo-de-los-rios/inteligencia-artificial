;-------------------------------------------------------------
; Item 3
;-------------------------------------------------------------
; Mabel y Gustavo se casaron y formaron una bella familia, 
; teniendo dos bellos hijos: Pedro y Laura. 
; Ambos cónyuges tenían un hijo cada uno antes del matrimonio,
; Agustín y Santiago respectivamente.
;-------------------------------------------------------------

(deftemplate mujer
  (slot nombre (type STRING))
)

(deftemplate hombre
  (slot nombre (type STRING))
)

(deftemplate hijo_de
  (slot hijo (type STRING))
  (slot padre_madre (type STRING))
)

(deftemplate esposa_de
  (slot esposa (type STRING))
  (slot esposo (type STRING))
)

(deftemplate marido_de
  (slot esposo (type STRING))
  (slot esposa (type STRING))
)

(deftemplate hermano
  (slot nombre1 (type STRING))
  (slot nombre2 (type STRING))
)

(deftemplate medio-hermano
  (slot nombre1 (type STRING))
  (slot nombre2 (type STRING))
)

(deftemplate hermanastro
  (slot nombre1 (type STRING))
  (slot nombre2 (type STRING))
)

(deffacts nombres
  (mujer (nombre "Mabel"))
  (mujer (nombre "Laura"))
  (hombre (nombre "Gustavo"))
  (hombre (nombre "Pedro"))
  (hombre (nombre "Agustin"))
  (hombre (nombre "Santiago"))
)

(deffacts hijos
    (hijo_de (hijo "Laura") (padre_madre "Gustavo"))
    (hijo_de (hijo "Laura") (padre_madre "Mabel"))
    (hijo_de (hijo "Pedro") (padre_madre "Gustavo"))
    (hijo_de (hijo "Pedro") (padre_madre "Mabel"))
    (hijo_de (hijo "Agustin") (padre_madre "Mabel"))
    (hijo_de (hijo "Santiago") (padre_madre "Gustavo"))
)

(deffacts matrimonio
  (esposa_de (esposa "Mabel") (esposo "Gustavo"))
  (marido_de (esposo "Gustavo") (esposa "Mabel"))
)

(defrule hermano
  (hijo_de (hijo ?hijo1) (padre_madre ?madre))
  (mujer (nombre ?madre))
  (hijo_de (hijo ?hijo1) (padre_madre ?padre))
  (hombre (nombre ?padre))
  (hijo_de (hijo ?hijo2&:(neq ?hijo2 ?hijo1)) (padre_madre ?madre_comun&:(eq ?madre_comun ?madre)))
  (hijo_de (hijo ?hijo2&:(neq ?hijo2 ?hijo1)) (padre_madre ?padre_comun&:(eq ?padre_comun ?padre)))
  (not (hermano (nombre1 ?hijo1) (nombre2 ?hijo2)))    ;para chequear que ya no existe un hecho entre los hermanos 
  (not (hermano (nombre1 ?hijo2) (nombre2 ?hijo1)))
  =>
  (printout t ?hijo1 " y " ?hijo2 " son hermanos." crlf)
  (assert (hermano (nombre1 ?hijo1) (nombre2 ?hijo2) )) 
)

(defrule medios-hermanos-madre
  (hijo_de (hijo ?hijo1) (padre_madre ?madre_comun))
  (mujer (nombre ?madre_comun)) 
  (hijo_de (hijo ?hijo2&:(neq ?hijo2 ?hijo1)) (padre_madre ?madre_comun))
  (hijo_de (hijo ?hijo1) (padre_madre ?padre))
  (hombre (nombre ?padre))
  (not (hijo_de (hijo ?hijo2&:(neq ?hijo2 ?hijo1)) (padre_madre ?padre)))
  =>
  (printout t ?hijo1 " y " ?hijo2 " son medios hermanos por parte de madre:" ?madre_comun crlf)
  (assert (medio-hermano (nombre1 ?hijo1) (nombre2 ?hijo2)))
)

(defrule medios-hermanos-padre
  (hijo_de (hijo ?hijo1) (padre_madre ?padre_comun))
  (hombre (nombre ?padre_comun))
  (hijo_de (hijo ?hijo2&:(neq ?hijo2 ?hijo1)) (padre_madre ?padre_comun))
  (hijo_de (hijo ?hijo1) (padre_madre ?madre))
  (mujer (nombre ?madre))
  (not (hijo_de (hijo ?hijo2&:(neq ?hijo2 ?hijo1)) (padre_madre ?madre)))
  =>
  (printout t ?hijo1 " y " ?hijo2 " son medios hermanos por parte de padre:" ?padre_comun crlf)
  (assert (medio-hermano (nombre1 ?hijo1) (nombre2 ?hijo2)))
)

(defrule hermanastros
  (hijo_de (hijo ?hijo1) (padre_madre ?padre))
  (hombre (nombre ?padre))
  (hijo_de (hijo ?hijo2&:(neq ?hijo2 ?hijo1)) (padre_madre ?madre))
  (mujer (nombre ?madre))
  (not (hijo_de (hijo ?hijo2&:(neq ?hijo2 ?hijo1)) (padre_madre ?padre)))
  (not (hijo_de (hijo ?hijo1) (padre_madre ?madre)))
  =>
  (printout t ?hijo1 " y " ?hijo2 " son hermanastros." crlf)
  (assert (hermanastro (nombre1 ?hijo1) (nombre2 ?hijo2)))
)
