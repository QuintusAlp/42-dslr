import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import f_oneway
from itertools import combinations, islice
from .base_plot import BasePlot

# scatter plots are used to show the relationship between 2 numeric vars:
#   ex: study hours VS test scores
# here we use a categorical third variable for the houses
# only render scatter plots where houses dont't overlap -> heterogenous

class ScatterPlot(BasePlot):

    def prepare_data(self, df: pd.DataFrame):
        """"Scatter plot specific data preparation"""

        cols_to_drop = ['Index', 'First Name', 'Last Name', 'Birthday', 'Best Hand']
        df_filtered = df.drop(columns=cols_to_drop, errors='ignore')
        df_filtered = df_filtered[df_filtered['Hogwarts House'].notna()] #removes rows with missing house
        return (df_filtered)
        
    def make_batches(self, items, size):
        it = iter(items)
        while True:
            batch = list(islice(it, size))
            if not batch:
                break
            yield batch #like a return but resume to where it was when function is called again -> pauses fct

    def plot(self, df_filtered):
        """"Scatter plot specific plotting"""

        df_numeric = df_filtered.select_dtypes(include=['number'])
        courses = df_numeric.columns.tolist()
        n_courses = len(courses)
        
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
            fig, axes = plt.subplots(3, 4, figsize=(12, 9))
            axes = axes.flatten()

            # i is the # of pairs (= 12)
            for i, pair in enumerate(batch):
                for house in self.HOUSES:
                    ax = axes[i]
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
                    
                    ax.set_title(x_feature + " VS " + y_feature)
                    ax.set_xlabel(x_feature)
                    ax.set_ylabel(y_feature)

            # Hiding empty axes if nbr of plots in the fig / nbr of plots per fig
            for j in range(len(batch), len(axes)):
                axes[j].set_visible(False)

            plt.tight_layout()
            plt.show()


def main():
    scatter_plot = ScatterPlot()
    scatter_plot.run()
    