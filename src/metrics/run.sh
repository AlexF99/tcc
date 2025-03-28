#!/bin/bash

# Define the paths to the directories
RESULTS_DIR="../../metanome-cli/results"
DATASETS_DIR="../../datasets"
SCRIPT="main.py"

# Loop through each FD file in the results directory
for fd_file in "$RESULTS_DIR"/*; do
  # Extract the algorithm and dataset names from the FD filename
  filename=$(basename -- "$fd_file")
  algorithm="${filename%%-*}"
  dataset="${filename#*-}"
  type="metanome"

  # Construct the path to the dataset file
  dataset_file="$DATASETS_DIR/$dataset"

  # Check if the dataset file exists
  if [ -f "$dataset_file" ]; then
    # Construct the output directory name
    output_dir="${algorithm}-${dataset}"

    # Run the main.py script with the appropriate arguments
    echo "Running main.py for dataset: $dataset_file and FDs: $fd_file"
    python3 "$SCRIPT" --dataset "$dataset_file" --fds "$fd_file" --output "$output_dir" --type "$type"
  else
    echo "Dataset file not found: $dataset_file"
  fi
done