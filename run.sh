#!/bin/bash

if (($# == 0)); then
    echo "usage: bash run.sh --option [web|terminal]"
    exit 0
fi

POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    -o|--option)
      EXTENSION="$2"
      shift # past argument
      shift # past value
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
    *)
      POSITIONAL_ARGS+=("$1") # save positional arg
      shift # past argument
      ;;
  esac
done
set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters

echo "GAME OPTION  = ${EXTENSION}"

if [[ -n $1 ]]; then
    echo "Last line of file specified as non-opt/last argument:"
    echo "usage: bash run.sh --option [web|terminal]"
    exit 0
fi

if [ ${EXTENSION} != "web" ] && [ ${EXTENSION} != "terminal" ]; then
    echo "invalid game mode"
    echo "usage: bash run.sh --option [web|terminal]"
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

if [ ${EXTENSION} == "web" ]; then
    python app.py
fi

if [ ${EXTENSION} == "terminal" ]; then
    python main.py
fi