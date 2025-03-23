#!/bin/bash

# Define the paths to the JAR files and the datasets directory
METANOME_CLI_JAR="metanome-cli-1.1.0.jar"
PYRO_JAR="../algorithms/pyro-distro-1.0-SNAPSHOT-distro.jar"
HYFD_JAR="../algorithms/HyFD-1.2-SNAPSHOT.jar"
DATASETS_DIR="../datasets"

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
    --algorithm-config maxUccError:0

  # Run the HyFD algorithm
  java -cp "$METANOME_CLI_JAR:$HYFD_JAR" de.metanome.cli.App --algorithm de.metanome.algorithms.hyfd.HyFD \
    --files "$dataset" \
    --file-key INPUT_GENERATOR \
    --separator ","
done