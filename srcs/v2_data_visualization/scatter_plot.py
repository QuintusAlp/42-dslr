import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import f_oneway
from .base_plot import BasePlot

# only render scatter plots where houses dont't overlap -> heterogenous

class ScatterPlot(BasePlot):

    # using ANOVA (= analysis of variance method)
    def determine_homogeneity(self, df: pd.DataFrame, course):
        houses_scores = []

        for house in self.HOUSES:
            scores = df[df['Hogwarts House'] == house][course].dropna()
            houses_scores.append(scores)
        
        f_stat, p_value = f_oneway(*houses_scores)

        # if p > 0.05 -> cannot reject null -> means are similar -> homogeneous
        # if p < 0.05 -> reject null -> means differ -> heterogeneous
        return (p_value)

    def prepare_data(self, df: pd.DataFrame):
        """"Scatter plot specific data preparation"""

    def plot(self, df: pd.DataFrame):
        """"Scatter plot specific plotting"""

def main():
    scatter_plot = ScatterPlot()
    scatter_plot.run()
    