#!/bin/bash

benchmark=$1

if [[ $benchmark == "disk-no-synch" || $benchmark == "disk-synch" ]]; then
    if [[ ! -d benchmark ]]; then
	echo "No benchmark folder"
    fi
    #    bash disk-prepare-data.sh "$2" $benchmark/"$3"
fi
