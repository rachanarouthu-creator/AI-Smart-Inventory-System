import cv2
import os
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import pickle

# Read inventory data
df = pd.read_csv("products.csv")

print("Inventory Data:")
print(df)

dataset = "dataset"

X = []
y = []

# Read every product folder
for product_name in os.listdir(dataset):

    product_folder = os.path.join(dataset, product_name)

    if not os.path.isdir(product_folder):
        continue

    # Read images
    for image_name in os.listdir(product_folder):

        image_path = os.path.join(product_folder, image_name)

        img = cv2.imread(image_path)

        if img is not None:

            img = cv2.resize(img, (100, 100))
            img = img.flatten()

            X.append(img)
            y.append(product_name)

            print(image_name, "->", product_name)

# Train model
model = KNeighborsClassifier(n_neighbors=1)
model.fit(X, y)

# Save model
with open("model.pkl", "wb") as file:
    pickle.dump(model, file)

print("\nModel trained successfully!")
print("Total training images:", len(X))