import pandas as pd
from faker import Faker
import random

fake = Faker()

# Define the number of rows
num_rows = 1000

# Define the number of URLs
num_urls = 20

# Generate a list of URLs
urls = [fake.url() for _ in range(num_urls)]

# backend_access_data.csv
concurrent_requests = [random.randint(1, 100) for _ in range(num_rows)]
base_cpu_usage = [random.uniform(0.1, 50) for _ in range(num_rows)]  # in percentage
base_storage_usage = [random.uniform(0.1, 5000) for _ in range(num_rows)]  # in MB
base_memory_usage = [usage * random.uniform(0.1, 1) for usage in base_storage_usage]  # in MB

cpu_usage = [base + request * random.uniform(0.1, 0.5) for base, request in zip(base_cpu_usage, concurrent_requests)]  # in percentage
storage_usage = [base + request * random.uniform(0.1, 50) for base, request in zip(base_storage_usage, concurrent_requests)]  # in MB
memory_usage = [base + request * random.uniform(0.1, 50) for base, request in zip(base_memory_usage, concurrent_requests)]  # in MB

backend_data = {
    'Endpoint': urls * (num_rows // num_urls),
    'CPU Usage': cpu_usage,
    'Memory Usage': memory_usage,
    'Storage Usage': storage_usage,
    'Concurrent requests': concurrent_requests
}
df = pd.DataFrame(backend_data)
df.to_csv('backend_access_data.csv', index=False)

# fronted_access_data.csv
request_size = [usage * random.uniform(0.1, 1) for usage in base_storage_usage]  # in KB
request_time = [usage * random.uniform(0.1, 1) for usage in cpu_usage]  # in seconds

frontend_data = {
    'URL': urls * (num_rows // num_urls),
    'Query': [fake.uri_path() for _ in range(num_rows)],
    'HTTP method': [random.choice(['GET', 'POST', 'PUT', 'DELETE']) for _ in range(num_rows)],
    'Pricing Plan': [random.choice(['Free', 'Basic', 'Premium']) for _ in range(num_rows)],
    'Request Size': request_size,
    'Response Status': [random.choice([200, 404, 500]) for _ in range(num_rows)],
    'Request Time': request_time,
    'Response Size': [random.randint(1, 5000) for _ in range(num_rows)]  # in KB
}
df = pd.DataFrame(frontend_data)
df.to_csv('fronted_access_data.csv', index=False)

# metrics.csv
lines_of_code = [random.randint(1, 1000) for _ in range(num_urls)]
cyclomatic_complexity = [usage * random.uniform(0.1, 1) for usage in base_cpu_usage[:num_urls]]

metrics_data = {
    'Endpoint': urls,
    'Cyclomatic Complexity': cyclomatic_complexity,
    'Code Duplicity': [random.uniform(0, 100) for _ in range(num_urls)],  # in percentage
    'Lines of Code': lines_of_code
}
df = pd.DataFrame(metrics_data)
df.to_csv('metrics.csv', index=False)