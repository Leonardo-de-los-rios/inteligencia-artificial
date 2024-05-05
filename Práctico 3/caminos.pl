% Hechos con todas las rutas (numero,Corigen,Cdestino)
ruta(1,"Cap(SJ)","Caucete").
ruta(2,"Caucete","Chepes").
ruta(3,"Caucete","Quines").
ruta(4,"Caucete","Cap(SL)").
ruta(5,"Quines","R79").
ruta(6,"R79","Chepes").
ruta(7,"Quines","E91").
ruta(8,"E91","V.Dolores").
ruta(9,"V.Dolores","R20").
ruta(10,"R20","M.Clavero").
ruta(11,"M.Clavero","Taninga").
ruta(12,"Taninga","Chepes").
ruta(13,"Cap(SL)","R146").
ruta(14,"R146","Quines").
ruta(15,"Cap(SL)","R2").
ruta(16,"R2","E91").
ruta(17,"E91","R148").
ruta(18,"R148","R20").
ruta(19,"E91","R79").
ruta(20,"Cap(SL)","V.Mercedes").
ruta(21,"V.Mercedes","R2").
% Dos reglas para imprimir el camino, considerando Corigen y Cdestino.
camino(Co,Cd,[Co,Cd]):-ruta(_,Co,Cd).
camino(Co,Cd,[Co|Y]):-ruta(_,Co,Ci),camino(Ci,Cd,Y).

% Para ejecutar consulta
% camino("Cap(SJ)","Chepes",X),set_prolog_flag(answer_write_options,[max_depth(0)]).
% De esa forma se puede mostrar todo la lista sin truncarla
