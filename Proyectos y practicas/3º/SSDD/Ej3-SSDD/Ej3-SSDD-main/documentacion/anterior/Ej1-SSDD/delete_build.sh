#!/bin/bash

# Cambia a tu directorio objetivo


# Elimina archivos .o
find . -type f -name "*.o" ! -path "*/.git/*" -exec rm -f {} \;

# Elimina archivos .so
find . -type f -name "*.so" ! -path "*/.git/*" -exec rm -f {} \;

# Elimina archivos sin extensión, excepto 'makefile' y excepto en la carpeta .git
find . -type f ! -name "*.*" ! -name "makefile" ! -path "*/.git/*" -exec rm -f {} \;
