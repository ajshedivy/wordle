#!/bin/bash

if (($# != 1)) || [ "$1" != "web" ] && [ "$1" != "terminal" ]; then
    echo "usage: bash run.sh [web|terminal]"
    exit 0
fi

echo "activate wordle environment"
eval "$(conda shell.bash hook)"
conda activate wordle

if [ $? -ne 0 ]; then
   	echo "environment does not exist"
	echo "creating wordle environment"
	conda env create -n wordle -f requirements.txt
	conda activate wordle
fi
echo "environment activated"

if [ "$1" == "web" ]; then
    python app.py
fi

if [ "$1" == "terminal" ]; then
    python main.py
fi