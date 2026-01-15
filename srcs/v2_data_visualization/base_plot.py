import sys
import pandas as pd
from abc import ABC, abstractmethod
from srcs.v1_data_analysis.describe import validate_arguments, error
from srcs.v1_data_analysis.csv_loader import validate_csv
from srcs.v1_data_analysis.exceptions import FileValidationError, DataProcessingError

class BasePlot(ABC):
    """Base class for all visualizations plots"""

    def run(self):
        """Main execution flow, shared across all plots"""
        try: 
            filename = validate_arguments()
            df = validate_csv(filename)
            df_filtered = self.prepare_data(df)
            self.plot(df_filtered)

        except FileValidationError as e:
            error(str(e))
            sys.exit(1)
        except DataProcessingError as e:
            error(str(e))
            sys.exit(1)
        except Exception as e:
            error(f"Unexpected error: {str(e)}")
            sys.exit(2)
    
    @abstractmethod
    def prepare_data(self, df: pd.DataFrame):
        """Each plot implements its own data preparation"""
        pass

    @abstractmethod
    def plot(self, df: pd.DataFrame):
        """Each plot implements its own plotting logic"""
        pass