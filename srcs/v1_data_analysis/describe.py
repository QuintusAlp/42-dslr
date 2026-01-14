import pandas as pd
import sys 
from colorama import Fore, Style, init

# colorama init
init() 

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

    df_numeric = df.select_dtypes(include=["number"])

    print(df_numeric.head())
    print(df_numeric.shape)