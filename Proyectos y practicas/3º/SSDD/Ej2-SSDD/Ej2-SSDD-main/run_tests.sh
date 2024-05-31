#!/bin/bash

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)
export IP_TUPLAS=localhost
export PORT_TUPLAS=9090

echo "Presiona Enter para ejecutar cada comando. Presiona Ctrl+C para salir."

# Función para esperar a que el usuario presione Enter
press_enter() {
    read -p "Presiona Enter para ejecutar el siguiente comando (o Ctrl+C para salir)"
}

# Ejecución de comandos
press_enter
./cliente tests/valids/init

press_enter
./cliente tests/valids/set

press_enter
./cliente tests/valids/get

press_enter
./cliente tests/valids/modify

press_enter
./cliente tests/valids/exist

press_enter
./cliente tests/valids/delete

press_enter
./cliente tests/valids/copy

press_enter
./cliente tests/invalids/set

press_enter
./cliente tests/invalids/get

press_enter
./cliente tests/invalids/modify

press_enter
./cliente tests/invalids/delete

press_enter
./cliente tests/invalids/copy
