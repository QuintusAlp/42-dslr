import pandas as pd
import numpy as np
import json
import sys


def sigmoid(z):
    return np.where(
        z >= 0,
        1 / (1 + np.exp(-z)),
        np.exp(z) / (1 + np.exp(z))
    )


def mean(x):
    return x.sum() / x.size


def std(x):
    m = mean(x)
    return np.sqrt(((x - m) ** 2).sum() / x.size)


def normalised_col(x):
    m = mean(x)
    s = std(x)
    if s == 0:
        return x
    return (x - m) / s


def load_models(model_file):
    with open(model_file, 'r') as f:
        return json.load(f)


def prepare_test_data(csv_file):
    data = pd.read_csv(csv_file)
    columns_to_drop = ['Index', 'First Name', 'Last Name', 'Birthday', 'Best Hand']
    data = data.drop(columns=columns_to_drop, errors='ignore')
    return data


def normalize_test_data(data, normalization_params):
    numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
    
    for col in numeric_columns:
        if col in normalization_params:
            m = normalization_params[col]['mean']
            s = normalization_params[col]['std']
            if s == 0:
                data[col] = 0.0
            else:
                data[col] = (data[col] - m) / s
        else:
            data[col] = normalised_col(data[col])


def predict(X, models_dict):
    classifiers = models_dict['classifiers']
    predictions = []
    
    for idx, features in enumerate(X):
        scores = {}
        
        for house, model in classifiers.items():
            theta = np.array(model['theta'])
            b = model['b']
            z = np.dot(features, theta) + b
            prob = sigmoid(z)
            scores[house] = prob
        
        predicted_house = max(scores, key=scores.get)
        predictions.append(predicted_house)
    
    return predictions


def main():
    if len(sys.argv) != 3:
        print("Usage: logreg_predict.py <dataset_test.csv> <models.json>")
        sys.exit(1)
    
    test_file = sys.argv[1]
    model_file = sys.argv[2]
    
    models = load_models(model_file)
    test_data = prepare_test_data(test_file)
    
    numeric_columns = models['classifiers'][list(models['classifiers'].keys())[0]]['features']
    
    median_values = test_data[numeric_columns].median()
    test_data.loc[:, numeric_columns] = test_data[numeric_columns].fillna(median_values)
    test_data.loc[:, numeric_columns] = test_data[numeric_columns].fillna(0.0)
    
    normalize_test_data(test_data, models['normalization'])
    X_normalized = test_data[numeric_columns].values
    
    predictions = predict(X_normalized, models)
    
    result = pd.DataFrame({
        'Index': range(len(predictions)),
        'Hogwarts House': predictions
    })
    
    result.to_csv('houses.csv', index=False)
    print("✓ Predictions saved to houses.csv")


if __name__ == "__main__":
    main()
