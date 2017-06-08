#!/bin/bash

function error() {
   echo $1 > /dev/stderr
}

if [[ -z $1 ]]; then
    error "Expected string as first argument."
    exit -1
fi

if [[ -z $2 ]]; then
    error "Output name is empty."
    exit -1
fi

files=$1
output=$2.data
values=$2.values

# Write header
printf "# Document length [bytes]
# I/O [KB], Bandwith [KB/s], I/O Operations Runtime [msec]\n" > $output
printf "Read\tWrite\n" >> $output

# Clean values file
printf "" > $values

# Print stats
for file in $files; do
    read_stat=$(grep read $file | tr -cd [:digit:][:blank:]'\n'. | tr -s ',' ' ' | cut -d ' ' -f 2-5)
    write_stat=$(grep write $file | tr -cd [:digit:][:blank:]'\n'. | tr -s ',' ' ' | cut -d ' ' -f 2-5)
    if [[ -n $read_stat && -n $write_stat ]]; then
	echo $read_stat $write_stat >> $output
	echo $read_stat $write_stat >> $values
    fi
done
