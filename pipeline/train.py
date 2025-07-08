import argparse
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--training', type=str, default=None)
    parser.add_argument('--testing', type=str, default=None)
    args = parser.parse_args()
    
    # Load the data
    train_data = pd.read_csv(f"{args.training}/train.csv")
    test_data = pd.read_csv(f"{args.testing}/test.csv")
    
    # Separate features and target
    X_train = train_data.drop('target', axis=1)
    y_train = train_data['target']
    
    # Train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Save the model
    joblib.dump(model, '/opt/ml/model/model.joblib')

if __name__ == "__main__":
    main()