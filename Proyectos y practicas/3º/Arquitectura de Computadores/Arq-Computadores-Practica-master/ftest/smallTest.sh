#!/bin/bash

# Parámetros de ejecución
smallInputFile="inputFiles/small.fld"
output_file="output.fld"
parentDir="$(dirname "$(pwd)")"
fluid_executable="${parentDir}/cmake-build-debug/fluid/fluid"


smallTrace1="trazas/small/boundint-base-1.trz"
smallTrace2="trazas/small/boundint-base-2.trz"
smallTrace3="trazas/small/boundint-base-3.trz"
smallTrace4="trazas/small/boundint-base-4.trz"
smallTrace5="trazas/small/boundint-base-5.trz"


tests_passed=0
# TEST 1
echo "TEST SMALL 1"
"$fluid_executable" 1 "$smallInputFile" "$output_file"
diffResult=$(diff "$output_file" "$smallTrace1")

if [ "$diffResult" == "" ]; then
  echo "TEST SMALL 1 PASSED"
   ((tests_passed++))
else
  echo "TEST SMALL 1 FAILED - $diffResult"
fi

# TEST SMALL 2
echo "TEST SMALL 2"
"$fluid_executable" 2 "$smallInputFile" "$output_file"
diffResult=$(diff "$output_file" "$smallTrace2")

if [ "$diffResult" == "" ]; then
  echo "TEST SMALL 2 PASSED"
   ((tests_passed++))
else
  echo "TEST SMALL 2 FAILED - $diffResult"
fi

# TEST SMALL 3
echo "TEST SMALL 3"
"$fluid_executable" 3 "$smallInputFile" "$output_file"
diffResult=$(diff "$output_file" "$smallTrace3")

if [ "$diffResult" == "" ]; then
  echo "TEST SMALL 3 PASSED"
   ((tests_passed++))
else
  echo "TEST SMALL 3 FAILED - $diffResult"
fi

# TEST SMALL 4
echo "TEST SMALL 4"
"$fluid_executable" 4 "$smallInputFile" "$output_file"
diffResult=$(diff "$output_file" "$smallTrace4")

if [ "$diffResult" == "" ]; then
  echo "TEST SMALL 4 PASSED"
   ((tests_passed++))
else
  echo "TEST SMALL 4 FAILED - $diffResult"
fi

# TEST SMALL 5
echo "TEST SMALL 5"
"$fluid_executable" 5 "$smallInputFile" "$output_file"
diffResult=$(diff "$output_file" "$smallTrace5")

if [ "$diffResult" == "" ]; then
  echo "TEST SMALL 5 PASSED"
   ((tests_passed++))
else
  echo "TEST SMALL 5 FAILED - $diffResult"
fi

echo "TESTS PASSED: $tests_passed of 5"