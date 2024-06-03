import pandas as pd
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression

# Read the backend_access_data.csv file
backend_data = pd.read_csv('backend_access_data.csv')

# Read the frontend_access_data.csv file
frontend_data = pd.read_csv('frontend_access_data.csv')

# Read the metrics.csv file
metrics_data = pd.read_csv('metrics.csv')

# Merge the backend and frontend data on the "Request ID" column
merged_data = pd.merge(backend_data, frontend_data, on='Request ID', suffixes=('_backend', '_frontend'))

merged_data = pd.merge(merged_data, metrics_data, on='Endpoint', suffixes=('_request', '_metric'))

def feature_selection(target_attribute, merged_data, k=5):
    # Split the data into input and output
    X = merged_data.drop(['CPU Usage', 'Memory Usage', 'Storage Usage', 'Request ID', 'Endpoint'], axis=1)
    Y = merged_data[target_attribute]

    categorical_columns = ['Query', 'HTTP method', 'Pricing Plan', 'Response Status']
    X = pd.get_dummies(X, columns=categorical_columns)

    # Feature extraction
    test = SelectKBest(score_func=f_regression, k=k)
    fit = test.fit(X, Y)

    features = fit.transform(X)

    # Get column names
    feature_names = X.columns

    # Get the indices of the features that were selected
    selected_features = fit.get_support(indices=True)

    # Get the names of the selected features
    selected_feature_names = feature_names[selected_features]

    return selected_feature_names

cpu_usage_feature_selection = feature_selection('CPU Usage', merged_data)
memory_usage_feature_selection = feature_selection('Memory Usage', merged_data)
storage_usage_feature_selection = feature_selection('Storage Usage', merged_data)

print('CPU Usage: ' + str(cpu_usage_feature_selection))
print('Memory Usage: '+ str(memory_usage_feature_selection))
print('Storage Usage: '+ str(storage_usage_feature_selection))

def cross_validation(target_attribute, selected_feature_names, merged_data, cv=5):
    # Select the features from the data
    X = merged_data
    Y = merged_data[target_attribute]

    categorical_columns = ['Query', 'HTTP method', 'Pricing Plan', 'Response Status']
    X = pd.get_dummies(X, columns=categorical_columns)
    
    X = X[selected_feature_names]

    # Create a Linear Regression model
    model = LinearRegression()

    # Perform cross-validation
    scores = cross_val_score(model, X, Y, cv=cv)

    return scores

cpu_usage_cross_validation = cross_validation('CPU Usage', cpu_usage_feature_selection, merged_data)
memory_usage_cross_validation = cross_validation('Memory Usage', memory_usage_feature_selection, merged_data)
storage_usage_cross_validation = cross_validation('Storage Usage', storage_usage_feature_selection, merged_data)

print('CPU Usage: ' + str(cpu_usage_cross_validation))
print('Memory Usage: '+ str(memory_usage_cross_validation))
print('Storage Usage: '+ str(storage_usage_cross_validation))