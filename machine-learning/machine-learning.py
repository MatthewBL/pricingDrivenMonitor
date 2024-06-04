import pandas as pd
import joblib
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import RobustScaler
from math import sqrt

# Read the backend_access_data.csv file
backend_data = pd.read_csv('backend_access_data.csv')

# Read the frontend_access_data.csv file
frontend_data = pd.read_csv('frontend_access_data.csv')

# Read the metrics.csv file
metrics_data = pd.read_csv('metrics.csv')

# Merge the backend and frontend data on the "Request ID" column
merged_data = pd.merge(backend_data, frontend_data, on='Request ID', suffixes=('_backend', '_frontend'))

merged_data = pd.merge(merged_data, metrics_data, on='Endpoint', suffixes=('_request', '_metric'))

# Group the rows by endpoints and calculate the average request time of each endpoint
grouped_data = merged_data.groupby('Endpoint')['Request Time'].mean()

# Add a new feature "average request time", and give it the value obtained earlier
merged_data['Average Request Time'] = merged_data['Endpoint'].map(grouped_data)

# Initialize a Robust Scaler
scaler = RobustScaler()

# Fit the scaler to the 'Request Time' column and transform it
merged_data['Request Time'] = scaler.fit_transform(merged_data[['Request Time']])

# Split data into two datasets: one with isCached as true and another as false
cached_data = merged_data[merged_data['isCached'] == True]
not_cached_data = merged_data[merged_data['isCached'] == False]

def feature_selection(target_attribute, data):
    # Split the data into input and output
    X = data.drop(['CPU Usage', 'Memory Usage', 'Storage Usage', 'Request ID', 'Query', 'Endpoint'], axis=1)
    Y = data[target_attribute]

    categorical_columns = ['HTTP method', 'Pricing Plan', 'Response Status', 'Cache Used']
    X = pd.get_dummies(X, columns=categorical_columns)

    # Create a GBM model
    model = GradientBoostingRegressor()

    # Train the model
    model.fit(X, Y)

    # Create a selector object that will use the GBM model to identify
    # features that have an importance of more than 0.15
    sfm = SelectFromModel(model, threshold=0.15)

    # Train the selector
    sfm.fit(X, Y)

    return X.columns[sfm.get_support(indices=True)]

cpu_usage_feature_selection_cache = feature_selection('CPU Usage', cached_data)
cpu_usage_feature_selection_not_cache = feature_selection('CPU Usage', not_cached_data)
memory_usage_feature_selection_cache = feature_selection('Memory Usage', cached_data)
memory_usage_feature_selection_not_cache = feature_selection('Memory Usage', not_cached_data)
storage_usage_feature_selection_cache = feature_selection('Storage Usage', cached_data)
storage_usage_feature_selection_not_cache = feature_selection('Storage Usage', not_cached_data)

print('Cached CPU Usage: ' + str(cpu_usage_feature_selection_cache))
print('Not cached CPU Usage: ' + str(cpu_usage_feature_selection_not_cache))
print('Cached Memory Usage: '+ str(memory_usage_feature_selection_cache))
print('Not cached Memory Usage: '+ str(memory_usage_feature_selection_not_cache))
print('Cached Storage Usage: '+ str(storage_usage_feature_selection_cache))
print('Not cached Storage Usage: '+ str(storage_usage_feature_selection_not_cache))

def train_model(target_attribute, selected_feature_names, data, model=GradientBoostingRegressor()):
    # Select the features from the data
    X = data
    Y = data[target_attribute]

    categorical_columns = ['HTTP method', 'Pricing Plan', 'Response Status', 'Cache Used']
    X = pd.get_dummies(X, columns=categorical_columns)
    
    X = X[selected_feature_names]

    # Split the data into training and test sets
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    # Train the model
    model.fit(X_train, Y_train)

    evaluation = evaluate_model(model, X_test, Y_test)

    return model, evaluation

def evaluate_model(model, X_test, Y_test):
    # Use the model to make predictions on the test set
    predictions = model.predict(X_test)

    # Compute evaluation metrics
    mae = mean_absolute_error(Y_test, predictions)
    mse = mean_squared_error(Y_test, predictions)
    rmse = sqrt(mse)
    r2 = r2_score(Y_test, predictions)

    return [mae, mse, rmse, r2]

def predict(model, new_data):
    # Use the trained model to make predictions on the new data
    predictions = model.predict(new_data)

    return predictions

model = GradientBoostingRegressor()

cpu_usage_model_cache, cpu_usage_evaluation_cache = train_model('CPU Usage', cpu_usage_feature_selection_cache, data, model)
memory_usage_model_cache, memory_usage_evaluation_cache = train_model('Memory Usage', memory_usage_feature_selection_cache, data, model)
storage_usage_model_cache, storage_usage_evaluation_cache = train_model('Storage Usage', storage_usage_feature_selection_cache, data, model)

cpu_usage_model_not_cache, cpu_usage_evaluation_not_cache = train_model('CPU Usage', cpu_usage_feature_selection_not_cache, data, model)
memory_usage_model_not_cache, memory_usage_evaluation_not_cache = train_model('Memory Usage', memory_usage_feature_selection_not_cache, data, model)
storage_usage_model_not_cache, storage_usage_evaluation_not_cache = train_model('Storage Usage', storage_usage_feature_selection_not_cache, data, model)

print('Cached CPU Usage: ' + str(cpu_usage_evaluation_cache))
print('Not cached CPU Usage: ' + str(cpu_usage_evaluation_not_cache))
print('Cached Memory Usage: '+ str(memory_usage_evaluation_cache))
print('Not cached Memory Usage: '+ str(memory_usage_evaluation_not_cache))
print('Cached Storage Usage: '+ str(storage_usage_evaluation_cache))
print('Not cached Storage Usage: '+ str(storage_usage_evaluation_not_cache))

# Save the models to disk
joblib.dump(cpu_usage_model_cache, 'cpu_usage_model_cache.pkl')
joblib.dump(cpu_usage_model_not_cache, 'cpu_usage_model_not_cache.pkl')
joblib.dump(memory_usage_model_cache, 'memory_usage_model_cache.pkl')
joblib.dump(memory_usage_model_not_cache, 'memory_usage_model_not_cache.pkl')
joblib.dump(storage_usage_model_cache, 'storage_usage_model_cache.pkl')
joblib.dump(storage_usage_model_not_cache, 'storage_usage_model_not_cache.pkl')

# Save the selected features to disk
joblib.dump(cpu_usage_feature_selection_cache, 'cpu_usage_features_cache.pkl')
joblib.dump(cpu_usage_feature_selection_not_cache, 'cpu_usage_features_not_cache.pkl')
joblib.dump(memory_usage_feature_selection_cache, 'memory_usage_features_cache.pkl')
joblib.dump(memory_usage_feature_selection_not_cache, 'memory_usage_features_not_cache.pkl')
joblib.dump(storage_usage_feature_selection_cache, 'storage_usage_features_cache.pkl')
joblib.dump(storage_usage_feature_selection_not_cache, 'storage_usage_features_not_cache.pkl')