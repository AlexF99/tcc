import sys

fds_map = {}

length_map = {}

succ_map = {}


for line in sys.stdin:
    if "->" in line:
        mylin = line.split("->")
        key = mylin[0]
        if key not in fds_map:
            fds_map[key] = []
        fds_map[key].append(mylin[1].replace("\n", ""))

min_len = None

for key, value in fds_map.items():
    key_length = len(key.split(","))
    length = key_length + len(value)
    length_map[key] = length
    if (min_len == None or length < min_len) and length > 0:
        min_len = length

for key, value in length_map.items():
    succ_map[key] = min_len / length_map[key]

print(f"found {len(fds_map)} fds")

for key, value in fds_map.items():
    print(key, end=": ")
    for v in value:
        print(v, end=", ")

    print("succinctness: ", end="")
    print(succ_map[key])


