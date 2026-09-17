import cv2
import pickle

# Load trained model
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

# Enter image path
image_path = input("Enter image path: ")

# Read image
image = cv2.imread(image_path)

if image is None:
    print("Image not found!")
    exit()

# Resize image
image = cv2.resize(image, (100, 100))

# Flatten image
image = image.flatten()

# Predict product
prediction = model.predict([image])

print("Predicted Product:", prediction[0])