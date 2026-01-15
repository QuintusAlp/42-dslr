import pandas as pd
import matplotlib.pyplot as plt
from .base_plot import BasePlot

# only render scatter plots where houses dont't overlap -> heterogenous

class ScatterPlot(BasePlot):

    # using ANOVA (= analysis of variance method)
    def determine_homogeneity(df: pd.DataFrame, course):
        houses_scores = []

        for house in self.houses:

    def prepare_data(self, df: pd.DataFrame):
        """"Scatter plot specific data preparation"""

    def plot(self, df: pd.DataFrame):
        """"Scatter plot specific plotting"""

def main():
    scatter_plot = ScatterPlot()
    scatter_plot.run()
    