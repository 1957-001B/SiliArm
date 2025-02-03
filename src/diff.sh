if [[ "$1" == "dump" ]]; then 
  echo "\n"
  echo "Reference:"
  hexdump -C reference.o
  echo "\n"
  echo "Output:"
  hexdump -C output.o

elif [[ "$1" == "headers" ]]; then 
  echo "\n"
  otool -l reference.o
  otool -l output.o

fi
