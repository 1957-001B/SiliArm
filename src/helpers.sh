#!/bin/bash

if [[ "$1" == "diff" ]]; then 
  if [[ "$2" == "dump" ]]; then 
    echo " "
    echo "Reference:"
    hexdump -C reference.o
    echo " "
    rm output.o
    python3 assemble.py test.s -o output.o
    echo "Output:"
    hexdump -C output.o

  elif [[ "$2" == "headers" ]]; then 
    echo " "
    otool -l reference.o
    rm output.o
    python3 assemble.py test.s -o output.o
    otool -l output.o
 fi
fi

if [[ "$1" == "ld" ]]; then 
  rm output.o
  python3 assemble.py test.s -o output.o
  ld -arch arm64 -platform_version macos 13.0.0 13.0.0 -o test output.o
fi

if [[ "$1" == "debug" ]]; then 
  DEBUG=1 python3 assemble.py test.s -o ../output.o
fi

if [[ "$1" == "info" ]]; then 
  hexdump -C $2 
  echo " "
  otool -l $2
fi


if [[ "$1" == "sz" ]]; then 
  echo "Total Lines:"
  find . -name "*.py" -type f | xargs wc -l | tail -n 1 | awk '{print $1}'
fi
