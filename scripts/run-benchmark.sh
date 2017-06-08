#!/bin/bash

benchmark=$1

if [[ -z $benchmark ]]; then
    echo "Invalid benchmark."
    exit -1
fi

# TODO Check if valid benchmark

mkdir -p pool/$benchmark/$(date +%F_%T)

