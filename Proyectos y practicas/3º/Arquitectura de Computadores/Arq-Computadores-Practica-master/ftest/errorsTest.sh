#!/bin/bash

smallInputFile="inputFiles/small.fld"
parentDir="$(dirname "$(pwd)")"
fluid_executable="${parentDir}/cmake-build-debug/fluid/fluid"
tests_passed=0
particleMissmathchPath="${parentDir}/ftest/inputFiles/np_incorrect.fld"
particleNegativePath="${parentDir}/ftest/inputFiles/np_negative.fld"

# Prueba 1: Número incorrecto de argumentos (0)
echo ""
echo "Prueba 1: Número incorrecto de argumentos (0)"
"$fluid_executable" 2>&1
if [ $? -eq 255 ]; then
    echo "Prueba 1 PASSED"
    ((tests_passed++))
else
    echo "Prueba 1 FAILED  -> $?"
fi

# Prueba 2: Número incorrecto de argumentos (1)
echo ""
echo "Prueba 2: Número incorrecto de argumentos (1)"
"$fluid_executable" 4 2>&1
if [ $? -eq 255 ]; then
    echo "Prueba 2 PASSED"
    ((tests_passed++))
else
    echo "Prueba 2 FAILED  -> $?"
fi

# Prueba 3: Número incorrecto de argumentos (2)
echo ""
echo "Prueba 3: Número incorrecto de argumentos (2)"
"$fluid_executable" 2000 init.fld 2>&1
if [ $? -eq 255 ]; then
    echo "Prueba 3 PASSED"
    ((tests_passed++))
else
    echo "Prueba 3 FAILED  -> $?"
fi

# Prueba 4: Número incorrecto de argumentos (4)
echo ""
echo "Prueba 4: Número incorrecto de argumentos (4)"
"$fluid_executable" 2000 init.fld final.fld 45 2>&1
if [ $? -eq 255 ]; then
    echo "Prueba 4 PASSED"
    ((tests_passed++))
else
    echo "Prueba 4 FAILED  -> $?"
fi

# Prueba 5: El primer argumento no es un número entero
echo ""
echo "Prueba 5: El primer argumento no es un número entero"
"$fluid_executable" hello "$smallInputFile" final.fld 2>&1
if [ $? -eq 255 ]; then
    echo "Prueba 5 PASSED"
    ((tests_passed++))
else
    echo "Prueba 5 FAILED  -> $?"
fi

# Prueba 6: Número de pasos de tiempo es un número negativo
echo ""
echo "Prueba 6: Número de pasos de tiempo es un número negativo"
"$fluid_executable" -3 "$smallInputFile" final.fld 2>&1
if [ $? -eq 254 ]; then
    echo "Prueba 6 PASSED"
    ((tests_passed++))
else
    echo "Prueba 6 FAILED  -> $?"
fi

# Prueba 7: No se puede abrir el archivo de entrada para lectura
echo ""
echo "Prueba 7: No se puede abrir el archivo de entrada para lectura"
"$fluid_executable" 1 inexistant.fld final.fld 2>&1
if [ $? -eq 253 ]; then
    echo "Prueba 7 PASSED"
    ((tests_passed++))
else
    echo "Prueba 7 FAILED  -> $?"
fi

# Prueba 8: No se puede abrir el archivo de salida para escritura
# Crear un directorio temporal con permisos restrictivos (sin permisos de escritura)
temp_dir=$(mktemp -d)
chmod a-w "$temp_dir"

# Asignar el archivo de salida dentro del directorio temporal
output_file="$temp_dir/final.fld"
echo ""
echo "Prueba 8: No se puede abrir el archivo de salida para escritura"
"$fluid_executable" 5 "$smallInputFile" "$output_file" 2>&1
if [ $? -eq 252 ]; then
    echo "Prueba 8 PASSED"
    ((tests_passed++))
else
    echo "Prueba 8 FAILED  -> $?"
fi

# Limpiar el directorio temporal después de la prueba
rm -r "$temp_dir"


# Prueba 9: Número de partículas incorrecto
echo ""
echo "Prueba 9: Número de partículas incorrecto"
"$fluid_executable" 1 "$particleMissmathchPath" final.fld 2>&1
if [ $? -eq 251 ]; then
    echo "Prueba 9 PASSED"
    ((tests_passed++))
else
    echo "Prueba 9 FAILED  -> $?"
fi

# Prueba 10: Número de partículas negativo
echo ""
echo "Prueba 10: Número de partículas negativo"
"$fluid_executable" 1 "$particleNegativePath" final.fld 2>&1
if [ $? -eq 251 ]; then
    echo "Prueba 10 PASSED"
    ((tests_passed++))
else
    echo "Prueba 10 FAILED  -> $?"
fi




echo "passed $tests_passed of 10 tests"