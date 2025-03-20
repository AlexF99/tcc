import math
from typing import Any, List
import numpy as np
import pandas as pd
import math
from subprocess import PIPE


def mu(df: pd.DataFrame, lhs: List[Any], rhs: Any) -> float:
    """This measure is mu as defined by [Piatetsky-Shapiro & Matheus, 1993], adapted for lists of columns."""
    pdepXY = pdep(df, lhs, rhs)  # Usa a função pdep adaptada
    pdepY = pdep_self(df, rhs)   # Usa a função pdep_self que não precisa ser adaptada
    r_size = df.shape[0] 
    
    domX_size = df.loc[:, lhs].drop_duplicates().shape[0]
    
    # print((r_size - domX_size))
    
    return 1.0 - ((1 - pdepXY) / (1 - pdepY)) * ((r_size - 1) / (r_size - domX_size))



def pdep_self(df: pd.DataFrame, y: Any) -> float:
    """This measure is pdep(Y) as defined by [Piatetsky-Shapiro & Matheus, 1993]."""
    return (df.loc[:, y].value_counts() / df.shape[0]).pow(2).sum()


def pdep(df: pd.DataFrame, lhs: List[Any], rhs: Any) -> float:
    """This measure is pdep as defined by [Piatetsky-Shapiro & Matheus, 1993], adapted for lists of columns."""
    
    combined_columns = lhs + [rhs]
    
    xy_counts = df.loc[:, combined_columns].value_counts().reset_index()
    xy_counts.columns = combined_columns + ["xy_count"]
    
    x_counts = df.loc[:, lhs].value_counts().reset_index()
    x_counts.columns = lhs + ["x_count"]
    
    counts = xy_counts.merge(x_counts, on=lhs)
    
    return (1 / df.shape[0]) * (counts["xy_count"].pow(2) / counts["x_count"]).sum()



def reliable_fraction_of_information(df: pd.DataFrame, lhs: List[Any], rhs: Any) -> float:
    """This measures reliable fraction of information as defined by [Mandros, Boley & Vreeken, 2017], adapted for lists of columns."""
    n = df.shape[0] 

    x_counts = df.loc[:, lhs].value_counts()
    y_counts = df.loc[:, rhs].value_counts()
    
    m = 0.0
    
    for _, a in x_counts.items():
        comb_n_a = math.comb(n, a)
        
        for _, b in y_counts.items():
            k0 = max(0, a + b - n)
            p0 = math.comb(b, k0) * math.comb(n - b, a - k0) / comb_n_a
            
            if k0 != 0:
                m += p0 * (k0 / n) * math.log((k0 * n) / (a * b), 2)

            for k1 in range(k0 + 1, min(a, b) + 1):
                p0 = p0 * (((a - k0) * (b - k0)) / (k1 * (n - a - b + k1)))
                m += p0 * (k1 / n) * math.log((k1 * n) / (a * b), 2)
                k0 = k1

    fi_value = fraction_of_information(df, lhs, rhs)
    
    bias_estimator = m / (-1.0 * ((y_counts / n) * np.log2(y_counts / n)).sum())
    
    return fi_value - bias_estimator

def fraction_of_information(df: pd.DataFrame, lhs: List[Any], rhs: Any) -> float:
    """This measures matches the function FD as defined by [Cavallo & Pittarelli, 1987], adapted for lists of columns."""
    
    r_size = df.shape[0]
    
    # Calcula a entropia de Shannon de Y
    y_counts = df.loc[:, rhs].value_counts().reset_index()
    y_counts.columns = [rhs, "y_count"]
    shannonY = (
        -1.0
        * ((y_counts["y_count"] / r_size) * np.log2(y_counts["y_count"] / r_size)).sum()
    )
    
    combined_columns = lhs + [rhs]
    
    xy_counts = df.loc[:, combined_columns].value_counts().reset_index()
    xy_counts.columns = combined_columns + ["xy_count"]
    
    x_counts = df.loc[:, lhs].value_counts().reset_index()
    x_counts.columns = lhs + ["x_count"]
    
    counts = xy_counts.merge(x_counts, on=lhs)
    
    shannonYX = (
        -1.0
        * (
            (counts["xy_count"] / r_size)
            * np.log2((counts["xy_count"] / r_size) / (counts["x_count"] / r_size))
        ).sum()
    )
    
    return (shannonY - shannonYX) / shannonY

