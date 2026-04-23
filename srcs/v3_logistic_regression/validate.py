import pandas as pd
import numpy as np
import json
import sys
from sklearn.metrics import accuracy_score, classification_report


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


def prepare_data(csv_file):
    data = pd.read_csv(csv_file)
    
    columns_to_drop = ['Index', 'First Name', 'Last Name', 'Birthday', 'Best Hand']
    clean_data = data.drop(columns=columns_to_drop, errors='ignore').copy()
    
    if 'Hogwarts House' not in clean_data.columns:
        raise ValueError("Missing target column: 'Hogwarts House'")
    
    clean_data = clean_data[clean_data['Hogwarts House'].notna()].copy()
    
    numeric_columns = clean_data.select_dtypes(include=[np.number]).columns.tolist()
    if not numeric_columns:
        raise ValueError("No numeric features available after preprocessing")
    
    median_values = clean_data[numeric_columns].median()
    clean_data.loc[:, numeric_columns] = clean_data[numeric_columns].fillna(median_values)
    clean_data.loc[:, numeric_columns] = clean_data[numeric_columns].fillna(0.0)
    clean_data = clean_data.drop_duplicates(ignore_index=True)
    
    return clean_data


def normalize_data(data):
    numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_columns:
        raise ValueError("No numeric features to normalize")
    
    for col in numeric_columns:
        data[col] = normalised_col(data[col])


def normalize_with_params(data, normalization_params):
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
    
    for features in X:
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
        print("Usage: validate.py <dataset_train.csv> <models.json>")
        sys.exit(1)
    
    train_file = sys.argv[1]
    model_file = sys.argv[2]
    
    models = load_models(model_file)
    data = prepare_data(train_file)
    
    y_true = data['Hogwarts House'].values
    
    numeric_columns = models['classifiers'][list(models['classifiers'].keys())[0]]['features']
    
    normalize_with_params(data, models['normalization'])
    X_normalized = data[numeric_columns].values
    
    y_pred = predict(X_normalized, models)
    
    accuracy = accuracy_score(y_true, y_pred)
    
    print(f"\n{'='*60}")
    print(f"Training Set Validation (with stored normalization params)")
    print(f"{'='*60}")
    print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"Samples: {len(y_true)}")
    print(f"{'='*60}\n")
    
    print("Classification Report:")
    print(classification_report(y_true, y_pred))


if __name__ == "__main__":
    main()
