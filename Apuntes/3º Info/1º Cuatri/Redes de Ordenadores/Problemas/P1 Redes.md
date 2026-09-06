
**22**. Considere la Figura 1.19 (b). Suponga que cada enlace entre el servidor y el cliente tiene una probabilidad de pérdida de paquetes p y que las probabilidades de pérdida de paquetes de estos enlaces son independientes. ¿Cuál es la probabilidad de que un paquete (enviado por el servidor) sea recibido correctamente por el receptor? Si un paquete se pierde en el camino que va desde el servidor hasta el cliente, entonces el servidor volverá a transmitir el paquete. Como media, ¿cuántas veces tendrá que retransmitir el paquete el servidor para que el cliente lo reciba correctamente?



Para calcular la probabilidad de que un paquete enviado por el servidor sea recibido correctamente por el receptor a través de una serie de enlaces con pérdida de paquetes independientes, primero debemos considerar que la probabilidad de que un paquete se pierda en cada enlace es (p), y la probabilidad de que un paquete no se pierda en un enlace (es decir, sea recibido correctamente) es (1 - p).

Para calcular la probabilidad total de que el paquete sea recibido correctamente por el receptor, consideramos todas las posibilidades:

- El paquete se recibe correctamente en el primer intento (con probabilidad (1 - p)).
- El paquete se recibe correctamente en el segundo intento (con probabilidad $(p(1 - p))).$
- El paquete se recibe correctamente en el tercer intento (con probabilidad $(p^2(1 - p))).$
- Y así sucesivamente.

La probabilidad total de que el paquete sea recibido correctamente se puede calcular sumando todas estas posibilidades infinitas:

$P(\text{Paquete recibido correctamente}) = (1 - p) + p(1 - p) + p^2(1 - p) + \ldots$
$$P(\text{Paquete recibido correctamente}) = \sum_{n=0}^N(1-p)p^n=1-p^{N+1}$$
Utilizando la fórmula de la suma de una serie geométrica infinita:

$P(\text{Paquete recibido correctamente}) = 1 - p^{(N + 1)}$

No hay una respuesta finita de cuantas veces se tiene que mandar un paquete de media para asegurarte de que con N nodos de probabilidad de perdida p el cliente siempre reciba el paquete  

En conclusion, la pregunta sobre cuántas veces tendrá que retransmitir el servidor para que el cliente reciba correctamente el paquete no tiene una respuesta finita, ya que las retransmisiones pueden continuar indefinidamente en teoría. La probabilidad de que el paquete se reciba correctamente aumenta con cada retransmisión, pero no se puede determinar un número exacto de retransmisiones necesarias para garantizar la recepción correcta.

![[0.jpg]]

**23**. Considere la Figura 1.19 (a). Suponga que sabemos que el enlace cuello de botella a lo largo de la ruta entre el servidor y el cliente es el primer enlace, cuya velocidad es R_s bits/segundo. Suponga que envíamos un par de paquetes uno tras otro desde el servidor al cliente y que no hay más tráfico que ese en la ruta. Suponga que cada paquete tiene un tamaño de Lbits y que ambos enlaces presentan el mismo retardo de propagación d_prop.

a. ¿Cuál es el periodo entre llegadas de paquetes al destino? Es decir, ¿cuánto tiempo transcurre desde que el último bit del primer paquete llega hasta que lo hace el último bit del segundo paquete?  
b. Suponga ahora que el enlace cuello de botella es el segundo enlace (es decir, R_c < R_s). ¿Es posible que el segundo paquete tenga que esperar en la cola de entrada del segundo enlace? Explique su respuesta. Suponga ahora que el servidor envía el segundo paquete T segundos después de enviar el primero. ¿Qué valor debe tener T para garantizar que el segundo paquete no tenga que esperar en la cola de entrada del segundo enlace? Explique su respuesta.

**25**. Se tienen dos hosts, A y B, separados 20.000 kilómetros y conectados mediante un enlace directo con R= 2 Mbps. Suponga que la velocidad de propagación por el enlace es igual a 2,5·10^8 m/s. 

a. Calcule el producto ancho de banda-retardo, R·dprop  

b. Se envía un archivo cuyo tamaño es de 800.000 bits desde el host A al host B. Suponga que el archivo se envía de forma continua como un mensaje de gran tamaño. ¿Cuál es el número máximo de bits que habrá en el enlace en un instante de tiempo determinado?  
c. Haga una interpretación del producto ancho de banda-retardo.  
d. ¿Cuál es el ancho (en metros) de un bit dentro del enlace? ¿Es más grande que un campo de fútbol?  
e. Deduzca una expresión general para la anchura de un bit en función de la velocidad de propagación s, la velocidad de transmisión R y la longitud del enlace m.

**31**. En las redes de conmutación de paquetes modernas, el host de origen segmenta los mensajes largos de la capa de aplicación (por ejemplo, una imagen o un archivo de música) en paquetes más pequeños y los envía a la red. Después, el receptor ensambla los paquetes para formar el paquete original. Este proceso se conoce como segmentación de mensajes. La Figura 1.27 ilustra el transporte terminal a terminal de un mensaje con y sin segmentación del mensaje. Imagine que se envía un mensaje cuya longitud es de 8·10^6 bits desde el origen hasta el destino mostrados en la Figura 1.27. Suponga que cada enlace de los mostrados en la figura son enlaces a 2 Mbps. Ignore los retardos de propagación, de cola y de procesamiento. 

a. Suponga que el mensaje se transmite desde el origen al destino sin segmentarlo. ¿Cuánto tiempo tarda el mensaje en desplazarse desde el origen hasta el primer conmutador de paquetes? Teniendo en cuenta que cada conmutador de paquetes utiliza el método de conmutación de almacenamiento y reenvío, ¿cuál el tiempo total que invierte el mensaje para ir desde el host de origen hasta el host de destino?

b. Suponga ahora que el mensaje se segmenta en 4.000 paquetes y que la longitud de cada paquete es de 2.000 bits. ¿Cuánto tiempo tarda el primer paquete en transmitirse desde el origen hasta el primer conmutador de paquetes? Cuando se está enviando el primer paquete del primer conmutador al segundo, el host de origen envía un segundo paquete al primer conmutador de paquetes. ¿En qué instante de tiempo habrá recibido el primer conmutador el segundo paquete completo?

c. ¿Cuánto tiempo tarda en transmitirse el archivo desde el host de origen al host de destino cuando se emplea la segmentación de mensajes? Compare este resultado con la respuesta del apartado (a) y coméntelo. 

d. Comente los inconvenientes de la segmentación de mensajes.
![[1.jpg]]