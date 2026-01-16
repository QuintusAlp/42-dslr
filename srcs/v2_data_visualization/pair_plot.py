import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from .base_plot import BasePlot

class PairPlot(BasePlot):

    def prepare_data(self, df: pd.DataFrame):
        """Pair plot specific data preparation"""

    def plot(self, df: pd.DataFrame):
        """Pair plot specific plotting"""

def main():
    pair_plot = PairPlot()
    pair_plot.run()
    