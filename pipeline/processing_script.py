import pandas as pd
from sklearn.model_selection import train_test_split

if __name__ == "__main__":
    df = pd.read_csv("/opt/ml/processing/input/sample-data.csv")

    # Ensure label is int
    df["label"] = df["label"].astype(int)

    # Make sure label is the first column
    cols = ["label"] + [col for col in df.columns if col != "label"]
    df = df[cols]

    train, val = train_test_split(df, test_size=0.2, random_state=42)

    # Drop empty rows just in case
    train = train.dropna()
    val = val.dropna()

    # Save without header / index
    train.to_csv("/opt/ml/processing/output/train/train.csv", index=False, header=False)
    val.to_csv("/opt/ml/processing/output/validation/validation.csv", index=False, header=False)
