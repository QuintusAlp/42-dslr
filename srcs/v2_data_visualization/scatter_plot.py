import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations, islice
from .base_plot import BasePlot

# scatter plots are used to show the relationship between 2 numeric vars:
#   ex: study hours VS test scores
# here we use a categorical third variable for the houses
# only render scatter plots where houses dont't overlap -> heterogenous

class ScatterPlot(BasePlot):
        
    def make_batches(self, items, size):
        batches = []

        for i in range(0, len(items), size):
            batches.append(items[i:i + size])
        
        return (batches)

    def plot(self, df_filtered, df_numeric, courses):
        """Scatter plot specific plotting"""

        plots_per_figure = 12 

        # Extracting every possible course combinations        
        # number of plots = nbr of possible combinations
        # (n * (n-1)) / 2
        pairs = list(combinations(courses, 2))
        pairs_batches = self.make_batches(pairs, plots_per_figure)

        for batch_idx, batch in enumerate(pairs_batches):
            # fig = the entire figure ; ax = array that holds each individual subplot 
            fig, axes = plt.subplots(3, 4, figsize=(14, 10))
            axes = axes.flatten()
            
            # i is the # of pairs (= 12)
            for i, pair in enumerate(batch):
                ax = axes[i]
                x_feature = pair[0]
                y_feature = pair[1]

                for house in self.HOUSES:
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

            self.save_file(f"scatter_plot{batch_idx + 1}.png")


def main():
    scatter_plot = ScatterPlot()
    scatter_plot.run()
    