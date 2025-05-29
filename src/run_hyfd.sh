#!/bin/bash

# Define the paths to the JAR files and the datasets directory
METANOME_CLI_JAR="metanome-cli-1.1.0.jar"
HYFD_JAR="./algorithms/HyFD-1.2-SNAPSHOT.jar"
DATASETS_DIR="../datasets/experiments"

# Get the dataset path from the first parameter
if [ -z "$1" ]; then
  echo "Error: Dataset path not provided. Usage: $0 <dataset_path>"
  exit 1
fi

dataset="$1"
echo "Processing dataset: $dataset"

java -cp "$METANOME_CLI_JAR:$HYFD_JAR" de.metanome.cli.App --algorithm de.metanome.algorithms.hyfd.HyFD \
    --files "$dataset" \
    --file-key INPUT_GENERATOR \
    --header \
    --output file:hyfd_$(basename "$dataset" .csv) \
    --separator ","