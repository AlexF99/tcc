import sys
import pandas as pd

dc = {"type":"DenialConstraint","predicates":[{"type":"de.metanome.algorithm_integration.PredicateVariable","column1":{"tableIdentifier":"ncvoter_1001r_19c.csv","columnIdentifier":"\"race\""},"index1":0,"op":"UNEQUAL","column2":{"tableIdentifier":"ncvoter_1001r_19c.csv","columnIdentifier":"\"race\""},"index2":1},{"type":"de.metanome.algorithm_integration.PredicateVariable","column1":{"tableIdentifier":"ncvoter_1001r_19c.csv","columnIdentifier":"\"full_phone_num\""},"index1":0,"op":"EQUAL","column2":{"tableIdentifier":"ncvoter_1001r_19c.csv","columnIdentifier":"\"full_phone_num\""},"index2":1},{"type":"de.metanome.algorithm_integration.PredicateVariable","column1":{"tableIdentifier":"ncvoter_1001r_19c.csv","columnIdentifier":"\"ethnic\""},"index1":0,"op":"UNEQUAL","column2":{"tableIdentifier":"ncvoter_1001r_19c.csv","columnIdentifier":"\"ethnic\""},"index2":1},{"type":"de.metanome.algorithm_integration.PredicateVariable","column1":{"tableIdentifier":"ncvoter_1001r_19c.csv","columnIdentifier":"\"city\""},"index1":0,"op":"EQUAL","column2":{"tableIdentifier":"ncvoter_1001r_19c.csv","columnIdentifier":"\"city\""},"index2":1},{"type":"de.metanome.algorithm_integration.PredicateVariable","column1":{"tableIdentifier":"ncvoter_1001r_19c.csv","columnIdentifier":"\"gender\""},"index1":0,"op":"UNEQUAL","column2":{"tableIdentifier":"ncvoter_1001r_19c.csv","columnIdentifier":"\"gender\""},"index2":1},{"type":"de.metanome.algorithm_integration.PredicateVariable","column1":{"tableIdentifier":"ncvoter_1001r_19c.csv","columnIdentifier":"\"birth_place\""},"index1":0,"op":"EQUAL","column2":{"tableIdentifier":"ncvoter_1001r_19c.csv","columnIdentifier":"\"birth_place\""},"index2":1}]},

voters = pd.read_csv("../datasets/ncvoter_1001r_19c.csv")
ke = {}

def equal(p1,p2):
    return p1 == p2

def unequal(p1,p2):
    return p1 != p2

def lt(p1,p2):
    return p1 < p2

def lte(p1,p2):
    return p1 <= p2

def gt(p1,p2):
    return p1 > p2

def gte(p1,p2):
    return p1 >= p2


ops = {"EQUAL": equal, "UNEQUAL": unequal, "LT": lt, "LTE": lte, "GT": gt, "GTE": gte}

#   print(dc[0]['predicates'])

for i in range(len(voters)):
    currentTuple = voters.iloc[i]
    currentValue = 0 
    for j in range(i+1, len(voters)):
        for predicate in dc[0]['predicates']:
            p1 = voters.loc[i, predicate['column1']['columnIdentifier'].split("\"")[1]]
            p2 = voters.loc[j, predicate['column2']['columnIdentifier'].split("\"")[1]]

            if ops[predicate['op']](p1, p2):
                currentValue += 1
        
        if currentValue in ke:
            ke[currentValue] += 1
        else:
            ke[currentValue] = 1 


print(ke)
