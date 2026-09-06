#!/bin/bash

# Parámetros de ejecución
largeInputFile="inputFiles/large.fld"
output_file="output.fld"

parentDir="$(dirname "$(pwd)")"
fluid_executable="${parentDir}/cmake-build-debug/fluid/fluid"


largeTrace1="trazas/large/boundint-base-1.trz"
largeTrace2="trazas/large/boundint-base-2.trz"
largeTrace3="trazas/large/boundint-base-3.trz"
largeTrace4="trazas/large/boundint-base-4.trz"
largeTrace5="trazas/large/boundint-base-5.trz"

# TEST 1
echo "TEST LARGE 1"
"$fluid_executable" 1 "$largeInputFile" "$output_file"
diffResult=$(diff "$output_file" "$largeTrace1")

if [ "$diffResult" == "" ]; then
  echo "TEST LARGE 1 PASSED"
else
  echo "TEST LARGE 1 FAILED - $diffResult"
fi

# TEST LARGE 2
echo "TEST LARGE 2"
"$fluid_executable" 2 "$largeInputFile" "$output_file"
diffResult=$(diff "$output_file" "$largeTrace2")

if [ "$diffResult" == "" ]; then
  echo "TEST LARGE 2 PASSED"
else
  echo "TEST LARGE 2 FAILED - $diffResult"
fi

# TEST LARGE 3
echo "TEST LARGE 3"
"$fluid_executable" 3 "$largeInputFile" "$output_file"
diffResult=$(diff "$output_file" "$largeTrace3")

if [ "$diffResult" == "" ]; then
  echo "TEST LARGE 3 PASSED"
else
  echo "TEST LARGE 3 FAILED - $diffResult"
fi

# TEST LARGE 4
echo "TEST LARGE 4"
"$fluid_executable" 4 "$largeInputFile" "$output_file"
diffResult=$(diff "$output_file" "$largeTrace4")

if [ "$diffResult" == "" ]; then
  echo "TEST LARGE 4 PASSED"
else
  echo "TEST LARGE 4 FAILED - $diffResult"
fi

# TEST LARGE 5
echo "TEST LARGE 5"
"$fluid_executable" 5 "$largeInputFile" "$output_file"
diffResult=$(diff "$output_file" "$largeTrace5")

if [ "$diffResult" == "" ]; then
  echo "TEST LARGE 5 PASSED"
   ((tests_passed++))
else
  echo "TEST LARGE 5 FAILED - $diffResult"
fi

rm "$output_file"

echo "TESTS PASSED: $tests_passed of 5"