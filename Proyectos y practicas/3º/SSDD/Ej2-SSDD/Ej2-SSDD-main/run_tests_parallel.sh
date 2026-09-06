#!/bin/bash

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)
export IP_TUPLAS=localhost
export PORT_TUPLAS=9090

# Ejecución de comandos
./cliente tests/valids/init & 

./cliente tests/valids/set &

./cliente tests/valids/get &

./cliente tests/valids/modify &

./cliente tests/valids/exist & 

./cliente tests/valids/delete   &

./cliente tests/valids/copy &

./cliente tests/invalids/set    &

./cliente tests/invalids/get &

./cliente tests/invalids/modify &

./cliente tests/invalids/delete &

./cliente tests/invalids/copy   &
