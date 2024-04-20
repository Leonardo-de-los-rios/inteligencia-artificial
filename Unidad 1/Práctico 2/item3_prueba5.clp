(deftemplate mujer
  (slot nombre (type STRING))
)

(deftemplate hombre
  (slot nombre (type STRING))
)

(deftemplate hijx_de
  (slot hijx (type STRING))
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
  (hijx_de (hijx "Laura") (padre_madre "Gustavo"))
  (hijx_de (hijx "Laura") (padre_madre "Mabel"))
  (hijx_de (hijx "Pedro") (padre_madre "Gustavo"))
  (hijx_de (hijx "Pedro") (padre_madre "Mabel"))
  (hijx_de (hijx "Agustin") (padre_madre "Mabel"))
  (hijx_de (hijx "Santiago") (padre_madre "Gustavo"))
)

(deffacts matrimonio
  (esposa_de (esposa "Mabel") (esposo "Gustavo"))
  (marido_de (esposo "Gustavo") (esposa "Mabel"))
)

(defrule hermano
  (hijx_de (hijx ?hijo1) (padre_madre ?madre))
  (mujer (nombre ?madre))
  (hijx_de (hijx ?hijo1) (padre_madre ?padre))
  (hombre (nombre ?padre))
  (hijx_de (hijx ?hijo2&:(neq ?hijo2 ?hijo1)) (padre_madre ?madre_comun&:(eq ?madre_comun ?madre)))
  (hijx_de (hijx ?hijo2&:(neq ?hijo2 ?hijo1)) (padre_madre ?padre_comun&:(eq ?padre_comun ?padre)))
  (not (hermano (nombre1 ?hijo1) (nombre2 ?hijo2)))    ;para chequear que ya no existe un hecho entre los hermanos 
  (not (hermano (nombre1 ?hijo2) (nombre2 ?hijo1)))
  =>
  (printout t ?hijo1 " y " ?hijo2 " son hermanos." crlf)
  (assert (hermano (nombre1 ?hijo1) (nombre2 ?hijo2) )) 
)

(defrule medios-hermanos-madre
  (hijx_de (hijx ?hijo1) (padre_madre ?madre_comun))
  (mujer (nombre ?madre_comun)) 
  (hijx_de (hijx ?hijo2&:(neq ?hijo2 ?hijo1)) (padre_madre ?madre_comun))
  (hijx_de (hijx ?hijo1) (padre_madre ?padre))
  (hombre (nombre ?padre))
  (not (hijx_de (hijx ?hijo2&:(neq ?hijo2 ?hijo1)) (padre_madre ?padre)))
  =>
  (printout t ?hijo1 " y " ?hijo2 " son medios hermanos por parte de madre:" ?madre_comun crlf)
  (assert (medio-hermano (nombre1 ?hijo1) (nombre2 ?hijo2)))
)

(defrule medios-hermanos-padre
  (hijx_de (hijx ?hijo1) (padre_madre ?padre_comun))
  (hombre (nombre ?padre_comun))
  (hijx_de (hijx ?hijo2&:(neq ?hijo2 ?hijo1)) (padre_madre ?padre_comun))
  (hijx_de (hijx ?hijo1) (padre_madre ?madre))
  (mujer (nombre ?madre))
  (not (hijx_de (hijx ?hijo2&:(neq ?hijo2 ?hijo1)) (padre_madre ?madre)))
  =>
  (printout t ?hijo1 " y " ?hijo2 " son medios hermanos por parte de padre:" ?padre_comun crlf)
  (assert (medio-hermano (nombre1 ?hijo1) (nombre2 ?hijo2)))
)

(defrule hermanastros
  (hijx_de (hijx ?hijo1) (padre_madre ?padre))
  (hombre (nombre ?padre))
  (hijx_de (hijx ?hijo2&:(neq ?hijo2 ?hijo1)) (padre_madre ?madre))
  (mujer (nombre ?madre))
  (not (hijx_de (hijx ?hijo2&:(neq ?hijo2 ?hijo1)) (padre_madre ?padre)))
  (not (hijx_de (hijx ?hijo1) (padre_madre ?madre)))
  =>
  (printout t ?hijo1 " y " ?hijo2 " son hermanastros." crlf)
  (assert (hermanastro (nombre1 ?hijo1) (nombre2 ?hijo2)))
)
