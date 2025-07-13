import os
import pandas as pd
import numpy as np
from collections import defaultdict
from data_processing import extract_data
from feature_engineering import feature_engineering
from clustering import cluster_and_rank

dataset_path = "./dataset"

all_data = []
for filename in os.listdir(dataset_path):
    if filename.endswith(".json"):
        file_path = os.path.join(dataset_path, filename)
        all_data.extend(extract_data(file_path))

df_all = pd.DataFrame(all_data)
df_all['amount_usd'] = pd.to_numeric(df_all['amount_usd'], errors='coerce')
df_all['transaction_type'] = pd.to_numeric(df_all['transaction_type'], errors='coerce')

df_features = feature_engineering(df_all)

df_clustered = cluster_and_rank(df_features)

print(df_clustered[['wallet', 'credit_score']].sort_values(by='credit_score', ascending=False).head(10))