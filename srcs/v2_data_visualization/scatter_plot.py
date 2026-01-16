import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations, islice
from .base_plot import BasePlot

# scatter plots are used to show the relationship between 2 numeric vars:
#   ex: study hours VS test scores
# here we use a categorical third variable for the houses
# only render scatter plots where houses dont't overlap -> heterogenous

class ScatterPlot(BasePlot):

    def prepare_data(self, df: pd.DataFrame):
        """Scatter plot specific data preparation"""

        cols_to_drop = ['Index', 'First Name', 'Last Name', 'Birthday', 'Best Hand']
        df_filtered = df.drop(columns=cols_to_drop, errors='ignore')
        df_filtered = df_filtered[df_filtered['Hogwarts House'].notna()] #removes rows with missing house
        return (df_filtered)
        
    def make_batches(self, items, size):
        it = iter(items)
        batches = []
        
        while True:
            batch = list(islice(it, size))
            if not batch:
                break
            batches.append(batch)

        return (batches)

    def plot(self, df_filtered):
        """Scatter plot specific plotting"""

        df_numeric = df_filtered.select_dtypes(include=['number'])
        courses = df_numeric.columns.tolist()
        n_courses = len(courses)
        
        figures = []

        # number of plots = nbr of possible combinations
        # (n * (n-1)) / 2
        n_plots = (n_courses * (n_courses - 1)) / 2
        plots_per_figure = 12 
        n_figures = math.ceil(n_plots / plots_per_figure)

        # Extracting every possible course combinations        
        pairs = list(combinations(courses, 2))
        pairs_batches = list(self.make_batches(pairs, plots_per_figure))

        for batch in pairs_batches:
            # fig = the entire figure ; ax = array that holds each individual subplot 
            fig, axes = plt.subplots(3, 4, figsize=(14, 10))
            axes = axes.flatten()

            # i is the # of pairs (= 12)
            for i, pair in enumerate(batch):
                ax = axes[i]
                for house in self.HOUSES:
                    x_feature = pair[0]
                    y_feature = pair[1]

                    mask = df_filtered['Hogwarts House'] == house
                    mask &= df_filtered[x_feature].notna() & df_filtered[y_feature].notna()
                    house_x_data = df_filtered.loc[mask, x_feature]
                    house_y_data = df_filtered.loc[mask, y_feature]

                    ax.scatter(house_x_data, house_y_data,
                                color=self.HOUSES_COLORS[house],
                                alpha=0.6,
                                label=house)
                    
                    ax.set_title(x_feature + " VS " + y_feature, fontsize=10)
                    ax.set_xlabel(x_feature)
                    ax.set_ylabel(y_feature)
                    # Reducing the size of the values of the graduated axis
                    ax.tick_params(axis='both', which='major', labelsize=8)

            # Hiding empty axes if nbr of plots in the fig / nbr of plots per fig
            for j in range(len(batch), len(axes)):
                axes[j].set_visible(False)

            # Adding one legend per figure
            handles, labels = axes[0].get_legend_handles_labels()
            fig.legend(handles, labels,
                       loc='upper center',
                       ncol=len(self.HOUSES),
                       fontsize=10)

            plt.tight_layout()
            # Leaving space for legend
            plt.subplots_adjust(top=0.93)
            figures.append(fig)

        plt.show(block=True)


def main():
    scatter_plot = ScatterPlot()
    scatter_plot.run()
    