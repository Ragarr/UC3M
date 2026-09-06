# SSDD - P2 - 100472050
Este proyecto consiste en el desarrollo de un sistema peer-to-peer de distribución de archivos entre clientes. El proyecto se divide en dos partes: la primera parte implica la implementación de un servidor concurrente multihilo en C y un cliente multihilo en Python que se comunican utilizando sockets TCP. Se implementan funcionalidades como registro/baja de usuarios, conexión/desconexión, publicación/eliminación de contenidos, listado de usuarios y contenidos, y transferencia de archivos entre clientes.
En la segunda parte, se añade un servicio web en Python para obtener la fecha del sistema, y un servidor RPC en C que registra todas las operaciones realizadas por los clientes. Se utiliza el modelo ONC-RPC para la implementación del servidor RPC. Además, se integra el servicio web con el cliente Python para enviar la fecha actual junto con cada operación realizada.


El objetivo de este readme es explicar la compilación y ejecución de los programas de la práctica 2 de la asignatura de Sistemas Distribuidos, así como la ejecución de los tests.
Otros aspectos se explican en la memoria de la práctica.


## Estructura del proyecto
Cabe mencionar que la estructura de los archivos es la siguiente:
- `client/`: Contiene el código fuente del cliente.
- `server/`: Contiene el código fuente del servidor.
- `rpc_service/`: Contiene el código fuente del servicio RPC.
- `web_server/`: Contiene el código fuente del servidor web.
- `tests/`: Contiene los tests de la práctica.

Cada una de estas carpetas contiene lo necesario para ejecutar dicho componente de forma independiente (a excepcion del servidor, el cual necesita la libreria dinamica que genera el rpc_service tras su compilacion, esto se explica en la seccion de compilacion manual).

## Compilación
### Compilacion (y ejecucion) automática
Para simplificar la tarea de la compilacion y ejecucion del proyecto se ha escrito un script de python que se encarga de compilar y ejecutar el proyecto.
Dicho script se encuentra en la raiz del proyecto y se llama `setup.py`. Este script toma 3 posibles argumentos:
- `--clean` | `-c`: Borra todos los archivos generados por la compilacion.
- `--build` | `-b`: Compila los archivos de server, rpc_service e instala las dependencias necesarias.
- `--run` | `-r`: Ejecuta el rpc_service, el web_server y el servidor. De esta forma solo queda por ejecutar tantos clientes como se desee.
- `--help` | `-h`: Muestra la ayuda del script.

Una ejecucion tipica (la recomenda si se va a ejecutar todos los componentes del servidor en la misma maquina) del script seria:
```bash
python3 setup.py -cbr
```
Esto hara una compilacion limpia y ejecutara el servidor, el rpc_service y el web_server.


La salida de este script sera algo similar a:
```bash
... # Salida de la limpieza y compilacion
Server, logger and web service running.
Server PID: 23442
Logger PID: 23441
Web service PID: 23443

Server IP: 192.168.1.49
Server Port: 9090
Web service URL: http://192.168.1.49:8000
Web service WSDL URL: http://192.168.1.49:8000/?wsdl
Para ejecutar el cliente establece la variable de entorno 'WSDL_URL' a 'http://192.168.1.49:8000/?wsdl'
Press Ctrl+C to stop the processes.

Server output will be shown in server.out file.
Web service output will be shown in ws_time_service.out file.
Logger output will be shown in this terminal.
```
Una vez a terminado el script (el cual se mantendra ejecutandose hasta que se presione CTRL+C), en una terminal diferente se puede ejecutar el cliente siguiendo los siguientes pasos.
1. Establecer la variable de entorno `WSDL_URL` con la URL del servicio web. En el caso anterior seria: `export WSDL_URL="http://192.168.1.49:8000/?wsdl"`

2. Ejecutar el cliente se deben proporcionar como argumentos la direccion del servidor y el puerto del servidor. Siguiendo el ejemplo anterior: `python3 client/client.py -s 192.168.1.49 -p 9090`

### Compilación manual
Para compilar uno a uno y de forma manual los programas se debe seguir los siguientes pasos:
1. Compilar el servicio RPC:
```bash
cd rpc_service
make
```
2. Mover la libreria generada a la carpeta del servidor:
```bash
mv liblogger.so ../server/
```

3. Compilar el servidor:
```bash
cd ../server
make
```
4. Instalar las dependencias del servidor web:
```bash
cd ../web_service
pip3 install -r requirements.txt
```
5. Instalar las dependencias del cliente:
```bash
cd ../client
pip3 install -r requirements.txt
```

## Ejecución manual

Una vez generados los ejecutables, se pueden ejecutar de la siguiente forma, estos son exactamente los mismos pasos que se siguen en el script de python, pero de forma manual.

1. Ejecutar el servicio RPC:
```bash
cd rpc_service
./rpc_service
```
2. Ejecutar el servidor, en una terminal diferente:
```bash
cd server
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:. # Para que el servidor pueda encontrar la libreria dinamica
export LOGGER_HOST=localhost # Para que el servidor pueda encontrar el servicio RPC, si no se esta ejecutando en la misma maquina, cambiar localhost por la IP del RPC service
./server -p 9090 # El puerto puede ser cualquier puerto libre
``` 
3. Ejecutar el servidor web, en una terminal diferente:
```bash
cd web_service
python3 ws_time_service.py
```
4. Ejecutar el cliente, en una terminal diferente:
```bash
cd client
export WSDL_URL="http://localhost:8000/?wsdl" # La URL del servicio web, que se muestra en la salida del servidor web al ejecutarlo
python3 client.py -s localhost -p 9090 # La IP y puerto del servidor
```

## Ejecución de los tests
Para ejecutar los tests se debe seguir los siguientes pasos:
1. Compilar todos los programas, siguiendo los pasos de la sección de compilación.
2. NO ejecutar ningun programa ya que los tests se encargan de ejecutar los programas necesarios.
3. Ejecutar los tests:
```bash
cd tests
python3 test_client_valids.py
python3 test_client_invalids.py
python3 test_server.py
python3 test_multiclient.py
```
El contenido de los tests se explica en la memoria de la práctica.
