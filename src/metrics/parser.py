import json
def load_results(result_file):
    results = []
    with open(result_file, 'r') as f:
        for line in f:
            try:
                results.append(json.loads(line))
            except json.JSONDecodeError as erro:
                print(f"[ERROR]: {erro}")
                continue
            
    return results

def metanome_parser(results):
    fds = []
    for fd in results:
        lhs_columns = [det['columnIdentifier'] for det in fd["determinant"]["columnIdentifiers"]]
        rhs_column = fd['dependant']['columnIdentifier']
        
        fds.append((lhs_columns, rhs_column))
        
    return fds
        
