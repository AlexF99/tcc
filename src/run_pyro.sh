#!/bin/bash

# Define the paths to the JAR files and the datasets directory
METANOME_CLI_JAR="metanome-cli-1.1.0.jar"
PYRO_JAR="./algorithms/pyro-distro-1.0-SNAPSHOT-distro.jar"
HYFD_JAR="./algorithms/HyFD-1.2-SNAPSHOT.jar"
DATASETS_DIR="../datasets/experiments"
RESULTS_DIR="results"
# Get the dataset path from the first parameter
if [ -z "$1" ]; then
  echo "Error: Dataset path not provided. Usage: $0 <dataset_path>"
  exit 1
fi

dataset="$1"
echo "Processing dataset: $dataset"

# Create results directory if it doesn't exist
mkdir -p "$RESULTS_DIR"


java -cp "$METANOME_CLI_JAR:$PYRO_JAR" de.metanome.cli.App --algorithm de.hpi.isg.pyro.algorithms.Pyro \
  --files "$dataset" \
  --file-key inputFile \
  --separator "," \
  --algorithm-config isFindKeys:false \
  --algorithm-config isFindFds:true \
  --output file:pyro_$(basename "$dataset" .csv) \
  --header 

echo "Pyro algorithm completed"