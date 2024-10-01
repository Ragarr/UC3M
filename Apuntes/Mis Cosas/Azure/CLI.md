# Ejercicio: Creación de una máquina virtual de Azure
Usa los siguientes comandos de la CLI de Azure para crear una máquina virtual Linux e instalar Nginx. Una vez creada la máquina virtual, usará la extensión de script personalizado para instalar Nginx. La extensión de script personalizado es una manera fácil de descargar y ejecutar scripts en máquinas virtuales de Azure. Solo es una de las numerosas formas de configurar el sistema después de que la máquina virtual esté en funcionamiento.

Desde Cloud Shell, ejecuta el siguiente comando `az vm create` para crear una máquina virtual Linux:
``` Azure ClI
az vm create \
  --resource-group learn-689f79c0-5a41-4921-948a-e1dc4656f55b \
  --name my-vm \
  --image UbuntuLTS \
  --admin-username azureuser \
  --generate-ssh-keys
```

Ejecuta el siguiente comando `az vm extension set` para configurar Nginx en la máquina virtual:
```Azure CLI
az vm extension set \
  --resource-group learn-689f79c0-5a41-4921-948a-e1dc4656f55b \
  --vm-name my-vm \
  --name customScript \
  --publisher Microsoft.Azure.Extensions \
  --version 2.1 \
  --settings '{"fileUris":["https://raw.githubusercontent.com/MicrosoftDocs/mslearn-welcome-to-azure/master/configure-nginx.sh"]}' \
  --protected-settings '{"commandToExecute": "./configure-nginx.sh"}'
```

## Tarea 1: Acceso al servidor web

En este procedimiento se obtiene la dirección IP de la máquina virtual y se intenta acceder a la página principal del servidor web.

1. Ejecute el siguiente comando `az vm list-ip-addresses` para obtener la dirección IP de la máquina virtual y almacenar el resultado como una variable de Bash:

```
IPADDRESS="$(az vm list-ip-addresses \
  --resource-group learn-689f79c0-5a41-4921-948a-e1dc4656f55b \
  --name my-vm \
  --query "[].virtualMachine.network.publicIpAddresses[*].ipAddress" \
  --output tsv)"
```

```
echo $IPADDRESS
```

Ejecuta el siguiente comando `az network nsg list` para que muestre los grupos de seguridad de red asociados a la máquina virtual:
```
az network nsg list \
  --resource-group learn-689f79c0-5a41-4921-948a-e1dc4656f55b \
  --query '[].name' \
  --output tsv
```
Cada máquina virtual de Azure está asociada a, al menos, un grupo de seguridad de red. En este caso, Azure te creó un grupo de seguridad de red denominado_my-vmNSG.

## Tarea 2: Enumeración de las reglas de grupo de seguridad de red actuales

Ejecuta el siguiente comando `az network nsg rule list` mostrar las reglas asociadas al grupo de seguridad de red denominado _my-vmNSG_:
```
az network nsg rule list \
  --resource-group learn-689f79c0-5a41-4921-948a-e1dc4656f55b \
  --nsg-name my-vmNSG

```
Verás un bloque grande de texto en formato JSON en la salida. En el paso siguiente, ejecutarás un comando similar que facilita la lectura de este resultado.

Ejecuta por segunda vez el comando `az network nsg rule list`. Esta vez, use el argumento `--query` para recuperar solo el nombre, la prioridad, los puertos afectados y el acceso (**Permitir** o **Denegar**) para cada regla. El argumento `--output` da formato a la salida como una tabla para que sea fácil de leer.
```
az network nsg rule list \
  --resource-group learn-689f79c0-5a41-4921-948a-e1dc4656f55b \
  --nsg-name my-vmNSG \
  --query '[].{Name:name, Priority:priority, Port:destinationPortRange, Access:access}' \
  --output table
```
Verás la regla predeterminada _default-allow-ssh_. Esta regla permite conexiones entrantes a través del puerto 22 (SSH). SSH (Secure Shell) es un protocolo que se usa en Linux para permitir que los administradores accedan al sistema de forma remota. La prioridad de esta entrada es 1000. Las reglas se procesan en orden de prioridad, donde los números más bajos se procesan antes que los números más altos.

## Tarea 3: Creación de la regla de seguridad de red

En este caso, crearás una regla de seguridad de red que permita el acceso de entrada en el puerto 80 (HTTP).

1. Ejecute el siguiente comando `az network nsg rule create` para crear una regla denominada _allow-http_ que permita el acceso entrante en el puerto 80:
```
az network nsg rule create \
  --resource-group learn-689f79c0-5a41-4921-948a-e1dc4656f55b \
  --nsg-name my-vmNSG \
  --name allow-http \
  --protocol tcp \
  --priority 100 \
  --destination-port-range 80 \
  --access Allow

```
Con fines de aprendizaje, aquí establecerá la prioridad en 100. En este caso, la prioridad no importa. Tendriás que tener en cuenta la prioridad si tuvieras intervalos de puertos superpuestos.

Para comprobar la configuración, ejecuta `az network nsg rule list` para ver la lista actualizada de reglas:
```
az network nsg rule list \
  --resource-group learn-689f79c0-5a41-4921-948a-e1dc4656f55b \
  --nsg-name my-vmNSG \
  --query '[].{Name:name, Priority:priority, Port:destinationPortRange, Access:access}' \
  --output table

```
Verás las dos reglas, _default-allow-ssh_ y la nueva regla _allow-http_:

Resultados
```
Name              Priority    Port    Access
-----------------  ----------  ------  --------
default-allow-ssh  1000        22      Allow
allow-http        100        80      Allow
```

## Tarea 4: Nuevo acceso al servidor web
Ejecuta el mismo comando `curl` que has ejecutado antes:

```
curl --connect-timeout 5 http://$IPADDRESS
```

Verá lo siguiente:
```
<html><body><h2>Welcome to Azure! My name is my-vm.</h2></body></html>

```

- Como paso opcional, actualiza la pestaña que apunta al servidor web.
Verá lo siguiente:
![Captura de pantalla de un explorador web en el que se muestra la página de inicio del servidor web con un mensaje de bienvenida.](https://learn.microsoft.com/es-es/training/wwl-azure/describe-azure-compute-networking-services/media/browser-request-successful-df21c6f1.png)

