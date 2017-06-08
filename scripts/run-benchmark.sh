#!/bin/bash

benchmark=$1

if [[ -z $benchmark ]]; then
    echo "Invalid benchmark."
    exit -1
fi

# TODO: Check if valid benchmark

# Create folder to store data
folder=pool/$benchmark/$(date +%F_%T)

mkdir -p $folder

# TODO: Run benchmarks
cp pool/data/container-* $folder

# Prepare data
bash scripts/disk-prepare-data.sh "$folder/*" benchmarks/$benchmark/"output"

# TODO: Draw plots
cd benchmarks/$benchmark
python ../../scripts/plot_data.py ../../config/plot-$benchmark.json
cd ../../

# Clean up benchmark folder
rm -rf $folder
