# : Preprocess and split data

import pandas as pd
import os
from sklearn.model_selection import train_test_split

# Constants
RAW_DATA_PATH = "data/raw/housing.csv"
TRAIN_PATH = "data/processed/train.csv"
TEST_PATH = "data/processed/test.csv"
TEST_SIZE = 0.2
RANDOM_STATE = 42

def main():
    df = pd.read_csv(RAW_DATA_PATH)
    os.makedirs(os.path.dirname(TRAIN_PATH), exist_ok=True)

    train_df, test_df = train_test_split(df, test_size=TEST_SIZE, random_state=RANDOM_STATE)

    train_df.to_csv(TRAIN_PATH, index=False)
    test_df.to_csv(TEST_PATH, index=False)

    print(f"Train/Test data saved at {TRAIN_PATH} and {TEST_PATH}")

if __name__ == '__main__':
    main()
