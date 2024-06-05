import os
import pandas as pd
from sklearn.externals import joblib

# Define the directory path
dir_path = '../pre-trained models'

# Load the models from disk
cpu_usage_model_cache = joblib.load(os.path.join(dir_path, 'cpu_usage_model_cache.pkl'))
cpu_usage_model_not_cache = joblib.load(os.path.join(dir_path, 'cpu_usage_model_not_cache.pkl'))
memory_usage_model_cache = joblib.load(os.path.join(dir_path, 'memory_usage_model_cache.pkl'))
memory_usage_model_not_cache = joblib.load(os.path.join(dir_path, 'memory_usage_model_not_cache.pkl'))
storage_usage_model_cache = joblib.load(os.path.join(dir_path, 'storage_usage_model_cache.pkl'))
storage_usage_model_not_cache = joblib.load(os.path.join(dir_path, 'storage_usage_model_not_cache.pkl'))

# Load the selected features from disk
cpu_usage_features_cache = joblib.load(os.path.join(dir_path, 'cpu_usage_features_cache.pkl'))
cpu_usage_features_not_cache = joblib.load(os.path.join(dir_path, 'cpu_usage_features_not_cache.pkl'))
memory_usage_features_cache = joblib.load(os.path.join(dir_path, 'memory_usage_features_cache.pkl'))
memory_usage_features_not_cache = joblib.load(os.path.join(dir_path, 'memory_usage_features_not_cache.pkl'))
storage_usage_features_cache = joblib.load(os.path.join(dir_path, 'storage_usage_features_cache.pkl'))
storage_usage_features_not_cache = joblib.load(os.path.join(dir_path, 'storage_usage_features_not_cache.pkl'))

# Define the directory path
dir_path = '../dataset'

# Load the data from the CSV files
df = pd.read_csv(os.path.join(dir_path, 'input_data.csv'))
metrics_data = pd.read_csv(os.path.join(dir_path, 'metrics.csv'))
df = pd.merge(df, metrics_data, on='Endpoint', suffixes=('_request', '_metric'))

# Split the dataframe based on the 'isCached' column
df_cached = df.loc[df['isCached'] == True]
df_not_cached = df.loc[df['isCached'] == False]

def process_df(df, cpu_usage_features, memory_usage_features, storage_usage_features, cpu_usage_model, memory_usage_model, storage_usage_model):
    # Extract information that will be needed later
    request_id = df["Request ID"]
    endpoint = df["Endpoint"]
    pricing_plan = df["Pricing Plan"]
    request_time = df["Request Time"]

    # Select the relevant features from the DataFrame
    df_cpu = df[cpu_usage_features]
    df_memory = df[memory_usage_features]
    df_storage = df[storage_usage_features]

    # Make predictions
    cpu_usage_pred = cpu_usage_model.predict(df_cpu)
    memory_usage_pred = memory_usage_model.predict(df_memory)
    storage_usage_pred = storage_usage_model.predict(df_storage)

    return request_id, endpoint, pricing_plan, request_time, cpu_usage_pred, memory_usage_pred, storage_usage_pred

# Call the function for both dataframes
request_id_cache, endpoint_cache, pricing_plan_cache, request_time_cache, cpu_usage_cache_pred, memory_usage_cache_pred, storage_usage_cache_pred = process_df(df_cached, cpu_usage_features_cache, memory_usage_features_cache, storage_usage_features_cache, cpu_usage_model_cache, memory_usage_model_cache, storage_usage_model_cache)
request_id_not_cache, endpoint_not_cache, pricing_plan_not_cache, request_time_not_cache, cpu_usage_not_cache_pred, memory_usage_not_cache_pred, storage_usage_not_cache_pred = process_df(df_not_cached, cpu_usage_features_not_cache, memory_usage_features_not_cache, storage_usage_features_not_cache, cpu_usage_model_not_cache, memory_usage_model_not_cache, storage_usage_model_not_cache)

# Create dataframes from the returned values
df_cache = pd.DataFrame({
    'Request ID': request_id_cache,
    'Endpoint': endpoint_cache,
    'Pricing Plan': pricing_plan_cache,
    'Request Time': request_time_cache,
    'CPU Usage': cpu_usage_cache_pred,
    'Memory Usage': memory_usage_cache_pred,
    'Storage Usage': storage_usage_cache_pred,
    'isCached': True
})

df_not_cache = pd.DataFrame({
    'Request ID': request_id_not_cache,
    'Endpoint': endpoint_not_cache,
    'Pricing Plan': pricing_plan_not_cache,
    'Request Time': request_time_not_cache,
    'CPU Usage': cpu_usage_not_cache_pred,
    'Memory Usage': memory_usage_not_cache_pred,
    'Storage Usage': storage_usage_not_cache_pred,
    'isCached': False
})

# Concatenate the dataframes
df_output = pd.concat([df_cache, df_not_cache])

# Define the directory
dir_name = '../pre-trained models/dataset'

# Check if the directory exists
if not os.path.exists(dir_name):
    # If the directory doesn't exist, create it
    os.makedirs(dir_name)

# Write the dataframe to a CSV file in the directory
df_output.to_csv(os.path.join(dir_name, 'output.csv'), index=False)