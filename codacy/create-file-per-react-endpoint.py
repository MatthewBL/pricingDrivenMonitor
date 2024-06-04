import os
import re

# Prompt the user for the directory where their React project is located
project_dir = input("Please enter the path to your React project: ")

# Ask the user if they use "/path" to define their routes
use_slash_path = input("Do you use '/path' to define your routes? (yes/no): ")

# Define the regular expression pattern for the React Router routes
if use_slash_path.lower() == 'yes':
    pattern = re.compile(r'<Route\s+path="/(.*?)"\s+component={(\w+)}', re.DOTALL)
else:
    pattern = re.compile(r'<Route\s+path="(.*?)"\s+component={(\w+)}', re.DOTALL)

# Define output directory
output_dir = "/react_output"

# Create the directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Walk through the project directory
for root, dirs, files in os.walk(project_dir):
    for file in files:
        # Only consider .js, .jsx, .ts, and .tsx files
        if file.endswith(('.js', '.jsx', '.ts', '.tsx')):
            try:
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    matches = re.findall(pattern, content)
                    for i, match in enumerate(matches):
                        # Write the code for each endpoint to a separate file
                        with open(os.path.join(output_dir, f'{match[1].replace("/", "_")}_{i}.js'), 'w') as out_file:
                            out_file.write(match[0].strip())
            except FileNotFoundError:
                print(f"Could not open file {file}")
            except re.error:
                print(f"Invalid regular expression pattern")