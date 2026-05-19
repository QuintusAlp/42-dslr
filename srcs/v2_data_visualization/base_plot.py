import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from srcs.v1_data_analysis.describe import validate_arguments, error
from srcs.v1_data_analysis.csv_loader import validate_csv
from srcs.v1_data_analysis.exceptions import FileValidationError, DataProcessingError

class BasePlot(ABC):
    """Base class for all visualizations plots"""

    HOUSES = ['Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin']
    HOUSES_COLORS = {
        "Gryffindor": "red",
        "Hufflepuff": "yellow",
        "Ravenclaw": "blue",
        "Slytherin": "green"
    }

    def run(self):
        """Main execution flow, shared across all plots"""
        try: 
            filename = validate_arguments()
            df = validate_csv(filename)
            df_filtered, df_numeric, courses = self.prepare_data(df)
            self.plot(df_filtered, df_numeric, courses)

        except FileValidationError as e:
            error(str(e))
            sys.exit(1)
        except DataProcessingError as e:
            error(str(e))
            sys.exit(1)
        except Exception as e:
            error(f"Unexpected error: {str(e)}")
            sys.exit(2)
    
    def prepare_data(self, df: pd.DataFrame):
        """Data preparation common for each plot"""
        if 'Hogwarts House' not in df.columns:
            raise DataProcessingError("Dataset must contain 'Hogwarts House' column for visualization. Use dataset_train.csv instead of dataset_test.csv")
        
        cols_to_drop = ['Index', 'First Name', 'Last Name', 'Birthday', 'Best Hand']
        df_filtered = df.drop(columns=cols_to_drop, errors='ignore')
        df_filtered = df_filtered[df_filtered['Hogwarts House'].notna()] # keep only rows where a specific col is not missing
        
        if df_filtered.empty:
            raise DataProcessingError("No rows with valid house assignments found in dataset")
        
        df_numeric = df_filtered.select_dtypes(include=['number'])
        courses = df_numeric.columns.tolist()
        return (df_filtered, df_numeric, courses)

    def save_file(self, name: str):
        """Saving the resulting plot image in a plot folder"""
        # Creating plots dir if it doesnt exist
        script_dir = os.path.dirname(os.path.abspath(__file__))
        plots_folder = os.path.join(script_dir, "plots")
        os.makedirs(plots_folder, exist_ok=True)

        output_path = os.path.join(plots_folder, name)
        plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
        plt.close()

    @abstractmethod
    def plot(self, df_filtered, df_numeric, courses):
        """Each plot implements its own plotting logic"""
        pass