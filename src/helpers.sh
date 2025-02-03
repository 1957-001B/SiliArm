#!/bin/bash


if [[ "$1" == "diff" ]]; then 
  if [[ "$2" == "dump" ]]; then 
    echo " "
    echo "Reference:"
    hexdump -C reference.o
    echo " "
    echo "Output:"
    hexdump -C output.o

  elif [[ "$2" == "headers" ]]; then 
    echo " "
    otool -l reference.o
    otool -l output.o
 fi
fi

if [[ "$1" == "ld" ]]; then 
  ld -arch arm64 -platform_version macos 13.0.0 13.0.0 -o test ../output.o
fi

if [[ "$1" == "run" ]]; then 
  python3 assemble.py test.s -o ../output.o
fi

if [[ "$1" == "info" ]]; then 
  hexdump -C $2 
  echo " "
  otool -l $2
fi
