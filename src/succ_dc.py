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
