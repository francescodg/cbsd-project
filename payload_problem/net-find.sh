#!/bin/bash

TYPE=$1
WEB_ADDRESS=$2
OUTPUT=$TYPE.values

printf "" > $OUTPUT

for ((i=0; i<=2048; i+=$(echo "2048/20" | bc))); do
    DATA_SIZE=$(echo "$i" | bc)
    VALUE=$(sudo chrt -f 99 taskset -c 1 ab -q -n 10 -c 1 http://$WEB_ADDRESS:5000/random?size=$DATA_SIZE | \
	grep "Time per request" | sed s/\ \ */\ /g | head -n 1 | tr -cd [:digit:].\\n)
    printf "%d %f\n" $DATA_SIZE $VALUE >> $OUTPUT
done

