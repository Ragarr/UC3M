```
ENVIO:= OPENKEY DATA CLOSINGKEY
OPENKEY:= {
CLOSINGKEY:= }
DATA:= D1 COMA D2
D1:= C ORD_ID C DP C DI_VAL C
C:= "
ORD_ID:= OrderId
DP:= :
DI_VAL:= a..f0..9{32}
COMA:= ,
D2:=C EMAIL C DP C VAL_EMAIL
EMAIL:= ContactEmail
VAL_EMAIL:= N_CORREO ARR DOM PT EXT
N_CORREO:= a..z0..9
ARR:= @
DOM a..z0..9
PT:= .
EXT:= a..z{max 3}
```

![[arbol derivacion f2.excalidraw]]














chat prompt 
tenemos una funcion que toma por argumento texto que sigue la siguiente gramatica:
```
ENVIO:= OPENKEY DATA CLOSINGKEY
OPENKEY:= {
CLOSINGKEY:= }
DATA:= D1 COMA D2
D1:= C ORD_ID C DP C DI_VAL C
C:= "
ORD_ID:= OrderId
DP:= :
DI_VAL:= a..f0..9{32}
COMA:= ,
D2:=C EMAIL C DP C VAL_EMAIL
EMAIL:= ContactEmail
VAL_EMAIL:= N_CORREO ARR DOM PT EXT
N_CORREO:= a..z0..9
ARR:= @
DOM a..z0..9
PT:= .
EXT:= a..z{max 3}
```
eres capaz de crear una tabla con las siguientes columnas (#,	NODE,	TERMINAL (T) / NO TERMINAL (NT),	TYPE (DUPLICATION / DELETION / MODIFICATION / VALID),	ID TEST,	DESCRIPTION,	FILE, PATH,	FILE, CONTENT	EXPECTED RESULT) donde file content es el tex to que hay que generar y file path es test#.json (donde # es el numero de test de la columna 1), se debe probar la duplicacion y eliminacion de todos los nodos no terminales del arbol de derivación de la gramatica y la modificacion de todos los nodos terminales del arbol de derivación. 