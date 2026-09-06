<h1>Memoria de la entrega 2</h1>


<p> Criptografía y Seguridad Informática
</p>
<p>Raúl Aguilar Arroyo
</p>
<p>Alberto Penas Díaz
</p>
<p>Grupo 8001
</p>
<p>

</p>
<h1></h1>


<h1>Índice</h1>


<p>

</p>
<h1>Propósito de la aplicación</h1>


<p>
El propósito general de la aplicación es encriptar localmente secciones de imágenes que se almacenan en un servidor.
</p>
<h2>Estructura de la aplicación</h2>


<p>
La aplicación está compuesta de dos partes muy diferenciadas, el lado del cliente y el lado del servidor.
</p>
<h3>Lado del cliente</h3>


<p>
Este es el encargado de encriptar las imágenes y almacenar (mientras dure la sesión) la contraseña del usuario. También es el encargado de enviar correctamente las imágenes y la información al servidor. Esta parte se divide a su vez en 3 componentes:
</p>
<ul>

<li><strong>Interfaz de usuario (UI):</strong> 
<ul>
 
<li>Es simplemente la interfaz gráfica contra la que interactúa el usuario, está recopila las entradas, se las manda al cliente y muestra las imágenes e información que el cliente le proporciona.
</li> 
</ul>

<li><strong>Cliente:</strong> 
<ul>
 
<li>Se encarga de enviar la información al servidor y a la interfaz gráfica, así como de hacer las solicitudes al servidor. Proporciona las funciones a las que tiene acceso el usuario.
</li> 
</ul>

<li><strong>Paquete Image Crypto Utils (ICU):</strong> 
<ul>
 
<li>Es el encargado de encriptar y desencriptar imágenes, así como de generar los MAC de las mismas.
</li> 
</ul>
</li> 
</ul>
<h3>Lado del servidor</h3>


<p>
Este es el encargado de autenticar a los usuarios y de administrar las imágenes que se suben. A nivel lógico se divide en servidor y la base de datos.
</p>
<ul>

<li><strong>Servidor:</strong> 
<ul>
 
<li>Es el encargado de autenticar a los usuarios, exigir la robustez de las contraseñas, la generación de KDFs de las contraseñas para su almacenamiento y la verificación de la originalidad de las imágenes proporcionadas
</li> 
</ul>

<li><strong>Base de datos:</strong> 
<ul>
 
<li>Es la encargada de administrar la localización y búsqueda tanto de imágenes como de la información de los usuarios.
</li> 
</ul>
</li> 
</ul>
<h3>Autoridades de Acreditación</h3>


<p>
Hemos creado una serie de autoridades que se encargan de firmar los certificados que utilizan el servidor y el cliente (se explica en la página 4 )
</p>
<ul>

<li><strong>El Papa</strong>: Es la autoridad máxima y se autoafirma su certificado.

<li><strong>Pedro Sanchez</strong> y <strong>Ursula</strong> (von der Leyen) que certifican cliente y al servidor respectivamente 
</li>
</ul>
<p>
Se indaga más profundamente en el funcionamiento de la aplicación en la página 
</p>
<h1>Firma Digital</h1>


<p>
Utilizamos la firma digital para acreditar cada una de las imágenes que envía el cliente al servidor. De esta manera, aportamos a ésta comunicación un método para verificar la identidad del cliente así como el “no repudio”.  Hemos decidido emplear el método de cifrado RSA para firmar el hash de autenticación de imágen (véase la memoria de la primera entrega), de esta manera, el cliente envía <strong>directamente</strong> al servidor una tupla con la siguiente información: 
</p>
<ol>

<li><strong>hash:</strong> resumen de la imagen previamente encriptada utilizando como generador una clave de 32 bytes generada aleatoriamente, el nonce y el salt.

<li><strong>key: </strong> la clave que se ha utilizado para generar el resumen de la  imagen.

<li><strong>signature:</strong> el hash encriptado con la clave privada del usuario.
</li>
</ol>
<p>
De esta forma, el servidor, haciendo uso de la clave pública del usuario (que el mismo hace llegar al servidor a través del certificado) es capaz de comprobar que, efectivamente, el hash de la imagen coincide con el resultado de descifrar la <em>signature </em>con la clave pública del cliente.
</p>
<p>
Es conveniente explicar que este par de clave pública y clave privada se renueva cada vez que se empieza una nueva comunicación entre cliente y servidor.
</p>
<h1></h1>


<h1>Certificados de clave pública</h1>


<h2>Infraestructura de clave pública</h2>


<p>
Consta de 3 niveles (aunque por la implementación es sencillo escalar a tantos niveles como se quiera), hemos designado al Papa como CA raiz y a Pedro Sanchez y Ursula Von Der Lien como autoridades subordinadas.
</p>
<p>
Los usuarios finales son el cliente y el servidor, cuya única autoridad en común es el CA raíz. 
</p>
<p>
Por lo tanto cuando se verifican los certificados siempre acaban acudiendo a la CA raíz.
</p>
<h2>Generación de certificados y 	PKs</h2>


<p>
La generación de certificados y claves públicas se lleva a cabo de la siguiente manera.
</p>
<p>
Primero el CA raíz emite su certificado autofirmado después los CA subordinados emiten un csr firmado por ellos en el que adjuntan su clave pública y alguna otra información. Esta solicitud se envía a la autoridad superior, en este caso el Papa, el cual “revisa”(de forma conceptual) la solicitud y les genera un certificado firmado por el. Este certificado se guarda junto al certificado de la autoridad que lo ha firmado (para simplificar luego el proceso de buscar autoridades comunes). 
</p>
<p>
Un usuario final (el servidor y el cliente) solicita los certificados a sus respectivas autoridades seleccionadas. Y al igual que antes se genera un csr que se envía a la autoridad, la cual lo “revisa” y firma.
</p>
<p>
A nivel implementación hemos incluido un certificado dentro de otro de forma recursiva para simplificar la búsqueda de autoridades comunes
</p>
<p>
Para los procesos que lo requieren, las claves públicas siempre se obtienen de los certificados y siempre que se recibe un certificado (ya sea cliente o servidor) se verifica la validez de este y que haya sido emitido por una autoridad de confianza.
</p>
<h1>Complejidad y código de la aplicación</h1>


<p>
Consideramos que nuestra aplicación es considerablemente compleja, en lo que a su funcionamiento interno se refiere. Hemos preferido afianzar una correcta y potente implementación de nuestros conocimientos en lugar de centrarnos en la parte estética de la misma. De esta manera, hacemos que sea muy fácil extender el código en el futuro y que quede muy claro cuál es la estructura de nuestro código, el cual podría ser modelizado resumidamente de la siguiente manera:
</p>

<p>
En el diagrama, se puede contemplar cómo es posible obtener imágenes del servidor desde la ventana principal así como desde la ventana de usuario, esto es porque es posible pedir imágenes al servidor a través del cliente sin haberse autenticado inicialmente, de esta forma, el cliente dará a la interfaz las imágenes tal y como se las ha entregado el servidor, es decir; encriptadas. Cabe destacar, además, que es notable cómo no es posible que ninguna imagen salga del lado del cliente sin encriptar. 
</p>
<p>
Además ha sido necesario implementar algunos patrones de diseño como singleton para las clases de las autoridades.
</p>
<p>
 
</p>
<h1>Mejoras</h1>


<ul>

<li>Tratamiento de imágenes

<li>Almacenamiento en base de  datos 
<ul>
 
<li>Almacenamiento de imágenes
 
<li>Almacenamiento de claves/usuarios
</li> 
</ul>

<li>Validación de datos introducidos por el usuario

<li>Rotación de claves

<li>Sistema de logs

<li>Cifrado simétrico Y asimétrico  
<ul>
 
<li>Todas las operaciones de login, register y auth usan RSA 	
 
<li>El encriptado de las imágenes usa AES y RSA 
</li> 
</ul>

<li>Interfaz gráfica 
<ul>
 
<li>Pantallas de carga
 
<li>Ventanas emergentes 
 
<li>Control de errores
 
<li>Selección de región a encriptar
 
<li>Capacidad de eliminar y añadir usuarios
</li> 
</ul>
</li> 
</ul>
<p>

</p>
<h1>Anexo</h1>


<h2>Link al repositorio</h2>


<p>
<a href="https://github.com/Ragarr/Criptografia_2023-24">https://github.com/Ragarr/Criptografia_2023-24</a>
</p>
