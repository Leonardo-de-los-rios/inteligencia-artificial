/* P: pastor, L: lobo, O: oveja, R: Repollo
inicialmente todos se encuentran del lado norte: [norte, norte, norte, norte] */

% Condiciones
opuesto(norte,sur).
opuesto(sur,norte).

% Ejecución del Programa
iniciar():- movimiento(norte,norte,norte,norte,1,1,1,1),!.


% Caso Base
movimiento(sur,sur,sur,sur,_,_,_,_).

% Ir Pastor con Oveja:
movimiento(X,L,X,R,_,_,1,_):- opuesto(X,Y), writeln("El Pastor viaja con la Oveja"), movimiento(Y,L,Y,R,1,1,0,1).

% Ir Pastor solo:
movimiento(P,L,O,R,1,_,_,_):- opuesto(L,O), opuesto(O,R), opuesto(P,P1), writeln("El Pastor viaja solo"), movimiento(P1,L,O,R,0,1,1,1).

% Ir Pastor con Lobo:
movimiento(X,X,O,R,_,1,_,_):- opuesto(O,R), opuesto(X,Y), writeln("El Pastor viaja con el Lobo"), movimiento(Y,Y,O,R,1,0,1,1).

% Ir Pastor con Repollo:
movimiento(X,L,O,X,_,_,_,1):- opuesto(L,O), opuesto(X,Y), writeln("El Pastor viaja con la Repollo"), movimiento(Y,L,O,Y,1,1,1,0).