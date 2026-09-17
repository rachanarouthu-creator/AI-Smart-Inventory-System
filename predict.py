import cv2
import pickle
import pandas as pd
from datetime import datetime

# Load trained model
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

# Load inventory
products = pd.read_csv("products.csv")

# Get image path
image_path = input("Enter image path: ")

# Read image
image = cv2.imread(image_path)

if image is None:
    print("Image not found!")
    exit()

# Resize image
image = cv2.resize(image, (100, 100))

# Convert image to one-dimensional array
image = image.flatten()

# Predict product
prediction = model.predict([image])[0]

print("\nPredicted Product:", prediction)

# Convert ML name to CSV name
product_names = {
    "horlicks": "Horlicks",
    "harpic": "Harpic",
    "kissan": "Kissan",
    "soya_sos": "Soya Sauce",
    "coriander_powder": "Coriander Powder",
    "oil": "Oil"
}

product_name = product_names.get(prediction)

if product_name is None:
    print("Product not found in inventory!")
    exit()

# Find product in inventory
product = products[products["Product"] == product_name]

if product.empty:
    print("Product not found in CSV!")
    exit()

product = product.iloc[0]

# Get details
category = product["Category"]
expiry_date = product["ExpiryDate"]
quantity = product["Quantity"]

# Calculate expiry status
today = datetime.today().date()
expiry = datetime.strptime(expiry_date, "%Y-%m-%d").date()

days_left = (expiry - today).days

if days_left < 0:
    status = "EXPIRED"
elif days_left <= 30:
    status = "EXPIRING SOON"
else:
    status = "SAFE"

# Low stock check
if quantity <= 2:
    stock_status = "LOW STOCK"
else:
    stock_status = "STOCK AVAILABLE"

# Display information
print("\n------ PRODUCT DETAILS ------")
print("Product:", product_name)
print("Category:", category)
print("Quantity:", quantity)
print("Expiry Date:", expiry_date)
print("Days Left:", days_left)
print("Expiry Status:", status)
print("Stock Status:", stock_status)