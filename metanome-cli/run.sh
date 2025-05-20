#!/bin/bash

# Define the paths to the JAR files and the datasets directory
METANOME_CLI_JAR="metanome-cli-1.1.0.jar"
PYRO_JAR="./algorithms/pyro-distro-1.0-SNAPSHOT-distro.jar"
HYFD_JAR="./algorithms/HyFD-1.2-SNAPSHOT.jar"
DATASETS_DIR="../datasets/experiments"
RESULTS_DIR="results"

# Check if no flag is passed
if [ -z "$1" ]; then
  echo "Executing default Pyro and HyFD algorithms..."

  # Loop through each CSV file in the datasets directory
  for dataset in "$DATASETS_DIR"/*.csv; do
    echo "Processing dataset: $dataset"

    # Run the Pyro algorithm
    java -cp "$METANOME_CLI_JAR:$PYRO_JAR" de.metanome.cli.App --algorithm de.hpi.isg.pyro.algorithms.Pyro \
      --files "$dataset" \
      --file-key inputFile \
      --separator "," \
      --algorithm-config isFindKeys:false \
      --algorithm-config isFindFds:true \
      --header 

    LATEST_FILE=$(ls -t "$RESULTS_DIR"/ | head -n1)
    mv "$RESULTS_DIR/$LATEST_FILE" "$RESULTS_DIR/pyro-$(basename "$dataset")"

    # Run the HyFD algorithm
    java -cp "$METANOME_CLI_JAR:$HYFD_JAR" de.metanome.cli.App --algorithm de.metanome.algorithms.hyfd.HyFD \
      --files "$dataset" \
      --file-key INPUT_GENERATOR \
      --header \
      --separator ","

    LATEST_FILE=$(ls -t "$RESULTS_DIR"/ | head -n1)
    mv "$RESULTS_DIR/$LATEST_FILE" "$RESULTS_DIR/hyfd-$(basename "$dataset")"
  done
fi

# Check if the pyro-threshold flag is enabled
if [ "$1" == "pyro-threshold" ]; then
  echo "Executing Pyro algorithm with threshold parameters for multiple values..."

  # Loop through each CSV file in the datasets directory
  for dataset in "$DATASETS_DIR"/*.csv; do
    echo "Processing dataset with threshold: $dataset"

    # Loop through multiple values for maxUccError and errorDev
    for value in 0.01 0.05 0.1 0.15; do
      echo "Running Pyro with maxUccError=$value and errorDev=$value"

      # Run the Pyro algorithm with threshold parameters
      java -cp "$METANOME_CLI_JAR:$PYRO_JAR" de.metanome.cli.App --algorithm de.hpi.isg.pyro.algorithms.Pyro \
        --files "$dataset" \
        --file-key inputFile \
        --separator "," \
        --algorithm-config isFindKeys:false \
        --algorithm-config isFindFds:true \
        --algorithm-config maxUccError:$value \
        --algorithm-config errorDev:$value \
        --header 

      LATEST_FILE=$(ls -t "$RESULTS_DIR"/ | head -n1)
      mv "$RESULTS_DIR/$LATEST_FILE" "$RESULTS_DIR/pyro-threshold-$value-$(basename "$dataset")"
    done
  done
fi
