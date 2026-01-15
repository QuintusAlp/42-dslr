# Replicating describe() behavior
#   count, mean, standard deviation, min, Q1, median, Q3, max

import pandas as pd
import sys 
import math
from colorama import Fore, Style, init
from pprint import pprint

# colorama init
init() 

def compute_count(values: list) -> int:
    return (len(values))

def compute_mean(values: list, count: int) -> float:
    return (sum(values) / count)

# sqrt(sum(x - mean)^2) / (n - 1)
def compute_standard_deviation(values: list, mean: float, count: int) -> float:
    if (count < 2):
        return (0.0)
        
    variance = sum((x - mean) ** 2 for x in values) / (count - 1)
    return (math.sqrt(variance))

def compute_extrema(values: list) -> dict[str, float]:
    return {
        "min": values[0],
        "max": values[len(values) - 1]
    }

def compute_percentiles(values: list, count: int) -> dict[str, float]:
    def get_percentile(p):
        index = p / 100 * (count - 1)
        lower = int(index) # if float values take the index just below the result
        if (lower + 1 < count):
            upper = lower + 1
        else:
            upper = lower
        fraction = index - lower # how far is the index value from the closest smallest int value
        return (values[lower] + fraction * (values[upper] - values[lower])) # interpolating
            
    return {
        "q1": get_percentile(25),
        "q2": get_percentile(50),
        "q3": get_percentile(75)
    }

def compute_stats(values: list) -> dict[str, float]:
    count = compute_count(values)
    mean = compute_mean(values, count)
    sorted_values = sorted(values)
    min_max = compute_extrema(sorted_values)
    percentiles = compute_percentiles(sorted_values, count)

    return {
        "count": count,
        "mean": mean,
        "std": compute_standard_deviation(values, mean, count),
        "min": min_max["min"],
        "25%": percentiles["q1"],
        "50%": percentiles["q2"],
        "75%": percentiles["q3"],
        "max": min_max["max"],
    }

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
    df_filtered = df_numeric.drop(columns=["Index"])

    # print(df_numeric.head())
    # print(df_numeric.shape)

    data = {}

    for col in df_filtered.columns:
        numeric_values = df_filtered[col].dropna().tolist()
        stats_dict = compute_stats(numeric_values)
        data[col] = stats_dict
    
    pprint(data, sort_dicts=False)

    # print()
    # print("***** DESCRIBE OUTPUT *****")
    # describe_stats = df_filtered.describe()
    # print(describe_stats)