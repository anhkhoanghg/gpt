import json
from sklearn.model_selection import train_test_split
import random

# Load the JSON data
file_path = './data/prompt-target/full_data.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Shuffle the data
# Ensure that your data has a sufficient size before shuffling, as shuffling may not be meaningful for small datasets.
random_seed = 42  # You can choose any seed for reproducibility
data_shuffled = data[:]  # Create a copy to avoid modifying the original data
random.shuffle(data_shuffled)

# Split the data into training and testing sets (80% train, 20% test in this example)
train_data, test_data = train_test_split(data_shuffled, test_size=0.05, random_state=random_seed)

# Save the split data into separate JSON files
train_file_path = './data/prompt-target/train_data.json'
test_file_path = './data/prompt-target/test_data.json'

with open(train_file_path, 'w') as train_file:
    json.dump(train_data, train_file, indent=2)

with open(test_file_path, 'w') as test_file:
    json.dump(test_data, test_file, indent=2)