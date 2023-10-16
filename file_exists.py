import os

# Get the current working directory
current_directory = os.getcwd()
print("Current working directory:", current_directory)

# Provide the full path to the index.html file
html_file_path = './index.html'  # Replace with the actual full path

# Verify the existence of the file
if os.path.isfile(html_file_path):
    print("File exists:", html_file_path)
else:
    print("File does not exist:", html_file_path)
