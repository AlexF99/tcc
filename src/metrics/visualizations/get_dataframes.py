import os
import pandas as pd


def get_global_df(results_path="../../../experiments/12-05-2025"):
    algorithms = ["fdx", "pyro"]
    datasets = [
        "abalone",
        "adult",
        "bridges",
        "echocardiogram",
        "iris",
        "letter",
        "ncvoter",
    ]

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

    global_df = pd.DataFrame(columns=["algorithm", "dataset", "lhs_size"])

    for (algo, dataset), df in fds_results.items():
        if "fd" in df.columns:
            # Create a temporary dataframe with just the metrics that exist in this df
            available_metrics = [m for m in metrics if m in df.columns]
            if not available_metrics:
                continue

            temp_df = df[available_metrics].copy()

            # Calculate LHS size based on 'fd' structure
            temp_df["lhs_size"] = df["fd"].str.split("->").str[0].str.count(",") + 1

            # Add identifying columns
            temp_df["algorithm"] = algo
            temp_df["dataset"] = dataset

            # Append to the global DataFrame
            global_df = pd.concat([global_df, temp_df], ignore_index=True)

    return global_df


def get_thresholds_df(results_path="../../../experiments/pyro-thresholds"):
    thresholds = ["0.1", "0.01", "0.05", "0.15"]
    datasets = [
        "abalone",
        "adult",
        "bridges",
        "echocardiogram",
        "iris",
        "letter",
        "ncvoter",
    ]

    fds_results = {}

    for dataset in datasets:
        for threshold in thresholds:
            folder_name = f"pyro-threshold-{threshold}-{dataset}"

            folder_path = os.path.join(results_path, folder_name)
            file_path = os.path.join(folder_path, f"pyro-threshold.csv")

            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                fds_results[(threshold, dataset)] = df

    metrics = ["rfi_prime_plus", "mu_plus", "g3_prime"]

    global_df = pd.DataFrame(columns=["threshold", "dataset", "lhs_size"])

    for (threshold, dataset), df in fds_results.items():
        if "fd" in df.columns:
            # Create a temporary dataframe with just the metrics that exist in this df
            available_metrics = [m for m in metrics if m in df.columns]
            if not available_metrics:
                continue

            temp_df = df[available_metrics].copy()

            # Calculate LHS size based on 'fd' structure
            temp_df["lhs_size"] = df["fd"].str.split("->").str[0].str.count(",") + 1

            # Add identifying columns
            temp_df["threshold"] = threshold
            temp_df["dataset"] = dataset

            # Append to the global DataFrame
            global_df = pd.concat([global_df, temp_df], ignore_index=True)

    return global_df
