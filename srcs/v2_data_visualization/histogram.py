import pandas as pd
import matplotlib.pyplot as plt
from .base_plot import BasePlot

class HistogramPlot(BasePlot):

    def prepare_data(self, df: pd.DataFrame):
        """"Histogram-specific data preparation"""
        cols_to_drop = ['Index', 'First Name', 'Last Name', 'Birthday', 'Best Hand']
        df_filtered = df.drop(columns=cols_to_drop, errors='ignore')
        df_filtered = df_filtered[df_filtered['Hogwarts House'].notna()] # keep only rows where a specific col is not missing
        return (df_filtered)

    def plot(self, df_filtered):
        """"Histogram-specific plotting"""
        houses = df_filtered['Hogwarts House'].unique()
        course_cols = df_filtered.select_dtypes(include=['number']).columns.tolist()

        n_courses = len(course_cols)
        n_cols = 4
        n_rows = (n_courses + n_cols - 1) // n_cols

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 5 * n_rows))
        axes = axes.flatten()

        for i, course in enumerate(course_cols):
            ax = axes[i]

            for house in houses:
                house_data = df_filtered[df_filtered['Hogwarts House'] == house][course].dropna()
                ax.hist(house_data, bins=20, alpha=0.5, label=house)
            
            ax.set_title(course)
            ax.set_xlabel('Score')
            ax.set_ylabel('Frequency')
            ax.legend()
        
        for j in range(i + 1, len(axes)):
            axes[j].set_visible(False)
        
        plt.tight_layout()
        plt.show()

def main():
    histogram = HistogramPlot()
    histogram.run()
