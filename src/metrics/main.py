import time
import json
import adapted_paper_metrics
import metrics_parser
import pandas as pd
import os
from datetime import datetime
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description="Run metrics on datasets")
parser.add_argument("--dataset", type=str, required=True, help="Path to the dataset CSV file")
parser.add_argument("--fds", type=str, required=True, help="Path to the FDs input file")
parser.add_argument("--output", type=str, required=False, help="Output's dir name")

args = parser.parse_args()

print(args.dataset, args.fds)
dataset_csv_file = args.dataset
fds_input_file = args.fds

dir_name = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
if (args.output):
    dir_name = args.output
output_folder = os.path.join("metrics_results", dir_name)
os.makedirs(output_folder, exist_ok=True)

fds_csv_file = os.path.join(output_folder, "fds_results.csv")
metrics_csv_file = os.path.join(output_folder, "metrics_results.csv")

metrics = {
    "mu": adapted_paper_metrics.mu,
    "rfi": adapted_paper_metrics.reliable_fraction_of_information,
}

start_time_file = time.time()
total_time_metrics = {metric_name: 0 for metric_name in metrics}

results = metrics_parser.load_results(fds_input_file)
fds = metrics_parser.metanome_parser(results)

df = pd.read_csv(dataset_csv_file, header="infer")

num_columns = df.shape[1]
df.columns = [f"column{i+1}" for i in range(num_columns)]

for lhs_columns, rhs_column in fds:
    fd_identifier = f"{lhs_columns}->{rhs_column}"
    
    if not set(lhs_columns).issubset(df.columns) or rhs_column not in df.columns:
        print(f"Columns {lhs_columns} or {rhs_column} not found in {dataset_csv_file}")
        continue

    for metric_name, metric_function in metrics.items():
        start_time = time.time()
        try:
            if not lhs_columns:
                print("LHS está vazio")
                continue            

            print(f"Calculando {metric_name} para {lhs_columns} -> {rhs_column} no arquivo {dataset_csv_file}")
            result = metric_function(df, lhs_columns, rhs_column)

            elapsed_time = time.time() - start_time
            total_time_metrics[metric_name] += elapsed_time
            
            pd.DataFrame([{
                "file": dataset_csv_file,
                "fd": fd_identifier,
                "metric": metric_name,
                "metric_result_fd": result,
                "metric_time_fd": elapsed_time
            }]).to_csv(fds_csv_file, mode='a', header=False, index=False)
        
        except Exception as e:
            print(f"[ERROR] {metric_name} for {lhs_columns} and {rhs_column} in {dataset_csv_file}: {e}")
            continue

total_time_file = time.time() - start_time_file
for metric_name, total_time in total_time_metrics.items():
    pd.DataFrame([{
        "file": dataset_csv_file,
        "metric": metric_name,
        "metric_time": total_time,
        "num_columns": num_columns,
        "num_fds": len(results)
    }]).to_csv(metrics_csv_file, mode='a', header=False, index=False)

pd.DataFrame([{
    "file": dataset_csv_file,
    "metric": "total_file_time",
    "metric_time": total_time_file,
    "num_columns": num_columns,
    "num_fds": len(results)
}]).to_csv(metrics_csv_file, mode='a', header=False, index=False)