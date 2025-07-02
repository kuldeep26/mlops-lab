import argparse
import pandas as pd
import os
from sklearn.model_selection import train_test_split

def process_data():
    """
    Process and split the input data into training and validation sets
    """
    input_data_path = "/opt/ml/processing/input"
    output_path = "/opt/ml/processing/output"
    
    # Read input data
    input_files = [f for f in os.listdir(input_data_path) if f.endswith('.csv')]
    df = pd.read_csv(os.path.join(input_data_path, input_files[0]))
    
    # Your data preprocessing logic here
    # Example:
    # df = df.dropna()
    # df = pd.get_dummies(df, columns=['categorical_column'])
    
    # Split the data
    train_data, validation_data = train_test_split(df, test_size=0.2, random_state=42)
    
    # Create output directories
    os.makedirs(f"{output_path}/train", exist_ok=True)
    os.makedirs(f"{output_path}/validation", exist_ok=True)
    
    # Save the processed data
    train_data.to_csv(f"{output_path}/train/train.csv", index=False)
    validation_data.to_csv(f"{output_path}/validation/validation.csv", index=False)

if __name__ == "__main__":
    process_data()