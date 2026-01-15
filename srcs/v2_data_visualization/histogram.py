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
        
        course_cols = df_filtered.select_dtypes(include=['number']).columns.tolist()

        n_courses = len(course_cols)
        n_cols = 4
        n_rows = (n_courses + n_cols - 1) // n_cols

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 3 * n_rows))
        axes = axes.flatten()

        for i, course in enumerate(course_cols):
            ax = axes[i]
            
            house_datasets = []
            labels = []
            colors = []
            
            for house in self.HOUSES:
                house_data = df_filtered[df_filtered['Hogwarts House'] == house][course].dropna()
                if len(house_data) > 0:
                    house_datasets.append(house_data.values)
                    labels.append(house)
                    colors.append(self.HOUSES_COLORS[house])
            
            if house_datasets:
                ax.hist(house_datasets,
                        bins=20,
                        alpha=0.6,
                        color=colors,
                        label=labels,
                        edgecolor='black',
                        linewidth=0.5)
            
            ax.set_title(f'{course}', fontsize=10, fontweight='bold')
            ax.set_xlabel('Score', fontsize=8)
            ax.set_ylabel('Count', fontsize=8)
            ax.legend(fontsize=7, loc='best')
            ax.grid(True, alpha=0.3)
        
        for j in range(i + 1, len(axes)):
            axes[j].set_visible(False)
        
        plt.tight_layout()
        plt.show()

def main():
    histogram = HistogramPlot()
    histogram.run()
