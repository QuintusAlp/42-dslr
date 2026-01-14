# Replicating describe() behavior
#   count, mean, standard deviation, min, Q1, median, Q3, max

import pandas as pd
import sys 
from colorama import Fore, Style, init

# colorama init
init() 

# store everyhting in a dict 

# def count():
#     # number of elements of the var

# def mean():
#     # sum all values / count

# def standard_deviation():
#     # sqrt(sum(x - mean)^2) / (n - 1)

# def min_max():
#     # iterate through all values and store -> return a dict

# def q1_q2_q3():
#     # sort and then find values at positions



def error(msg):
    print(Fore.RED + "Error: " + Style.RESET_ALL, msg)

def main():
    if len(sys.argv) != 2:
        print(Fore.RED + "Error:" + Style.RESET_ALL + " Please submit one (and only one) argument.")
        sys.exit(1)
    
    filename = sys.argv[1]

    if not filename.lower().endswith('.csv'):
        error("File needs a .csv extension")
        sys.exit(1)

    # print("CHANGES")

    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        error("File does not exist.")
        sys.exit(1)
    except PermissionError:
        error("File could not be opened.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        error("File is empty.")
        sys.exit(1)
    except pd.errors.ParserError:
        error("Invalid CSV format.")
        sys.exit(1)
    except OSError as e:
        error(str(e))
        sys.exit(1)

    df_numeric = df.select_dtypes(include=["number"]).dropna(axis=1, how="all")

    print(df_numeric.head())
    print(df_numeric.shape)