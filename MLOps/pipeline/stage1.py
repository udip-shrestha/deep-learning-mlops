

import pandas as pd
from sklearn.datasets import fetch_california_housing
import os

# Set output directory
os.makedirs("data/raw", exist_ok=True)

# Fetch dataset
data = fetch_california_housing(as_frame=True)
df = pd.concat([data.data, data.target.rename("target")], axis=1)

# Save to CSV
df.to_csv("data/raw/housing.csv", index=False)
print(" California housing data saved to data/raw/housing.csv")