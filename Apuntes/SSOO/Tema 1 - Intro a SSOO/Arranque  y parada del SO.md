# Fases del arranque del SO
[[Arranque  y parada del SO#Iniciador ROM|Iniciador ROM]] ->[[Arranque  y parada del SO#Cargador del sistema operativo|Cargador del SO]] -> [[Arranque  y parada del SO#Parte residente del SO|Parte residente del SO]] ->Ejecución normal del SO

## Iniciador ROM
1. La [[Señales, excepciones y pipes|señal]] RESET carga valores predefinidos en registros.
		CP <-dirección de arranque del cargador ROM
2. Se ejecuta el iniciador ROM del sistema:
	1. Test hardware del sistema
	2. Trae a memoria el boot (iniciador) del SO

## Cargador del sistema operativo 
-  El programa cargador se encuentra en el sector de inicio (boot) del disco. 
-  Es responsable de cargar el sistema operativo. 
- Verifica la presencia de palabra mágica en sector de arranque.![[Pasted image 20230309135457.png]]

## Parte residente del SO
- Responsable de la iniciación del sistema operativo. 
	- Verificación de consistencia del sistema de ficheros.
	- Creación de las estructuras de datos internas. 
	- Activación de modo de memoria virtual. 
	- Carga el resto del sistema operativo residente. 
	- Habilita interrupciones. 
	- Crea procesos iniciales

# Parada del ordenador
Para acelerar la ejecución el sistema operativo mantiene información en memoria no actualizada a disco. Al apagar hay que volcar dicha información a disco y terminar la ejecución de todos los procesos. 
Si no se hace volcado (apagado brusco)
- Pérdida de información. 
- Sistema de ficheros en estado inconsistente. 
Otras alternativas en computadores personales: 
- Hibenación: Se guarda estado de la memoria principal a disco. 
- Apagado en espera (standby): Parada del computador que mantiene alimentada la memoria principal.
