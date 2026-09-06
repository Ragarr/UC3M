# Índice
1. Profesión y ética
2. [[Apuntes#Programación por parejas y propiedad colectiva|Programación en parejas y propiedad colectiva del codigo]]
3. [[Apuntes#Desarrollo dirigido por pruebas|Desarrollo dirigido por pruebas]]
	4. Clases de equivalencia y valores límite
	5. Análisis sintáctico
	6. Pruebas estructurales
7. Integración continua
8. Refactoiring
	9. Técnicas de refactoring
	10. Diseño simple y patrones


# Ética
La ingeniería del software es una profesión muy nueva,  tiene un consejo general a nivel nacional, así como algunas asociaciones como: [Association for Computing Machinery (acm.org)](https://www.acm.org/)  o [IEEE Computer Society](https://www.computer.org/)
Tampoco hay un código ético concreto, pero hay varios:
- [Código Ético y Deontológico de la Ingeniería Informática (ccii.es)](https://ccii.es/CodigoDeontologico)
- [Code of Ethics (acm.org)](https://www.acm.org/code-of-ethics)
- [BCS Code of Conduct for members - Ethics for IT professionals | BCS](https://www.bcs.org/membership-and-registrations/become-a-member/bcs-code-of-conduct/)
- [Code of Ethics | IEEE Computer Society](https://www.computer.org/education/code-of-ethics)

# Programación por parejas y propiedad colectiva
## Programación por parejas
Es una técnica en la que dos programadores trabajan juntos en el mismo código al mismo tiempo. 
Un programador es el **“conductor” que escribe el código**, mientras que el otro programador es el “**observador” que revisa el código** y proporciona comentarios.

Los roles de **conductor y observador se intercambian** periódicamente. La técnica puede **mejorar la calidad** y **productividad del código**, promover la comunicación entre los participantes y fomentar la **propiedad colectiva del código** entre los participantes.
## Ventajas e inconvenientes
**Ventajas**
Las ventajas de programar en parejas incluyen 
- detección y corrección rápida de errores
- mejora de la calidad del producto
- la promoción de la comunicación entre los participantes y la propiedad colectiva del código entre los participantes
La técnica también puede mejorar la satisfacción y confianza de los desarrolladores. 

**Inconvenientes**
Los inconvenientes pueden incluir
- posible disminución en la velocidad de codificación y discusiones absurdas entre los miembros de la pareja. 
- Además, ambos miembros deben tener un nivel similar de experiencia para que la técnica sea efectiva.
## Propiedad colectiva del código
La propiedad colectiva del código se refiere a la idea de que el código fuente puede ser modificado por varios programadores en cualquier momento.

Cuando el equipo entero trabaja en pares como norma, la continuidad de la pareja en el tiempo es menos importante: **un programador puede sustituir en cualquier momento a otro miembro del equipo**.

# Desarrollo dirigido por pruebas

Hay cuatro tipos de pruebas:
- **Pruebas de aceptación**: El cliente verifica si el producto reúne sus expectativas
- **Pruebas de sistema**: Los componentes se prueban como un todo
- **Pruebas de integración**: Entornos y scripts de integración continua
- **Pruebas unitarias**: Pruebas asociadas a cada componente individual
## Pruebas de aceptación
Los clientes deben percibir el progreso del proyecto a través de pruebas de software (Pruebas de aceptación - no entraremos en detalle) 
- Deben verificar que el software funciona acorde a sus expectativas 
- En la mayoría de los casos, estos tests sólo se llevan a cabo en el momento de la entrega del software
- Cada iteración en el desarrollo del software debe incluir pruebas de aceptación
- Céntrate únicamente en probar las cosas que quieres que funcionen en cada iteración. Al final ¡todo acabará siendo probado!

BLA BLA BLA 

## Pruebas unitarias
**Pasos**
1. Elegir un requisito 
	- Este requisito describe lo que el componente debe hacer. 
2. Escribir casos de prueba 
	- Basados en los requisitos (tanto funcionales como no-funcionales). 
3. El primer test falla 
	- Porque el diseño y la implementación aún no se han realizado. 
	- Si la primera vez no falla, deberías preocuparte: puede ser resultado de una mala definición del caso de prueba, o que hay otro componente ya implementado usando ese nombre. 11 Desarrollo de Software 2022-23 P
4. Diseñar e implementar la función
	 - Diseñar e implementar la parte del componente necesaria para superar cada caso de prueba (secuencialmente)
	 - Principio KISS (“Keep it small and simple”)
5. Ejecutar los casos de prueba automatizados 
	- Verificar que el caso de prueba ya no falla
	- Continuar con el siguiente caso de prueba o con el siguiente requisito
Cuando los tests pasan, refactorizar el código fuente aplicando los estándares de codificación

## Clases de equivalencia y valores límite
### Clases de equivalencia
El objetivo de utilizar clases de equivalencia es reducir la cantidad de casos de prueba necesarios para cubrir todas las posibles situaciones.
En lugar de probar cada valor individualmente, se prueban representantes de cada clase. Si se determina que un caso de prueba de una clase de equivalencia funciona correctamente, se asume que todos los casos de esa clase también funcionarán correctamente.

Por ejemplo, si se está probando una función de registro de usuarios en un sitio web, algunas clases de equivalencia podrían ser:
-   Casos de prueba para nombres de usuario válidos: incluiría nombres que cumplen con las reglas de formato y longitud establecidas.
-   Casos de prueba para nombres de usuario inválidos: incluiría nombres que no cumplen con las reglas de formato o longitud.
-   Casos de prueba para contraseñas válidas: incluiría contraseñas que cumplen con los requisitos de complejidad y longitud establecidos.
-   Casos de prueba para contraseñas inválidas: incluiría contraseñas que no cumplen con los requisitos de complejidad o longitud.
### Valores límite
1. Identificar las Clases de Equivalencia
2. Identificar los límites de cada clase de equivalencia
3. Crear los casos de prueba para cada valor límite considerando las reglas que se indican a continuación

## Análisis sintáctico
- Está más indicado para componentes en los cuales la mayoría de los datos de entrada se pueden modelar como una gramática
- Las pruebas de análisis sintáctico reducen el número de casos de prueba que se deben generar y ejecutar 
- Se requiere que la gramática de las entradas se pueda identificar con base en los requisitos del sistema
- El análisis sintáctico se puede aplicar tanto a las pruebas unitarias como de integración 
- Solamente en algunos casos esta técnica se puede utilizar en el nivel de sistema 
- No es recomendable para pruebas de aceptación
**Procedimiento**
1. Definición de la gramática 
2. Creación del árbol de derivación 
3. Identificación de los casos de prueba 
4. Automatización de los casos de prueba

**Definición de la gramática**.
Debe estar en forma normal de Chomsky: A→BC, B→b, C→c.

**Creación del árbol de derivación.**
- Se crea usando la gramática obtenida en el primer paso.
- Cada símbolo, terminal o no, se incluirá en un nodo diferente.
- Los nodos se numeran en amplitud comenzando por el 1.

**Identificación de casos de prueba**.
Se obtienen el análisis del árbol y se dividen en dos partes:entradas válidas e inválidas
- **Entradas válidas:**
	1. Se producen casos de prueba de tal forma que todos los nodos no terminales estén cubiertos
	2. Se repite el paso anterior para cubrir al menos una vez todos los nodos terminales
- **Entradas no válidas**
	1. Para los nodos no terminales se procede a su borrado y su duplicación.
	2. Para los nodos terminales debe procederse a su duplicación y borrado (**si no se ha hecho en pruebas anteriores**) además a su modificación. Se simula mediante errores tipográficos, siendo aconsejable no someter a prueba grandes combinaciones de errores.

- **Excepciones en borrado**
	- Nodos ya borrados por nodos superiores en la jerarquía del árbol. 
	- Nodos que al ser borrados producen casos válidos 
	- Nodos ya borrados por igualdad con otros nodos en la misma producción.
	- Nodos ya borrados por cruzamiento de nodos en distintas producciones.
- **Excepciones en duplicación de nodos**.
	- Nodos ya añadidos en nodos superiores en la jerarquía del árbol
	- Nodos iguales consecutivos
	- Nodos que al duplicarlos dan un caso válido
- **Excepciones en modificación de nodos**.
	- Nodos ya modificados por otros nodos en reglas de producción que tienen la misma parte izquierda
	- Agrupación de modificaciones de nodos


## Pruebas estructurales

**Pruebas de flujo de control**
Definimos diferentes niveles de cobertura del flujo de control 
**Nivel 0:**
- El porcentaje de cobertura es inferior al 100% del total del código 
![[Pasted image 20230522105444.png]]

**Nivel 1 Cobertura de secuencias**:
- Se generan los casos necesarios para ejecutar cada secuencia de instrucciones al menos una vez
![[Pasted image 20230522105452.png]]

**Nivel 2: Cobertura de decisiones **
- Consiste en generar el número suficiente de casos de prueba para asegurar que cada decisión en el código fuente tiene al menos una evaluación positiva (VERDADERO) y una evaluación negativa (FALSO) 
- Normalmente, la ejecución de las pruebas para la cobertura de decisiones cumple con las restricciones establecidas para la cobertura de secuencias (nivel 1).
![[Pasted image 20230522105524.png]]

**Nivel 3: Cobertura de condiciones **
- Consiste en la generación de suficientes casos de prueba para evaluar todas las posibles combinaciones en las condiciones del código
![[Pasted image 20230522105545.png]]

**Pruebas de camino básico**
Utiliza un análisis de la topología del grafo de control para identificar caminos de prueba
Pasos: 
1. Dibujar el grafo de flujo de control para el método a probar 
2. Calcular la complejidad ciclomática del grafo (C) 
3. Elegir un conjunto de C caminos básicos. 
4. Crear un caso de prueba para cada camino
5. Ejecutar los casos de prueba
![[Pasted image 20230520160919.png]]
Calcular C:
$$C=Edges-Nodes+2$$
Algoritmo para definir los caminos:
1. **Establecer un camino de referencia**. Este camino debe ser el camino típico de ejecución más que una excepción en el proceso de ejecución
2. Para escoger el siguiente camino, el resultado de la **primera decisión** en el camino de referencia **se cambia** mientras que **se mantiene igual las otras decisiones** (si es posible) con respecto al camino de referencia 
3. Para generar el tercer caso de prueba, se utiliza el camino de referencia pero se **cambia el resultado de la segunda decisión en lugar de la primera** 
4. Para generar el cuarto caso de prueba, se utiliza el camino de referencia pero se cambia el **resultado de la tercera decisión en lugar de la segunda** 
5. Continuar variando cada decisión de una en una hasta que se alcance el final del grafo de control

**Pruebas de estructuras de control**
![[Pasted image 20230520161421.png]]
**Pruebas de bucles**.
- Bucles simples: 
	- No pasar por el bucle 
	- Pasar por el bucle 1 vez 
	- Pasar por el bucle 2 veces
	- Pasar por el bucle max-1 veces 
	- Pasar por el bucle el número máximo de veces 
	- Intentar pasar por el bucle max+1 veces 
- Bucles anidados: 
	- Comenzar en el bucle más interno y progresar hacia fuera 
- Bucles concatenados: 
	- Considerarlos como bucles independientes 
- Bucles no estructurados 
	- Rediseñar los bucles. ¿Problemas de calidad?

# Refactoring
muy fácil bro dividir el código en chunks más pequeños ya sea sacando funciones o creando clases
también es renombrar variables, campos, agrupar sentencias relacionadas, enviar metodos a superclase, dividir el problema en fases

# Patrones de diseño 
Hay que tener bajo acoplamiento: las clases dependan poco entre ellas
Y alta cohesión: Los elementos solo deben hacer cosas altamente relacionadas.

### Patrón Singleton
El patrón Singleton se compone de los siguientes elementos:
1.  Una clase Singleton: Es una clase que tiene la responsabilidad de crear y gestionar su única instancia. La clase debe tener un constructor privado para evitar que se pueda instanciar directamente desde fuera de la clase.
2.  Un método de acceso estático: La clase Singleton debe proporcionar un método estático que permita acceder a la instancia única de la clase. Este método debe comprobar si la instancia ya ha sido creada y devolverla en caso afirmativo, o crearla y almacenarla en caso contrario.

Algunas características y casos de uso comunes del patrón Singleton incluyen:

-   Acceso centralizado: El patrón Singleton permite tener una única instancia que puede ser accedida globalmente desde cualquier parte del código.

-   Control de instanciación: El patrón Singleton controla la creación de su instancia, evitando la creación de múltiples instancias y asegurando que solo exista una.

-   Configuración única: El patrón Singleton es útil cuando se necesita una única instancia para gestionar una configuración o estado compartido en la aplicación.

-   Recursos compartidos: El patrón Singleton puede ser utilizado para gestionar recursos compartidos, como conexiones a bases de datos o archivos, garantizando que solo haya una instancia responsable de manejar esos recursos.

Sin embargo, el uso excesivo del patrón Singleton puede llevar a un acoplamiento fuerte y dificultar las pruebas unitarias. Por lo tanto, se debe evaluar cuidadosamente su necesidad y considerar alternativas si el patrón Singleton no es la mejor opción para el caso específico.