import pandas as pd
from sklearn.model_selection import train_test_split

if __name__ == "__main__":
    df = pd.read_csv("/opt/ml/processing/input/sample-data.csv")
    train, val = train_test_split(df, test_size=0.2)
    
    train.to_csv("/opt/ml/processing/output/train/train.csv", index=False)
    val.to_csv("/opt/ml/processing/output/validation/validation.csv", index=False)