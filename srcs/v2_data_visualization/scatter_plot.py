import pandas as pd
import matplotlib.pyplot as plt
from .base_plot import BasePlot

class ScatterPlot(BasePlot):

    def prepare_data(self, df: pd.DataFrame):
        """"Scatter plot specific data preparation"""

    def plot(self, df: pd.DataFrame):
        """"Scatter plot specific plotting"""

def main():
    scatter_plot = ScatterPlot()
    scatter_plot.run()
    