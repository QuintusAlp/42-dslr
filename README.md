# 42-DSLR: Hogwarts House Classification

A data science project that classifies students into Hogwarts houses (Gryffindor, Slytherin, Ravenclaw, Hufflepuff) based on their academic performance using logistic regression. Made in collaboration with Quentin Alpesse (@QuintusAlp).

## Project Description

This project implements a complete machine learning pipeline consisting of three phases:

1. **Data Analysis** - Computes descriptive statistics for numeric features
2. **Data Visualization** - Explores feature distributions and relationships
3. **Logistic Regression Classification** - Trains and uses a multi-class classification model to predict house assignments

The dataset contains 1600+ student records with 13 course scores. A trained logistic regression model (`models.json`) is used to classify new students.

## Requirements

Before running this project, ensure you have:

- **Python 3.13 or higher** (required by the project configuration)
- **Poetry** installed (for dependency management)
- A CSV file with student data in the format: Index, Hogwarts House, and numeric course columns

## Theory

### Poetry: Dependency Management

Poetry is a Python package manager that handles project dependencies and virtual environments. Unlike pip, Poetry:

- Uses `pyproject.toml` to define project configuration and dependencies
- Locks exact versions in `poetry.lock` to ensure reproducible builds
- Manages isolated virtual environments (`.venv`) per Python version
- Simplifies running scripts with `poetry run <command>`

When you switch Python versions with `poetry env use`, you get a separate virtual environment, requiring `poetry install` to reinstall dependencies.

### Logistic Regression with Gradient Descent

Logistic regression is a classification algorithm that predicts discrete classes (houses) using the sigmoid function. The model works by:

1. **Feature Normalization** - Scales input values (mean=0, std=1) so features have equal importance
2. **Linear Combination** - Computes z = X·θ + b, where θ (theta) are learned weights and b is bias
3. **Sigmoid Function** - Maps z to probability [0,1]: σ(z) = 1/(1+e^(-z))
4. **Multi-class Prediction** - Trains one classifier per house, predicts the house with highest probability

The model learns θ and b using gradient descent optimization during training, minimizing classification error.

### Data Visualization: Insights and Interpretation

Data visualizations are critical for understanding feature distributions and relationships. They reveal patterns that inform feature selection and model performance expectations.

#### Histogram

A histogram displays the frequency distribution of a single feature across all four houses using overlaid bars with different colors.

**Data Science Insights:**
- **Feature Separability** - If houses show distinct, non-overlapping distributions, the feature is highly predictive. Overlapping distributions indicate weak discriminative power.
- **Outliers and Skewness** - Identifies extreme values and asymmetric distributions that may require special handling.
- **Multimodality** - Multiple peaks within a house distribution suggest subgroups or data quality issues.
- **Feature Selection** - Features with clear house separation are candidates for inclusion in the model; highly overlapped features contribute less to classification.

Example: If Arithmancy scores for Ravenclaw cluster at 70000+ while other houses are below 40000, Arithmancy is valuable for classification.

#### Pair Plot

A pair plot visualizes pairwise relationships between all numeric features, creating a matrix where each cell shows a scatter plot of two features, typically colored by house.

**Data Science Insights:**
- **Multivariate Correlation** - Reveals how features interact together, not just individually. Linear relationships visible as clear trends indicate strong feature combinations.
- **Class Clustering** - If houses form distinct clusters in 2D feature space, the feature pair has good discriminative power.
- **Feature Redundancy** - If two features show identical or nearly identical relationships with house, they may be redundant (high multicollinearity), limiting model improvement.
- **Decision Boundaries** - Visualizes the space the logistic regression model must separate; scattered, overlapped clusters indicate harder classification problems.

Example: A pair plot showing Transfiguration vs Ancient Runes might reveal that Slytherin students cluster in the upper-left while Gryffindors cluster in the lower-right, making this pair highly predictive.

#### Scatter Plot

A scatter plot shows the relationship between two features with points colored by house, useful for examining specific feature pairs of interest.

**Data Science Insights:**
- **Linear Separability** - Determines if logistic regression (a linear classifier) can effectively separate classes. Linearly separable classes yield high accuracy.
- **Feature Correlation** - Strong upward or downward trends between features indicate correlation. High correlation with low predictive value suggests feature redundancy.
- **Outlier Detection** - Isolated points reveal anomalies or data entry errors that may skew model training.
- **Class Imbalance Visibility** - If one house has far fewer points than others, the dataset is imbalanced and may require resampling techniques.

Example: A scatter plot of Defense Against Dark Arts vs Potions might show Gryffindors in the high-defense, low-potions region, enabling the model to learn this boundary.

**Interpretation for Model Building:**
Together, these visualizations guide feature engineering and hyperparameter tuning. High-quality separability in plots predicts high model accuracy. Dense overlaps suggest the need for feature transformation, polynomial features, or acceptance of lower baseline accuracy.

## Setup

1. Install dependencies:
```bash
poetry install
```

2. If needed, switch to Python 3.13:
```bash
poetry env use python3.13
poetry install
```

3. Verify installation:
```bash
poetry run describe datasets/dataset_train.csv
```

## Usage

### Available Commands

Run any command with: `poetry run <command> [arguments]`

**Data Analysis:**
```bash
poetry run describe datasets/dataset_train.csv
poetry run describe_bonus datasets/dataset_train.csv
```
Outputs summary statistics (count, mean, std dev, min, Q1, median, Q3, max) for each numeric column.

**Data Visualization:**
```bash
poetry run histogram
poetry run pair_plot
poetry run scatter_plot
```
Generates PNG files showing feature distributions and relationships. Plots are saved to `srcs/v2_data_visualization/plots/`.

**Classification:**
```bash
poetry run logreg_predict datasets/dataset_test.csv models.json
```
Predicts house assignments for test data and saves results to `houses.csv`.

**Cleanup:**
```bash
poetry run clean
```
Removes generated plot files and prediction output.

## Project Structure

```
42-dslr/
├── datasets/              # Training/test data
├── srcs/
│   ├── v1_data_analysis/  # Statistical analysis
│   ├── v2_data_visualization/  # Plot generation
│   ├── v3_logistic_regression/  # Classification model
│   └── scripts/           # Utility scripts
├── houses.csv             # Generated predictions
├── models.json            # Trained classifier parameters
├── pyproject.toml         # Project configuration
└── poetry.lock            # Locked dependency versions
```

## Dependency Management

Add a dependency:
```bash
poetry add <package>
```

Remove a dependency:
```bash
poetry remove <package>
```

Current dependencies: numpy, pandas, colorama, matplotlib, seaborn, scikit-learn