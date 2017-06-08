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
echo "Created pool folder."

# TODO: Run benchmarks
echo "Running benchmarks..."
cp pool/data/container-* $folder
echo "All Done."

# Prepare data
echo "Preparing data..."
output=$(date +%F_%T)
bash scripts/disk-prepare-data.sh "$folder/*" benchmarks/$benchmark/$output
echo "Created report data file."

# # Draw plots
# echo "Drawing plots..."
# cd benchmarks/$benchmark
# python ../../scripts/aggregator.py ../../config/plot-benchmark.json 
# python ../../scripts/plot_data.py ../../config/plot-$benchmark.json benchmarks/$benchmark/$output.values
# cd ../../
# echo "Drawing done."

# Clean up benchmark folder
echo "Clean up..."
rm -rf $folder
rm benchmarks/$benchmark/$output.values
echo "Done."

echo "Data Report can be found in benchmarks/$benchmark"
