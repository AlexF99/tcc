#!/bin/bash

# Define the paths to the directories
RESULTS_DIR="../../metanome-cli/results"
DATASETS_DIR="../../datasets"
SCRIPT="main.py"

# metrics for metanome results
for fd_file in "$RESULTS_DIR"/*; do
  # Extract the algorithm and dataset names from the FD filename
  filename=$(basename -- "$fd_file")

  if [[ "$filename" == pyro-threshold-* ]]; then
    # Handle threshold-x.xx-dataset structure
    algorithm=$filename
    dataset="${filename#*-}"  # Remove 'pyro-threshold-' prefix
    dataset="${dataset#*-}"  # Remove 'x.xx-' prefix
    dataset="${dataset#*-}"  # Remove 'x.xx-' prefix
    echo $dataset
  else
    # Default structure
    algorithm="${filename%%-*}"
    dataset="${filename#*-}"
  fi

  type="metanome"
  dataset_file="$DATASETS_DIR/experiments/$dataset"

  # Check if the dataset file exists
  if [ -f "$dataset_file" ]; then
    output_dir="${algorithm}-${dataset}"

    echo "Running main.py for dataset: $dataset_file and FDs: $fd_file"
    python3 "$SCRIPT" --dataset "$dataset_file" --fds "$fd_file" --output "$output_dir" --type "$type" --header "True"
  else
    echo "Dataset file not found: $dataset_file"
  fi
done

# metrics for fdx results
for fd_file in ../../profiler/results/*; do
  algorithm="fdx"
  dataset_name="$(basename ${fd_file%_by_col.txt})"
  type="fdx"
  dataset_file="$DATASETS_DIR/experiments/$dataset_name.csv"
  # Check if the dataset file exists
  if [ -f "$dataset_file" ]; then
    output_dir="${algorithm}-${dataset_name}"
    echo "Running main.py for dataset: $dataset_file and FDs: $fd_file"
    python3 "$SCRIPT" --dataset "$dataset_file" --fds "$fd_file" --output "$output_dir" --type "$type" --header "True"
  else
    echo "Dataset file not found: $dataset_file"
  fi
done
