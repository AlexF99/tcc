#!/bin/bash

# Directory containing the metrics results
METRICS_DIR="../metrics/metrics_results"

# Iterate through each subdirectory in the metrics directory
for dir in "$METRICS_DIR"/*/; do
    # Check if fds_results.csv exists in the subdirectory
    if [[ -f "${dir}fds_results.csv" ]]; then
        # Define the output file names for each plot type
        BASE_NAME=$(basename "$dir")
        BOX_PLOT_OUTPUT="${dir}boxplot.png"
        CORRELATION_OUTPUT="${dir}correlation.png"
        DENSITY_OUTPUT="${dir}density.png"

        # Run the plot.py script for each type of plot
        python3 plot.py "${dir}fds_results.csv" --colunas mu_plus,rfi_prime_plus,g3_prime --tipo boxplot --saida "$BOX_PLOT_OUTPUT"
        python3 plot.py "${dir}fds_results.csv" --colunas mu_plus,rfi_prime_plus,g3_prime --tipo correlacao --saida "$CORRELATION_OUTPUT"
        python3 plot.py "${dir}fds_results.csv" --colunas mu_plus,rfi_prime_plus,g3_prime --tipo densidade --saida "$DENSITY_OUTPUT"
    fi
done