import pandas as pd
from sklearn.model_selection import train_test_split

if __name__ == "__main__":
    df = pd.read_csv("/opt/ml/processing/input/sample-data.csv")
    
    # Ensure label is int and in [0,1]
    df["label"] = df["label"].astype(int)
    if not df["label"].isin([0, 1]).all():
        raise ValueError("Labels must be 0 or 1 for binary:logistic objective")
    
    train, val = train_test_split(df, test_size=0.2, random_state=42)
    
    train.to_csv("/opt/ml/processing/output/train/train.csv", index=False, header=False)
    val.to_csv("/opt/ml/processing/output/validation/validation.csv", index=False, header=False)