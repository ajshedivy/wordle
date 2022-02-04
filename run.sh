#!/bin/bash

echo "activate wordle environment"
eval "$(conda shell.bash hook)"
conda activate wordle

if [ $? -ne 0 ]; then
   	echo "environment does not exist"
	echo "creating wordle environment"
	conda env create -f env.yml
	conda activate wordle
fi
echo "environment activated"

python app.py