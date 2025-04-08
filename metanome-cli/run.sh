#!/bin/bash

# Define the paths to the JAR files and the datasets directory
METANOME_CLI_JAR="metanome-cli-1.1.0.jar"
PYRO_JAR="../algorithms/pyro-distro-1.0-SNAPSHOT-distro.jar"
HYFD_JAR="../algorithms/HyFD-1.2-SNAPSHOT.jar"
DATASETS_DIR="../datasets"
RESULTS_DIR="results"

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
    --header \
    --algorithm-config maxUccError:0

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
