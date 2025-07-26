#  Train a simple regression model

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

# Paths
TRAIN_PATH = "data/processed/train.csv"
TEST_PATH = "data/processed/test.csv"
MODEL_PATH = "models/linear_regression.joblib"

def main():
    os.makedirs("models", exist_ok=True)

    train_df = pd.read_csv(TRAIN_PATH)
    test_df = pd.read_csv(TEST_PATH)

    X_train = train_df.drop("median_house_value", axis=1)
    y_train = train_df["median_house_value"]
    X_test = test_df.drop("median_house_value", axis=1)
    y_test = test_df["median_house_value"]

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print(f" Model trained: MSE = {mse:.2f}, R2 = {r2:.2f}")

    joblib.dump(model, MODEL_PATH)
    print(f" Model saved to {MODEL_PATH}")

if __name__ == '__main__':
    main()
