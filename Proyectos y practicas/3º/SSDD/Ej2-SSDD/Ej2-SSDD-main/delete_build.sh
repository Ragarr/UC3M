#!/bin/bash

# Elimina archivos .o en la misma carpeta
find . -maxdepth 1 -type f -name "*.o" ! -path "*/.git/*" -exec rm -f {} \;

# Elimina archivos .so en la misma carpeta
find . -maxdepth 1 -type f -name "*.so" ! -path "*/.git/*" -exec rm -f {} \;

# Elimina archivos sin extensión, excepto 'makefile' y excepto en la carpeta .git en la misma carpeta
find . -maxdepth 1 -type f ! -name "*.*" ! -name "makefile" ! -path "*/.git/*" -exec rm -f {} \;

# Elimina archivos .debug en la misma carpeta
find . -maxdepth 1 -type f -name "*.debug" ! -path "*/.git/*" -exec rm -f {} \;
