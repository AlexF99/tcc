import time
import json
import adapted_paper_metrics
import parser
import pandas as pd
import os
from datetime import datetime

dataset_csv_file = "/home/lewis/ufpr/tcc/datasets/ncvoter_1001r_19c.csv"
fds_input_file = "/home/lewis/ufpr/tcc/metanome-cli/results/2025-03-14_11-36-24_fds"

current_time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
output_folder = os.path.join("metrics_results", current_time)
os.makedirs(output_folder, exist_ok=True)

fds_csv_file = os.path.join(output_folder, "fds_results.csv")
metrics_csv_file = os.path.join(output_folder, "metrics_results.csv")

metrics = {
    "mu": adapted_paper_metrics.mu,
    # "rfi": adapted_paper_metrics.reliable_fraction_of_information,
}

start_time_file = time.time()
total_time_metrics = {metric_name: 0 for metric_name in metrics}

results = parser.load_results(fds_input_file)
fds = parser.metanome_parser(results)



df = pd.read_csv(dataset_csv_file, header="infer")

print(df.columns)


num_columns = df.shape[1]
# df.columns = [f"column{i+1}" for i in range(num_columns)]

for lhs_columns, rhs_column in fds:

    fd_identifier = f"{lhs_columns}->{rhs_column}"
    
    # print(lhs_columns)
    # print(df.columns)
    
    # exit()
    
    # if not set(lhs_columns).issubset(df.columns) or rhs_column not in df.columns:
    #     print(f"Columns {lhs_columns} or {rhs_column} not found in {dataset_csv_file}")
    #     continue
    
    for metric_name, metric_function in metrics.items():
        start_time = time.time()
        try:
            if not lhs_columns:
                print("LHS está vazio")
                continue
            
            result = metric_function(df, lhs_columns, rhs_column)
            

            # if metric_function in paper_metrics.__dict__.values():
            #     if len(lhs_columns) != 1:
            #         print(f"[WARN] Métrica '{metric_name}' só aceita um argumento em LHS atual: {lhs_columns}. Ignorando esta FD.")
            #         continue
                
            #     lhs_column = lhs_columns[0]
            #     print(f"Calculando {metric_name} para {lhs_column} -> {rhs_column} no arquivo {dataset_csv_file}")
            #     result = metric_function(df, lhs_column, rhs_column) 
            # else:
            #     print(f"Calculando {metric_name} para {lhs_columns} -> {rhs_column} no arquivo {dataset_csv_file}")
            #     result = metric_function(df, lhs_columns, rhs_column)

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
print("PASSSEIII")
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