import pandas as pd
import joblib
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
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

def feature_selection(target_attribute, merged_data):
    # Split the data into input and output
    X = merged_data.drop(['CPU Usage', 'Memory Usage', 'Storage Usage', 'Request ID', 'Query', 'Endpoint'], axis=1)
    Y = merged_data[target_attribute]

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

cpu_usage_feature_selection = feature_selection('CPU Usage', merged_data)
memory_usage_feature_selection = feature_selection('Memory Usage', merged_data)
storage_usage_feature_selection = feature_selection('Storage Usage', merged_data)

print('CPU Usage: ' + str(cpu_usage_feature_selection))
print('Memory Usage: '+ str(memory_usage_feature_selection))
print('Storage Usage: '+ str(storage_usage_feature_selection))

def train_model(target_attribute, selected_feature_names, merged_data, model=GradientBoostingRegressor()):
    # Select the features from the data
    X = merged_data
    Y = merged_data[target_attribute]

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

cpu_usage_model, cpu_usage_evaluation = train_model('CPU Usage', cpu_usage_feature_selection, merged_data, model)
memory_usage_model, memory_usage_evaluation = train_model('Memory Usage', memory_usage_feature_selection, merged_data, model)
storage_usage_model, storage_usage_evaluation = train_model('Storage Usage', storage_usage_feature_selection, merged_data, model)

print('CPU Usage: ' + str(cpu_usage_evaluation))
print('Memory Usage: '+ str(memory_usage_evaluation))
print('Storage Usage: '+ str(storage_usage_evaluation))

# Save the models to disk
joblib.dump(cpu_usage_model, 'cpu_usage_model.pkl')
joblib.dump(memory_usage_model, 'memory_usage_model.pkl')
joblib.dump(storage_usage_model, 'storage_usage_model.pkl')

# Save the selected features to disk
joblib.dump(cpu_usage_feature_selection, 'cpu_usage_features.pkl')
joblib.dump(memory_usage_feature_selection, 'memory_usage_features.pkl')
joblib.dump(storage_usage_feature_selection, 'storage_usage_features.pkl')