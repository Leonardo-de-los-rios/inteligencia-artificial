;-------------------------------------------------------------
; Item 3
;-------------------------------------------------------------
; Mabel y Gustavo se casaron y formaron una bella familia, 
; teniendo dos bellos hijos: Pedro y Laura. 
; Ambos cónyuges tenían un hijo cada uno antes del matrimonio,
; Agustín y Santiago respectivamente.
;-------------------------------------------------------------
; • Mediante la definición de reglas:
; • Mostrar los nombres de los hermanos hijos del matrimonio y
; agregar los hechos (hermano <Nombre> <Nombre>) a la MT .
; • Mostrar los nombres de los medios hermanos y agregar esos 
; hechos a la MT (medio-hermano <Nombre> <Nombre>)
; • Mostrar los nombres de los hermanastros y agregar los
; hechos a la MT como tales. (hermanastro <> <>)
;-------------------------------------------------------------

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
  ; obetener dos hijos distintos y primer padre/madre de cada hijo
  (hijx_de (hijx ?hijo1) (padre_madre ?pm1_h1))
  (hijx_de (hijx ?hijo2&:(neq ?hijo2 ?hijo1)) (padre_madre ?pm1_h2&:(eq ?pm1_h2 ?pm1_h1)))

  ; verificar que no existe la relación hermano
  (not (hermano (nombre1 ?hijo1) (nombre2 ?hijo2)))
  (not (hermano (nombre1 ?hijo2) (nombre2 ?hijo1)))

  ; analizar la relación de los hijos y obetener segundo padre/madre de cada hijo
  (hijx_de (hijx ?hijo1) (padre_madre ?pm2_h1&:(neq ?pm1_h1 ?pm2_h1)))
  (hijx_de (hijx ?hijo2&:(neq ?hijo2 ?hijo1)) (padre_madre ?pm2_h2&:(eq ?pm2_h2 ?pm2_h1)))
  =>
  (printout t ?hijo1 " y " ?hijo2 " son hermanos." crlf)
  (assert (hermano (nombre1 ?hijo1) (nombre2 ?hijo2)))
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

