import os
import pandas as pd


def get_datasets_info():
    data = []
    datasets_path = "../../../datasets/final"
    if os.path.exists(datasets_path):
        for filename in os.listdir(datasets_path):
            if filename.endswith('.csv'):
                file_path = os.path.join(datasets_path, filename)
                df = pd.read_csv(file_path)
                num_rows = len(df)
                num_columns = len(df.columns)
                data.append([filename.split('.')[0], num_rows, num_columns])

    # Create a DataFrame with dataset information
    datasets_info = pd.DataFrame(data, columns=['dataset', 'num_rows', 'num_columns'])
    return datasets_info

def get_global_df(results_path="../../../experiments/nyc-experiments"):
    # Extract dataset names from the filenames within results_path directory
    datasets = set()
    if os.path.exists(results_path):
        for filename in os.listdir(results_path):
            if filename.endswith('.csv'):
                continue
            parts = filename.split('-')
            if len(parts) >= 2:
                # Extract dataset name (everything after the algorithm name)
                dataset_name = '-'.join(parts[1:])
                datasets.add(dataset_name)
    
    datasets = sorted(list(datasets))
    algorithms = ["fdx", "pyro", "hyfd"]

    fds_results = {}

    for dataset in datasets:
        for algorithm in algorithms:
            folder_name = f"{algorithm}-{dataset}"

            folder_path = os.path.join(results_path, folder_name)
            file_path = os.path.join(folder_path, f"{algorithm}-{dataset}.csv")
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                fds_results[(algorithm, dataset)] = df

    metrics = ["rfi_prime_plus", "mu_plus", "g3_prime"]

    global_df = pd.DataFrame(columns=["algorithm", "dataset", "lhs_size", "lhs_uniqueness"])

    for (algo, dataset), df in fds_results.items():
        if "fd" in df.columns:
            # Create a temporary dataframe with just the metrics that exist in this df
            available_metrics = [m for m in metrics if m in df.columns]
            if not available_metrics:
                continue

            temp_df = df[available_metrics].copy()

            # Calculate LHS size based on 'fd' structure
            temp_df["lhs_size"] = df["fd"].str.split("->").str[0].str.count(",") + 1
            
            # Include fd in the dataframe
            temp_df["fd"] = df["fd"]

            # Add identifying columns
            temp_df["algorithm"] = algo
            temp_df["dataset"] = dataset

            # Calculate LHS uniqueness based on 'fd' structure
            temp_df["lhs_uniqueness"] = df["lhs_uniqueness"]

            # Append to the global DataFrame
            global_df = pd.concat([global_df, temp_df], ignore_index=True)

    return global_df


def get_thresholds_df(results_path="../../../experiments/pyro-thresholds"):
    datasets = set()
    thresholds = set()
    
    if os.path.exists(results_path):
        for folder_name in os.listdir(results_path):
            if os.path.isdir(os.path.join(results_path, folder_name)):
                parts = folder_name.split('-')
                if len(parts) >= 3 and parts[0] == "pyro":
                    dataset = parts[1]
                    threshold = parts[2].replace('_', '.')
                    datasets.add(dataset)
                    thresholds.add(threshold)
    
    datasets = sorted(list(datasets))
    thresholds = sorted(list(thresholds), key=float)

    print(datasets)
    print(thresholds)

    fds_results = {}

    for dataset in datasets:
        for threshold in thresholds:
            # Convert threshold from decimal to folder format (0.05 -> 0_05)
            threshold_folder = threshold.replace('.', '_')
            folder_name = f"pyro-{dataset}-{threshold_folder}"
            
            folder_path = os.path.join(results_path, folder_name)
            runtime_file = os.path.join(folder_path, f"pyro-{dataset}-runtime.csv")
            results_file = os.path.join(folder_path, f"pyro-{dataset}.csv")
            
            if os.path.exists(results_file):
                df = pd.read_csv(results_file)
                fds_results[(threshold, dataset)] = df

    metrics = ["rfi_prime_plus", "mu_plus", "g3_prime"]

    global_df = pd.DataFrame(columns=["threshold", "dataset", "lhs_size", "fd"])

    for (threshold, dataset), df in fds_results.items():
        if "fd" in df.columns:
            # Create a temporary dataframe with just the metrics that exist in this df
            available_metrics = [m for m in metrics if m in df.columns]
            if not available_metrics:
                continue

            temp_df = df[available_metrics].copy()

            # Calculate LHS size based on 'fd' structure
            temp_df["lhs_size"] = df["fd"].str.split("->").str[0].str.count(",") + 1
            temp_df["fd"] = df["fd"]

            # Add identifying columns
            temp_df["threshold"] = threshold
            temp_df["dataset"] = dataset

            # Append to the global DataFrame
            global_df = pd.concat([global_df, temp_df], ignore_index=True)

    return global_df
