import cv2
import os
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# =========================================================
# LOAD DATASET
# =========================================================

dataset_path = "dataset"

X = []
y = []


for product in os.listdir(dataset_path):

    product_path = os.path.join(
        dataset_path,
        product
    )

    if not os.path.isdir(product_path):
        continue

    for image_name in os.listdir(product_path):

        image_path = os.path.join(
            product_path,
            image_name
        )

        image = cv2.imread(image_path)

        if image is None:
            continue

        image = cv2.resize(
            image,
            (100, 100)
        )

        image = image.flatten()

        X.append(image)
        y.append(product)


X = np.array(X)
y = np.array(y)


print("================================")
print("AI MODEL EVALUATION")
print("================================")

print("Total Images:", len(X))
print("Products:", np.unique(y))


# =========================================================
# SPLIT DATA
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.33,
    random_state=42,
    stratify=y
)


print("\nTraining Images:", len(X_train))
print("Testing Images:", len(X_test))


# =========================================================
# TRAIN MODEL
# =========================================================

model = KNeighborsClassifier(
    n_neighbors=3
)

model.fit(
    X_train,
    y_train
)


# =========================================================
# PREDICTION
# =========================================================

y_pred = model.predict(X_test)


# =========================================================
# ACCURACY
# =========================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n================================")
print("MODEL ACCURACY")
print("================================")

print(
    "Accuracy:",
    round(accuracy * 100, 2),
    "%"
)


# =========================================================
# CLASSIFICATION REPORT
# =========================================================

print("\n================================")
print("CLASSIFICATION REPORT")
print("================================")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# =========================================================
# CONFUSION MATRIX
# =========================================================

print("\n================================")
print("CONFUSION MATRIX")
print("================================")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)

print("\nEvaluation completed successfully!")