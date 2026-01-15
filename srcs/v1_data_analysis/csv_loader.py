import pandas as pd
from .exceptions import FileValidationError

def validate_csv(filename: str) -> pd.DataFrame:
    if not filename.lower().endswith('.csv'):
        raise FileValidationError("File needs a .csv extension.")

    try:
        df = pd.read_csv(filename)
        return (df)
    except FileNotFoundError:
        raise FileValidationError("File does not exist.")
    except PermissionError:
        raise FileValidationError("File could not be opened.")
    except pd.errors.EmptyDataError:
        raise FileValidationError("File is empty.")
    except pd.errors.ParserError:
        raise FileValidationError("Invalid CSV format.")
    except OSError as e:
        raise FileValidationError(str(e))
