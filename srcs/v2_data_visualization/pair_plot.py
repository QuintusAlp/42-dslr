import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from .base_plot import BasePlot

# Pairplot -> grid (matrix) of N x N graphs

class PairPlot(BasePlot):

    def plot(self, df_filtered, df_numeric, courses):
        """Pair plot specific plotting"""

        # hue = categorical third variable
        sns.pairplot(df_filtered,
                     vars=courses,
                    hue="Hogwarts House", 
                    palette=self.HOUSES_COLORS,
                    corner=True)
        
        self.save_file("pair_plot.png")

def main():
    pair_plot = PairPlot()
    pair_plot.run()


# Answer to pdf question:
#   we want the features for the logreg than can tell us something about the houses:
#       -> clear distinction between the houses
#       -> little overlap
#       -> non redudant, meaning not perfectly correlated with each other
    