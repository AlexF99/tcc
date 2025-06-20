import time
import adapted_paper_metrics
import metrics_parser
import pandas as pd
import os
from datetime import datetime

def run_metrics(dataset_csv_file, fds_input_file, source_type, hasHeader, output_dir_name=None):
    """
    Run metrics on datasets
    
    Args:
        dataset_csv_file (str): Path to the dataset CSV file
        fds_input_file (str): Path to the FDs input file
        source_type (str): "metanome" or "fdx"
        hasHeader (bool): Whether input data has header as first row
        output_dir_name (str, optional): Output directory name
    
    Returns:
        dict: Results containing output paths and metrics
    """
    # Extract algorithm from FDS filename if metanome, otherwise from output folder or default
    if source_type == "metanome":
        # For metanome, FDS file follows pattern: algorithmname_dataset_fds
        fds_filename = os.path.basename(fds_input_file)
        if "_fds" in fds_filename:
            # Split by underscore and take the first part as algorithm name
            algorithm = fds_filename.split("_")[0]
        else:
            algorithm = "unknown"
    else:
        algorithm = "fdx"

    dataset = os.path.basename(dataset_csv_file).split(".csv")[0]

    dir_name = datetime.now().strftime("%d-%m-%Y-%H-%M-%S-") + algorithm + "-" + dataset
    if output_dir_name:
        dir_name = output_dir_name.split(".csv")[0]
    output_folder = os.path.join("metrics_results", dir_name)

    os.makedirs(output_folder, exist_ok=True)

    fds_csv_file = os.path.join(output_folder, f"{algorithm}-{dataset}.csv")
    metrics_csv_file = os.path.join(output_folder, f"{algorithm}-{dataset}-runtime.csv")

    metrics = {
        "mu_plus": adapted_paper_metrics.mu_plus,
        "rfi_prime_plus": adapted_paper_metrics.reliable_fraction_of_information_prime_plus,
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
    lhs_size = {}
    lhs_uniqueness = {}

    for k, values in metrics_results.items():
        # Check if at least one value has the 'is_key' attribute
        if any("is_key" in v for v in values):
            isKey[f"is_key"] = [v.get("is_key", "-") for v in values]
        
        if any("lhs_size" in v for v in values):
            lhs_size[f"lhs_size"] = [v.get("lhs_size", "-") for v in values]
        
        if any("lhs_uniqueness" in v for v in values):
            lhs_uniqueness[f"lhs_uniqueness"] = [v.get("lhs_uniqueness", "-") for v in values]

    final_df = pd.DataFrame({"dataset": dataset, "algorithm": algorithm, "fd": fd_ids, **mobj, **isKey, **lhs_size, **lhs_uniqueness})

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
    
    return {
        "fds_csv_file": fds_csv_file,
        "metrics_csv_file": metrics_csv_file,
        "output_folder": output_folder,
        "total_time": total_time_file,
        "num_fds": len(results)
    }

if __name__ == "__main__":
    import argparse
    
    # Set up argument Parser for backward compatibility
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
    
    run_metrics(
        dataset_csv_file=args.dataset,
        fds_input_file=args.fds,
        source_type=args.type,
        hasHeader=args.header == "True",
        output_dir_name=args.output
    )
