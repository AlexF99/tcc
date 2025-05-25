#!/bin/bash

# Define the paths to the JAR files and the datasets directory
METANOME_CLI_JAR="metanome-cli-1.1.0.jar"
PYRO_JAR="./algorithms/pyro-distro-1.0-SNAPSHOT-distro.jar"
HYFD_JAR="./algorithms/HyFD-1.2-SNAPSHOT.jar"
DATASETS_DIR="../datasets/experiments"


java -cp "$METANOME_CLI_JAR:$PYRO_JAR" de.metanome.cli.App

echo "Pyro algorithm completed"