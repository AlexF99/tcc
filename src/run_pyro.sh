#!/bin/bash

# Define the paths to the JAR files and the datasets directory
METANOME_CLI_JAR="metanome-cli-1.1.0.jar"
PYRO_JAR="./algorithms/pyro-distro-1.0-SNAPSHOT-distro.jar"
HYFD_JAR="./algorithms/HyFD-1.2-SNAPSHOT.jar"
DATASETS_DIR="../datasets/experiments"
RESULTS_DIR="results"

# Get the dataset path from the first parameter
if [ -z "$1" ]; then
  echo "Error: Dataset path not provided. Usage: $0 <dataset_path> [threshold]"
  exit 1
fi

dataset="$1"
threshold="$2"
echo "Processing dataset: $dataset"

# Create results directory if it doesn't exist
mkdir -p "$RESULTS_DIR"

# Set up the base command
base_command="java -cp $METANOME_CLI_JAR:$PYRO_JAR de.metanome.cli.App --algorithm de.hpi.isg.pyro.algorithms.Pyro"
base_command+=" --files $dataset"
base_command+=" --file-key inputFile"
base_command+=" --separator \",\""
base_command+=" --algorithm-config isFindKeys:false"
base_command+=" --algorithm-config isFindFds:true"

# Add threshold parameters if threshold is provided
if [ -n "$threshold" ]; then
  echo "Using threshold value: $threshold"
  base_command+=" --algorithm-config maxUccError:$threshold"
  base_command+=" --algorithm-config errorDev:$threshold"
fi

# Add output filename
output_filename="pyro_$(basename "$dataset" .csv)"
if [ -n "$threshold" ]; then
  output_filename="${output_filename}_threshold_$(echo $threshold | tr ',' '_' | tr '.' '_')"
fi

base_command+=" --output file:$output_filename"
base_command+=" --header"

# Execute the command
echo "Executing: $base_command"
$base_command

echo "Pyro algorithm completed"