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
        return
    
    filename = sys.argv[1]

    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        error("File does not exist.")
    except PermissionError:
        error("File could not be opened.")
    except pd.errors.EmptyDataError:
        error("File is empty.")
    except pd.errors.ParserError:
        error("Invalid CSV format.")
    except OSError as e:
        error(str(e))

    df_numeric = df.select_dtypes(include=["number"])

    print(df_numeric.head())
    print(df_numeric.shape())