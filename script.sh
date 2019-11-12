#!bin/bash


if [ -z $1 ];
	then SAT=4;
	else SAT=$1;
fi

if [ -z $2 ];
	then USAT=2;
	else USAT=$2;
fi

echo "Satisfiable"
for i in $( eval echo {1..$SAT} )
do
  echo "Runing instance "$i
  inst="uf20-91/uf20-0"$i".cnf"
  python main.py -p $inst
done

echo "===================================="
echo "Unsatisfiable"
for i in $( eval echo {1..$USAT} )
do
  echo "Runing instance "$i
  inst="uuf50-218/UUF50.218.1000/uuf50-0"$i".cnf"
  python main.py -p $inst
done
