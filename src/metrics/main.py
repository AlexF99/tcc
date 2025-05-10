import time
import adapted_paper_metrics
import metrics_parser
import pandas as pd
import os
from datetime import datetime
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description="Run metrics on datasets")
parser.add_argument(
    "--dataset", type=str, required=True, help="Path to the dataset CSV file"
)
parser.add_argument("--fds", type=str, required=True, help="Path to the FDs input file")
parser.add_argument("--type", type=str, required=True, help="metanome or fdx")
parser.add_argument(
    "--header", type=str, required=True, help="input data has header as first row"
)
parser.add_argument("--output", type=str, required=False, help="Output's dir name")

args = parser.parse_args()

dataset_csv_file = args.dataset
fds_input_file = args.fds
hasHeader = args.header == "True"
source_type = args.type

dir_name = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
if args.output:
    dir_name = args.output
output_folder = os.path.join("metrics_results", dir_name)
os.makedirs(output_folder, exist_ok=True)

fds_csv_file = os.path.join(output_folder, "fds_results.csv")
metrics_csv_file = os.path.join(output_folder, "metrics_results.csv")

metrics = {
    "mu_plus": adapted_paper_metrics.mu_plus,
    "rfi_prime_plus": adapted_paper_metrics.reliable_fraction_of_information_prime_plus,
    "g3": adapted_paper_metrics.g3,
    "g3_prime": adapted_paper_metrics.g3_prime,
}

start_time_file = time.time()
total_time_metrics = {metric_name: 0 for metric_name in metrics}

results = (
    metrics_parser.load_metanome_results(fds_input_file)
    if source_type == "metanome"
    else metrics_parser.load_fdx_results(fds_input_file)
)
fds = (
    metrics_parser.metanome_parser(results)
    if source_type == "metanome"
    else metrics_parser.fdx_parser(results)
)

if hasHeader:
    df = pd.read_csv(dataset_csv_file, header=0)  # Use first row as column names
else:
    df = pd.read_csv(dataset_csv_file, header=None)  # No header, treat all as data
    num_columns = df.shape[1]
    df.columns = [f"column{i+1}" for i in range(num_columns)]

num_columns = df.shape[1]

fd_ids = []
metrics_results = {key: [] for key in metrics}

for lhs_columns, rhs_column in fds:

    lhs_columns = [col.strip() for col in lhs_columns]

    if not lhs_columns:
        print(f"LHS está vazio: {lhs_columns} -> {rhs_column}")
        continue

    rhs_column = rhs_column.strip()
    fd_identifier = f"{lhs_columns}->{rhs_column}"

    fd_ids.append(fd_identifier)

    if not set(lhs_columns).issubset(df.columns) or rhs_column not in df.columns:
        print(f"Columns {lhs_columns} or {rhs_column} not found in {dataset_csv_file}")
        continue

    for metric_name, metric_function in metrics.items():
        start_time = time.time()
        try:
            # print(
            #     f"Calculando {metric_name} para {lhs_columns} -> {rhs_column} no arquivo {dataset_csv_file}"
            # )
            result = metric_function(df, lhs_columns, rhs_column)

            metrics_results[metric_name].append(result)

            elapsed_time = time.time() - start_time
            total_time_metrics[metric_name] += elapsed_time

        except Exception as e:
            print(
                f"[ERROR] {metric_name} for {lhs_columns} and {rhs_column} in {dataset_csv_file}: {e}"
            )
            continue

mobj = {k: [v["result"] for v in values] for k, values in metrics_results.items()}

# Only include is_key and fi in final results if they exist in the values
isKey = {}
rfi = {}

for k, values in metrics_results.items():
    # Check if at least one value has the 'is_key' attribute
    if any("is_key" in v for v in values):
        isKey[f"{k}_is_key"] = [v.get("is_key", "-") for v in values]

    # Check if at least one value has the 'fi' attribute
    if any("rfi" in v for v in values):
        rfi[f"{k}_rfi"] = [v.get("rfi", "-") for v in values]

final_df = pd.DataFrame({"fd": fd_ids, **mobj, **isKey, **rfi})

final_df.to_csv(fds_csv_file, mode="w", header=True, index=False)

total_time_file = time.time() - start_time_file
for metric_name, total_time in total_time_metrics.items():
    pd.DataFrame(
        [
            {
                "file": dataset_csv_file,
                "metric": metric_name,
                "metric_time": total_time,
                "num_columns": num_columns,
                "num_fds": len(results),
            }
        ]
    ).to_csv(metrics_csv_file, mode="a", header=False, index=False)

pd.DataFrame(
    [
        {
            "file": dataset_csv_file,
            "metric": "total_file_time",
            "metric_time": total_time_file,
            "num_columns": num_columns,
            "num_fds": len(results),
        }
    ]
).to_csv(metrics_csv_file, mode="a", header=False, index=False)
