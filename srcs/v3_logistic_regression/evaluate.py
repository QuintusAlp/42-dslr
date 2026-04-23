import pandas as pd
import sys
from sklearn.metrics import accuracy_score


def evaluate_predictions(predictions_file, test_file):
    """
    Evaluate classifier accuracy against true labels.
    
    Args:
        predictions_file: Path to houses.csv (predicted labels)
        test_file: Path to dataset_test.csv or ground truth file
    """
    predictions = pd.read_csv(predictions_file)
    test_data = pd.read_csv(test_file)
    
    if 'Hogwarts House' not in test_data.columns or test_data['Hogwarts House'].isna().all():
        print("Error: No true labels found in test file")
        sys.exit(1)
    
    y_true = test_data['Hogwarts House'].values
    y_pred = predictions['Hogwarts House'].values
    
    accuracy = accuracy_score(y_true, y_pred)
    
    print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    return accuracy


def main():
    if len(sys.argv) != 3:
        print("Usage: evaluate.py <houses.csv> <dataset_test.csv>")
        sys.exit(1)
    
    predictions_file = sys.argv[1]
    test_file = sys.argv[2]
    
    evaluate_predictions(predictions_file, test_file)


if __name__ == "__main__":
    main()
