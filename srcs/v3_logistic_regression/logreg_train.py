import pandas as pd
import numpy as np
import json

def sigmoid(z):
    return np.where(
        z >= 0,
        1 / (1 + np.exp(-z)),
        np.exp(z) / (1 + np.exp(z))
    )

def logistic_regression(X, theta, b):
    z = (X @ theta) + b
    return sigmoid(z)

def gradient_descent(X, y, alpha=0.01, num_iter=10000, tol=1e-7):
    n_samples, n_features = X.shape

    theta = np.zeros(n_features)
    b = 0.0

    for i in range(num_iter):
        y_hat = logistic_regression(X, theta, b)
        
        error = y_hat - y
        
        epsilon = 1e-15
        y_hat_clipped = np.clip(y_hat, epsilon, 1 - epsilon)
        loss = -np.mean(y * np.log(y_hat_clipped) + (1 - y) * np.log(1 - y_hat_clipped))
        
        if (i + 1) % 1000 == 0:
            print(f"  Iteration {i+1}/{num_iter}, Loss: {loss:.6f}")
        
        grad_theta = X.T @ error / n_samples
        grad_b = error.sum() / n_samples

        theta -= alpha * grad_theta
        b -= alpha * grad_b

        if np.linalg.norm(grad_theta) < tol:
            print(f"  Converged at iteration {i+1}, Loss: {loss:.6f}")
            break

    return theta, b

    # print(theta, b)
    return theta, b



def prepare_data():
    data = pd.read_csv("./datasets/dataset_train.csv")
    
    columns_to_drop = ['Index', 'First Name', 'Last Name', 'Birthday', 'Best Hand', 'Defense']
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

def train(house, data):
    numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
    if not numeric_columns:
        raise ValueError(f"No numeric features available for training {house}")
    
    X = data[numeric_columns].values
    y = (data['Hogwarts House'] == house).astype(int).values
    
    theta, b = gradient_descent(X, y)
    
    return {
        'house': house,
        'theta': theta,
        'b': b,
        'features': numeric_columns
    }

def main():
    houses = ['Ravenclaw', 'Slytherin', 'Gryffindor', 'Hufflepuff']
    data = prepare_data()
    
    numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
    norm_params = {}
    for col in numeric_columns:
        norm_params[col] = {
            'mean': float(data[col].mean()),
            'std': float(data[col].std())
        }
    
    normalize_data(data)
    
    models = {
        'normalization': norm_params,
        'classifiers': {}
    }
    
    for house in houses:
        model = train(house, data)
        models['classifiers'][house] = {
            'theta': model['theta'].tolist(),
            'b': float(model['b']),
            'features': model['features']
        }
        print(f"✓ Trained {house}")
    
    with open('./models.json', 'w') as f:
        json.dump(models, f, indent=2)
    
    print("✓ Models saved to models.json")

if __name__ == "__main__":
    main()
