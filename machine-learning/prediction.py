import pandas as pd
from sklearn.externals import joblib

# Load the models from disk
cpu_usage_model_cache = joblib.load('cpu_usage_model_cache.pkl')
cpu_usage_model_not_cache = joblib.load('cpu_usage_model_not_cache.pkl')
memory_usage_model_cache = joblib.load('memory_usage_model_cache.pkl')
memory_usage_model_not_cache = joblib.load('memory_usage_model_not_cache.pkl')
storage_usage_model_cache = joblib.load('storage_usage_model_cache.pkl')
storage_usage_model_not_cache = joblib.load('storage_usage_model_not_cache.pkl')

# Load the selected features from disk
cpu_usage_features_cache = joblib.load('cpu_usage_features_cache.pkl')
cpu_usage_features_not_cache = joblib.load('cpu_usage_features_not_cache.pkl')
memory_usage_features_cache = joblib.load('memory_usage_features_cache.pkl')
memory_usage_features_not_cache = joblib.load('memory_usage_features_not_cache.pkl')
storage_usage_features_cache = joblib.load('storage_usage_features_cache.pkl')
storage_usage_features_not_cache = joblib.load('storage_usage_features_not_cache.pkl')

# Load the data from the CSV files
df = pd.read_csv('input_data.csv')
metrics_data = pd.read_csv('metrics.csv')
df = pd.merge(df, metrics_data, on='Endpoint', suffixes=('_request', '_metric'))

# Extract information that will be needed later
pricing_plan = df["Pricing Plan"]
endpoint = df["Endpoint"]
request_time = df["Request Time"]

# Select the relevant features from the DataFrame
df_cpu_cache = df[cpu_usage_features_cache]
df_cpu_not_cache = df[cpu_usage_features_not_cache]
df_memory_cache = df[memory_usage_features_cache]
df_memory_not_cache = df[memory_usage_features_not_cache]
df_storage_cache = df[storage_usage_features_cache]
df_storage_not_cache = df[storage_usage_features_not_cache]

# Make predictions
cpu_usage_cache_pred = cpu_usage_model_cache.predict(df_cpu_cache)
cpu_usage_not_cache_pred = cpu_usage_model_not_cache.predict(df_cpu_not_cache)
memory_usage_cache_pred = memory_usage_model_cache.predict(df_memory_cache)
memory_usage_not_cache_pred = memory_usage_model_not_cache.predict(df_memory_not_cache)
storage_usage_cache_pred = storage_usage_model_cache.predict(df_storage_cache)
storage_usage_not_cache_pred = storage_usage_model_not_cache.predict(df_storage_not_cache)