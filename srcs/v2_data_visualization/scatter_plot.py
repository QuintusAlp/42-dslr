import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import f_oneway
from .base_plot import BasePlot

# scatter plots are used to show the relationship between 2 vars:
#   ex: study hours VS test scores
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

        df_numeric = df.select_dtypes(include=["number"]).dropna(axis=1, how="all")
        df_filtered = df_numeric.drop(columns=["Index"], errors='ignore')
        
        

    def plot(self, df: pd.DataFrame):
        """"Scatter plot specific plotting"""

        x1 = np.array([]) # making is an np array because it permits more things with the data and matplotlib is optimized for numpy
        y1 = np.arrau([])

        x2 = np.array([])
        y2 = np.array([])

        # x = vars list of the x-axis
        plt.scatter(x, y, color="", alpha = 0.5,
                    )

        plt.title("Graph title")
        plt.xlabel("x vars name")
        plt.ylabel("y vars name")

        plt.show()

def main():
    scatter_plot = ScatterPlot()
    scatter_plot.run()
    