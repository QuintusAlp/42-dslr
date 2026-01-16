import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import f_oneway
from .base_plot import BasePlot

# scatter plots are used to show the relationship between 2 numeric vars:
#   ex: study hours VS test scores
# here we use a categorical third variable for the houses
# only render scatter plots where houses dont't overlap -> heterogenous

# can transform bday in age and then do mean of all scores and do age vs notes

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

        cols_to_drop = ['Index', 'First Name', 'Last Name', 'Birthday', 'Best Hand']
        df_filtered = df.drop(columns=cols_to_drop, errors='ignore')
        df_filtered = df_filtered[df_filtered['Hogwarts House'].notna()] #removes rows with missing house
        return (df_filtered)
        

    def plot(self, df_filtered):
        """"Scatter plot specific plotting"""

        df_numeric = df_filtered.select_dtypes(include=['number'])
        courses = df_numeric.columns.tolist()
        n_courses = len(courses)
        
        print(n_courses)

        # number of plots = nbr of possible combinations
        # (n * (n-1)) / 2

        for i in range(n_courses):
            for j in range(i + 1, n_courses):
                x_feature = courses[i]
                y_feature = courses[j]
                
                plt.figure()

                for house in self.HOUSES:
                    mask = df_filtered['Hogwarts House'] == house
                    mask &= df_filtered[x_feature].notna() & df_filtered[y_feature].notna()
                    house_x_data = df_filtered.loc[mask, x_feature]
                    house_y_data = df_filtered.loc[mask, y_feature]
                    plt.scatter(house_x_data, house_y_data,
                                color=self.HOUSES_COLORS[house],
                                alpha=0.6,
                                label=house)
                
                plt.title(x_feature + " VS " + y_feature)
                plt.xlabel(x_feature)
                plt.ylabel(y_feature)
                plt.legend()

                plt.tight_layout()
                plt.show()


def main():
    scatter_plot = ScatterPlot()
    scatter_plot.run()
    