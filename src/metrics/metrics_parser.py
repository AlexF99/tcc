import json


def load_metanome_results(result_file):
    results = []
    with open(result_file, "r") as f:
        for line in f:
            try:
                results.append(json.loads(line))
            except json.JSONDecodeError as erro:
                print(f"[ERROR]: {erro}")
                continue

    return results


def load_fdx_results(result_file):
    results = []
    with open(result_file, "r") as f:
        for line in f:
            results.append(line)

    return results


def metanome_parser(results):
    fds = []
    for fd in results:
        lhs_columns = [
            det["columnIdentifier"] for det in fd["determinant"]["columnIdentifiers"]
        ]
        rhs_column = fd["dependant"]["columnIdentifier"]

        fds.append((lhs_columns, rhs_column))

    return fds


def fdx_parser(results: list[str]):
    fds = []
    for fd in results:
        splitted_fd = fd.split(" -> ")
        lhs_columns = splitted_fd[0].split(",")
        rhs_column = splitted_fd[1]
        fds.append((lhs_columns, rhs_column))

    return fds
