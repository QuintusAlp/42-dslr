# Replicating describe() behavior
#   count, mean, standard deviation, min, Q1, median, Q3, max

import sys 
import pandas as pd
from colorama import Fore, Style, init
from pprint import pprint
from .csv_loader import validate_csv
from .exceptions import FileValidationError, DataProcessingError
from .statistics import compute_stats

# colorama init
init() 

def error(msg):
    print(Fore.RED + "Error: " + Style.RESET_ALL, msg)

def validate_arguments():
    if len(sys.argv) != 2:
        raise FileValidationError("Please submit one (and only one) argument.")
    return (sys.argv[1])

def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    df_numeric = df.select_dtypes(include=["number"]).dropna(axis=1, how="all")
    df_filtered = df_numeric.drop(columns=["Index"], errors='ignore')

    if df_filtered.empty:
        raise DataProcessingError("No numeric columns found in dataset")
    
    return (df_filtered)

def main(bonus: bool = False):
    try:
        filename = validate_arguments()
        df = validate_csv(filename)
        df_filtered = prepare_data(df)

        data = {}
        for col in df_filtered.columns:
            numeric_values = df_filtered[col].dropna().tolist()
            if not numeric_values:
                continue
            stats_dict = compute_stats(numeric_values, bonus=bonus)
            data[col] = stats_dict
        if not data:
            raise DataProcessingError("No valid data to analyze.")

        pprint(data, sort_dicts=False)

    except FileValidationError as e:
        error(str(e))
        sys.exit(1)

    except DataProcessingError as e:
        error(str(e))
        sys.exit(1)

    except Exception as e:
        error(f"Unexpected error: {str(e)}")
        sys.exit(2)

def main_bonus():
    main(bonus=True)

if __name__ == "__main__":
    main()
