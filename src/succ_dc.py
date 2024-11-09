import sys


# candidates 161

predicounts = {}
minCount = None

key = 0

for line in sys.stdin:
    numPredicates = line.count("PredicateVariable")
    if numPredicates == 1:
        print(key)
    if minCount == None or (minCount != None and numPredicates < minCount):
        minCount = numPredicates

    predicounts[key] = numPredicates
    key = key + 1

print(f"minCount: {minCount}")

for key, value in sorted(predicounts.items(), key=lambda x: x[1]):
    print(f"succintness of dc {key}: {minCount / value}")

# smallest
{
    "type": "DenialConstraint",
    "predicates": [
        {
            "type": "de.metanome.algorithm_integration.PredicateVariable",
            "column1": {
                "tableIdentifier": "ncvoter_1001r_19c.csv",
                "columnIdentifier": '"state"',
            },
            "index1": 0,
            "op": "UNEQUAL",
            "column2": {
                "tableIdentifier": "ncvoter_1001r_19c.csv",
                "columnIdentifier": '"state"',
            },
            "index2": 1,
        }
    ],
}


# largest
{
    "type": "DenialConstraint",
    "predicates": [
        {
            "type": "de.metanome.algorithm_integration.PredicateVariable",
            "column1": {
                "tableIdentifier": "ncvoter_1001r_19c.csv",
                "columnIdentifier": '"zip_code"',
            },
            "index1": 0,
            "op": "UNEQUAL",
            "column2": {
                "tableIdentifier": "ncvoter_1001r_19c.csv",
                "columnIdentifier": '"zip_code"',
            },
            "index2": 1,
        },
        {
            "type": "de.metanome.algorithm_integration.PredicateVariable",
            "column1": {
                "tableIdentifier": "ncvoter_1001r_19c.csv",
                "columnIdentifier": '"race"',
            },
            "index1": 0,
            "op": "EQUAL",
            "column2": {
                "tableIdentifier": "ncvoter_1001r_19c.csv",
                "columnIdentifier": '"race"',
            },
            "index2": 1,
        },
        {
            "type": "de.metanome.algorithm_integration.PredicateVariable",
            "column1": {
                "tableIdentifier": "ncvoter_1001r_19c.csv",
                "columnIdentifier": '"name_suffix"',
            },
            "index1": 0,
            "op": "EQUAL",
            "column2": {
                "tableIdentifier": "ncvoter_1001r_19c.csv",
                "columnIdentifier": '"name_suffix"',
            },
            "index2": 1,
        },
        {
            "type": "de.metanome.algorithm_integration.PredicateVariable",
            "column1": {
                "tableIdentifier": "ncvoter_1001r_19c.csv",
                "columnIdentifier": '"download_month"',
            },
            "index1": 0,
            "op": "UNEQUAL",
            "column2": {
                "tableIdentifier": "ncvoter_1001r_19c.csv",
                "columnIdentifier": '"download_month"',
            },
            "index2": 1,
        },
        {
            "type": "de.metanome.algorithm_integration.PredicateVariable",
            "column1": {
                "tableIdentifier": "ncvoter_1001r_19c.csv",
                "columnIdentifier": '"full_phone_num"',
            },
            "index1": 0,
            "op": "EQUAL",
            "column2": {
                "tableIdentifier": "ncvoter_1001r_19c.csv",
                "columnIdentifier": '"full_phone_num"',
            },
            "index2": 1,
        },
        {
            "type": "de.metanome.algorithm_integration.PredicateVariable",
            "column1": {
                "tableIdentifier": "ncvoter_1001r_19c.csv",
                "columnIdentifier": '"city"',
            },
            "index1": 0,
            "op": "EQUAL",
            "column2": {
                "tableIdentifier": "ncvoter_1001r_19c.csv",
                "columnIdentifier": '"city"',
            },
            "index2": 1,
        },
        {
            "type": "de.metanome.algorithm_integration.PredicateVariable",
            "column1": {
                "tableIdentifier": "ncvoter_1001r_19c.csv",
                "columnIdentifier": '"gender"',
            },
            "index1": 0,
            "op": "UNEQUAL",
            "column2": {
                "tableIdentifier": "ncvoter_1001r_19c.csv",
                "columnIdentifier": '"gender"',
            },
            "index2": 1,
        },
        {
            "type": "de.metanome.algorithm_integration.PredicateVariable",
            "column1": {
                "tableIdentifier": "ncvoter_1001r_19c.csv",
                "columnIdentifier": '"age"',
            },
            "index1": 0,
            "op": "EQUAL",
            "column2": {
                "tableIdentifier": "ncvoter_1001r_19c.csv",
                "columnIdentifier": '"age"',
            },
            "index2": 1,
        },
        {
            "type": "de.metanome.algorithm_integration.PredicateVariable",
            "column1": {
                "tableIdentifier": "ncvoter_1001r_19c.csv",
                "columnIdentifier": '"name_prefix"',
            },
            "index1": 0,
            "op": "EQUAL",
            "column2": {
                "tableIdentifier": "ncvoter_1001r_19c.csv",
                "columnIdentifier": '"name_prefix"',
            },
            "index2": 1,
        },
        {
            "type": "de.metanome.algorithm_integration.PredicateVariable",
            "column1": {
                "tableIdentifier": "ncvoter_1001r_19c.csv",
                "columnIdentifier": '"birth_place"',
            },
            "index1": 0,
            "op": "UNEQUAL",
            "column2": {
                "tableIdentifier": "ncvoter_1001r_19c.csv",
                "columnIdentifier": '"birth_place"',
            },
            "index2": 1,
        },
    ],
}
# nomes iguais, gen dif

# t1 t2 => 0E
# t1 t3 => 1E
# t1 t4 => 1E
# t1 t5 => 0E
# t1 t6 => 1E
# t1 t7 => 1E
# t1 t8 => 1E

# t2 t3 => 1E
# t2 t4 => 1E
# t2 t5 => 0E
# t2 t6 => 0E
# t2 t7 => 1E
# t2 t8 => 1E

# t3 t4 => 0E
# t3 t5 => 1E
# t3 t6 => 1E
# t3 t7 => 0E
# t3 t8 => 0E

# t4 t5 => 1E
# t4 t6 => 1E
# t4 t7 => 0E
# t4 t8 => 0E

# t5 t6 => 0E
# t5 t7 => 1E
# t5 t8 => 1E

# t6 t7 => 1E
# t6 t8 => 1E

# t7 t8 => 0E

# 11 OE w(0)=1/2
# 17 1E w(1)=1
# (5.5+17)/11+17 