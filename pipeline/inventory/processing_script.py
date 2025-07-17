import argparse
import pandas as pd
import os
import logging
from sklearn.model_selection import train_test_split  # Added this import

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-data', type=str, required=True)
    args = parser.parse_args()

    logger.info(f"Input data directory: {args.input_data}")
    logger.info(f"Files in input directory: {os.listdir(args.input_data)}")

    try:
        # List files in the input directory
        input_files = os.listdir(args.input_data)
        logger.info(f"Found files: {input_files}")

        # Read the data
        # Assuming the CSV file is the only file in the directory
        input_file = os.path.join(args.input_data, input_files[0])
        logger.info(f"Reading file: {input_file}")
        df = pd.read_csv(input_file)
        logger.info(f"Data shape: {df.shape}")

        # Create output directories if they don't exist
        os.makedirs("/opt/ml/processing/train", exist_ok=True)
        os.makedirs("/opt/ml/processing/test", exist_ok=True)
        logger.info("Created output directories")

        # Split the data
        train_data, test_data = train_test_split(
            df, test_size=0.2, random_state=42)
        logger.info(f"Train data shape: {train_data.shape}")
        logger.info(f"Test data shape: {test_data.shape}")

        # Save the split datasets
        train_data.to_csv("/opt/ml/processing/train/train.csv", index=False)
        test_data.to_csv("/opt/ml/processing/test/test.csv", index=False)
        logger.info("Saved train and test datasets")

        logger.info("Processing completed successfully!")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise e


if __name__ == "__main__":
    main()
