#!bin/bash


if [ -z $1 ];
	then SAT=5;
	else SAT=$1;
fi


echo "Satisfiable"
for i in $( eval echo {1..$SAT} )
do
  echo "Runing instance "$i
  inst="uf20-91/uf20-0"$i".cnf"
  python main.py -p $inst
done

if [ $2 ]; then
  echo "===================================="
  echo "Unsatisfiable"
  for i in $( eval echo {1..$2} )
  do
    echo "Runing instance "$i
    inst="uuf50-218/UUF50.218.1000/uuf50-0"$i".cnf"
    python main.py -p $inst
  done;
fi
