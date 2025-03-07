import sys

filepath = sys.argv[1]
output = sys.argv[2]

print(sys.argv)

def translate(content):
    values = None

    if "," in content:
        keys = content.split(",")

        values = []
        for key in keys:
            values.append(ids[int(key)])
            
        values.sort()
        
        values_string = ""
        for value in values:
            if values_string == "":
                values_string = value
            else:
                values_string += f",{value}"
        
        values = values_string
    else:
        if content != "":
            values = ids[int(content)]
            
    return values


ids = {}
column_section = False
results_section = False
data = []
with open(filepath, "r") as file:
    for line in file:
        if "# COLUMN" in line:
            column_section = True
            continue

        if "# RESULTS" in line:
            column_section = False
            results_section = True
            continue
        
        if (column_section):
            content = line.split("\t")
            value = content[0].replace("1.","")
            key = int(content[1].replace("\n",""))
            
            ids.setdefault(key, value)

        if (results_section):
            content = line.split("->")

            lhs = translate(content[0])
            rhs = translate(content[1])

            data.append(f"{lhs} -> {rhs}")

data.sort()
for item in data:
    print(item)
    
with open(output, "+w") as file:
    for item in data:
        file.write(item + "\n")