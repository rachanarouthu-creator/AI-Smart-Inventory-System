import cv2
import os
import pickle
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

# Path to dataset
dataset_path = "dataset"

X = []
y = []

# Read images from each product folder
for product in os.listdir(dataset_path):

    product_path = os.path.join(dataset_path, product)

    if not os.path.isdir(product_path):
        continue

    for image_name in os.listdir(product_path):

        image_path = os.path.join(product_path, image_name)

        image = cv2.imread(image_path)

        if image is None:
            continue

        # Resize image
        image = cv2.resize(image, (100, 100))

        # Convert image into one-dimensional array
        image = image.flatten()

        X.append(image)
        y.append(product)

# Convert to NumPy arrays
X = np.array(X)
y = np.array(y)

print("Number of images:", len(X))
print("Products:", np.unique(y))

# Create KNN model
model = KNeighborsClassifier(n_neighbors=3)

# Train model
model.fit(X, y)

# Save model
with open("model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model trained successfully!")
print("Model saved as model.pkl")