import pandas as pd
import matplotlib.pyplot as plt
from .base_plot import BasePlot

class HistogramPlot(BasePlot):

    def plot(self, df_filtered, df_numeric, courses):
        """"Histogram-specific plotting"""
        
        n_courses = len(courses)
        n_cols = 4
        n_rows = (n_courses + n_cols - 1) // n_cols

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 3 * n_rows))
        axes = axes.flatten()

        for i, course in enumerate(courses):
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
        
        self.save_file("histogram.png")

def main():
    histogram = HistogramPlot()
    histogram.run()
