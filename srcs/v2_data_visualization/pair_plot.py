import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from .base_plot import BasePlot

# Pairplot -> grid (matrix) of N x N graphs

class PairPlot(BasePlot):

    def prepare_data(self, df: pd.DataFrame):
        """Pair plot specific data preparation"""

        cols_to_drop = ['Index', 'First Name', 'Last Name', 'Birthday', 'Best Hand']
        df_filtered = df.drop(columns=cols_to_drop, errors='ignore')
        df_filtered = df_filtered[df_filtered['Hogwarts House'].notna()] 
        return (df_filtered)

    def plot(self, df_filtered):
        """Pair plot specific plotting"""

        df_numeric = df_filtered.select_dtypes(include=['number'])
        courses = df_numeric.columns.tolist()

        # hue = categorical third variable
        sns.pairplot(df_filtered,
                     vars=courses,
                    hue="Hogwarts House", 
                    palette=self.HOUSES_COLORS,
                    # height=2.0,
                    # aspect=1.0,
                    corner=True)
        
        SCRIPT_DIR = Path(__file__).resolve().parent
        output_path = SCRIPT_DIR / "pairplot.png"
        plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
        plt.close()

def main():
    pair_plot = PairPlot()
    pair_plot.run()


# Answer to pdf question:
#   we want the features for the logreg than can tell us something about the houses:
#       -> clear distinction between the houses
#       -> little overlap
#       -> non redudant, meaning not perfectly correlated with each other
    