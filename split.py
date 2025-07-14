import json
import random

# Load the original JSON
with open('kaakaa_vgg_regions.json', 'r') as f:
    data = json.load(f)

# Shuffle the keys for random sampling
keys = list(data.keys())
random.shuffle(keys)

# Split 80/20
split_index = int(len(keys) * 0.8)
train_keys = keys[:split_index]
val_keys = keys[split_index:]

# Create train and validation dictionaries
train_data = {k: data[k] for k in train_keys}
val_data = {k: data[k] for k in val_keys}

# Save the new JSONs
with open('train_set.json', 'w') as f:
    json.dump(train_data, f, indent=2)

with open('validation_set.json', 'w') as f:
    json.dump(val_data, f, indent=2)

print(f"Total images: {len(keys)}")
print(f"Training images: {len(train_data)}")
print(f"Validation images: {len(val_data)}")