import os
import sys
import warnings
import logging
from urllib.parse import urlparse

import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature
import dagshub

# === Initialize Dagshub for MLflow Tracking ===
dagshub.init(repo_owner='udipsth1', repo_name='MLFlow_test', mlflow=True)

# === Logging Setup ===
logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

# === Evaluation Function ===
def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


# === Main Script ===
if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    np.random.seed(42)

    # === Load Dataset ===
    csv_url = (
             "https://raw.githubusercontent.com/mlflow/mlflow/master/tests/datasets/winequality-red.csv"
     )

    try:
        data = fetch_california_housing(as_frame=True)
        df = pd.concat([data.data, data.target.rename("MedHouseVal")], axis=1)
    except Exception as e:
        logger.exception("Failed to load dataset. Error: %s", e)
        sys.exit(1)

    # === Split Data ===
    train_df, test_df = train_test_split(df, test_size=0.25, random_state=42)
    train_x = train_df.drop("MedHouseVal", axis=1)
    test_x = test_df.drop("MedHouseVal", axis=1)
    train_y = train_df["MedHouseVal"]
    test_y = test_df["MedHouseVal"]

    # === Hyperparameters from CLI or default ===
    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5

    # === Start MLflow Run ===
    with mlflow.start_run():
        model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        model.fit(train_x, train_y)
        predictions = model.predict(test_x)

        # === Eval + Log Metrics ===
        rmse, mae, r2 = eval_metrics(test_y, predictions)
        print(f"ElasticNet model (alpha={alpha}, l1_ratio={l1_ratio}):")
        print(f"  RMSE: {rmse}")
        print(f"  MAE: {mae}")
        print(f"  R2: {r2}")

        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)

        # === Save model ===
        signature = infer_signature(train_x, predictions)

        remote_server_uri = "https://dagshub.com/udipsth1/MLFlow_test.mlflow"
        mlflow.set_tracking_uri(remote_server_uri)

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        if tracking_url_type_store != "file":
            mlflow.sklearn.log_model(
                model,
                "model",
                registered_model_name="ElasticNetCaliforniaModel",
                signature=signature
            )
        else:
            mlflow.sklearn.log_model(model, "model", signature=signature)
