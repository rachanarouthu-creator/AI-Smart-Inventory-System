
import streamlit as st
import pandas as pd
import sqlite3
import pickle
import cv2
import numpy as np
from datetime import datetime


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Smart Inventory Management",
    page_icon="📦",
    layout="wide"
)


# =====================================================
# LOGIN SYSTEM
# =====================================================

USERNAME = "admin"
PASSWORD = "admin123"


def login_page():

    st.title("🔐 Smart Inventory Management System")

    st.write("Please login to continue.")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username == USERNAME and password == PASSWORD:

            st.session_state["logged_in"] = True
            st.rerun()

        else:

            st.error("❌ Invalid username or password")


if "logged_in" not in st.session_state:

    st.session_state["logged_in"] = False


if not st.session_state["logged_in"]:

    login_page()
    st.stop()


# =====================================================
# DATABASE FUNCTIONS
# =====================================================

def get_products():

    connection = sqlite3.connect("inventory.db")

    products = pd.read_sql_query(
        "SELECT * FROM products",
        connection
    )

    connection.close()

    products = products.rename(
        columns={
            "product": "Product",
            "category": "Category",
            "expiry_date": "ExpiryDate",
            "quantity": "Quantity"
        }
    )

    return products


def update_quantity(product_name, quantity):

    connection = sqlite3.connect("inventory.db")

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE products
        SET quantity = ?
        WHERE product = ?
        """,
        (quantity, product_name)
    )

    connection.commit()
    connection.close()


def delete_product(product_name):

    connection = sqlite3.connect("inventory.db")

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM products
        WHERE product = ?
        """,
        (product_name,)
    )

    connection.commit()
    connection.close()


def add_product(
    product,
    category,
    expiry_date,
    quantity
):

    connection = sqlite3.connect("inventory.db")

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO products
        (product, category, expiry_date, quantity)
        VALUES (?, ?, ?, ?)
        """,
        (
            product,
            category,
            expiry_date,
            quantity
        )
    )

    connection.commit()
    connection.close()


# =====================================================
# LOAD INVENTORY
# =====================================================

products = get_products()


# =====================================================
# EXPIRY CALCULATION
# =====================================================

today = datetime.today().date()

days_remaining = []
statuses = []

for _, product in products.iterrows():

    expiry = datetime.strptime(
        product["ExpiryDate"],
        "%Y-%m-%d"
    ).date()

    days_left = (
        expiry - today
    ).days

    days_remaining.append(days_left)

    if days_left < 0:

        statuses.append("EXPIRED")

    elif days_left <= 30:

        statuses.append("EXPIRING SOON")

    else:

        statuses.append("SAFE")


products["Days Left"] = days_remaining

products["Expiry Status"] = statuses


# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

st.sidebar.title("📦 Smart Inventory")

st.sidebar.write("Welcome, Admin 👋")

st.sidebar.divider()

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📦 Inventory",
        "⚠️ Alerts",
        "🤖 AI Recognition",
        "📊 Analytics",
        "🛒 Restock Recommendations"
    ]
)

st.sidebar.divider()

if st.sidebar.button("🚪 Logout"):

    st.session_state["logged_in"] = False

    st.rerun()


# =====================================================
# DASHBOARD
# =====================================================

if menu == "🏠 Dashboard":

    st.title(
        "🏠 Smart Inventory Dashboard"
    )

    st.write(
        "AI-Based Product Recognition and Inventory Tracking"
    )

    st.divider()

    total_products = len(products)

    expired_products = len(
        products[
            products["Expiry Status"] == "EXPIRED"
        ]
    )

    expiring_products = len(
        products[
            products["Expiry Status"] == "EXPIRING SOON"
        ]
    )

    low_stock = len(
        products[
            products["Quantity"] <= 2
        ]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📦 Total Products",
            total_products
        )

    with col2:

        st.metric(
            "❌ Expired",
            expired_products
        )

    with col3:

        st.metric(
            "⚠️ Expiring Soon",
            expiring_products
        )

    with col4:

        st.metric(
            "🔴 Low Stock",
            low_stock
        )

    st.divider()

    st.subheader(
        "📋 Inventory Overview"
    )

    st.dataframe(
        products,
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# INVENTORY
# =====================================================

elif menu == "📦 Inventory":

    st.title("📦 Inventory Management")

    st.subheader("🔎 Search & Filter")

    col1, col2, col3 = st.columns(3)

    with col1:

        search = st.text_input(
            "Search Product"
        )

    with col2:

        categories = [
            "All"
        ] + sorted(
            products["Category"]
            .unique()
            .tolist()
        )

        category_filter = st.selectbox(
            "Category",
            categories
        )

    with col3:

        status_filter = st.selectbox(
            "Expiry Status",
            [
                "All",
                "SAFE",
                "EXPIRING SOON",
                "EXPIRED"
            ]
        )

    filtered_products = products.copy()

    if search:

        filtered_products = filtered_products[
            filtered_products["Product"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    if category_filter != "All":

        filtered_products = filtered_products[
            filtered_products["Category"]
            == category_filter
        ]

    if status_filter != "All":

        filtered_products = filtered_products[
            filtered_products["Expiry Status"]
            == status_filter
        ]

    st.subheader(
        "📋 Current Inventory"
    )

    st.dataframe(
        filtered_products,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ADD PRODUCT

    st.subheader("➕ Add New Product")

    with st.expander(
        "Add Product"
    ):

        new_product = st.text_input(
            "Product Name"
        )

        new_category = st.text_input(
            "Category"
        )

        new_expiry = st.date_input(
            "Expiry Date"
        )

        new_quantity = st.number_input(
            "Quantity",
            min_value=0,
            value=1
        )

        if st.button(
            "Add Product",
            key="add_product"
        ):

            if new_product and new_category:

                add_product(
                    new_product,
                    new_category,
                    new_expiry.strftime(
                        "%Y-%m-%d"
                    ),
                    new_quantity
                )

                st.success(
                    "✅ Product added successfully!"
                )

                st.rerun()

            else:

                st.error(
                    "Please enter product name and category."
                )

    # UPDATE QUANTITY

    st.subheader(
        "🔄 Update Quantity"
    )

    with st.expander(
        "Update Product Quantity"
    ):

        product_list = products[
            "Product"
        ].tolist()

        if product_list:

            selected_product = st.selectbox(
                "Select Product",
                product_list,
                key="update_product"
            )

            new_quantity = st.number_input(
                "New Quantity",
                min_value=0,
                value=1,
                key="new_quantity"
            )

            if st.button(
                "Update Quantity",
                key="update_quantity"
            ):

                update_quantity(
                    selected_product,
                    new_quantity
                )

                st.success(
                    "✅ Quantity updated!"
                )

                st.rerun()

    # DELETE PRODUCT

    st.subheader(
        "🗑️ Delete Product"
    )

    with st.expander(
        "Delete Product"
    ):

        product_list = products[
            "Product"
        ].tolist()

        if product_list:

            delete_name = st.selectbox(
                "Select Product",
                product_list,
                key="delete_product"
            )

            if st.button(
                "Delete Product",
                key="delete_button"
            ):

                delete_product(
                    delete_name
                )

                st.success(
                    "✅ Product deleted!"
                )

                st.rerun()


# =====================================================
# ALERTS
# =====================================================

elif menu == "⚠️ Alerts":

    st.title("⚠️ Inventory Alerts")

    st.subheader(
        "📅 Expiry Alerts"
    )

    expiry_alerts = products[
        products["Expiry Status"] != "SAFE"
    ]

    if expiry_alerts.empty:

        st.success(
            "✅ No expiry alerts."
        )

    else:

        st.dataframe(
            expiry_alerts[
                [
                    "Product",
                    "Category",
                    "ExpiryDate",
                    "Days Left",
                    "Expiry Status"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    st.subheader(
        "🔴 Low Stock Alerts"
    )

    low_stock_products = products[
        products["Quantity"] <= 2
    ]

    if low_stock_products.empty:

        st.success(
            "✅ No low-stock products."
        )

    else:

        st.dataframe(
            low_stock_products[
                [
                    "Product",
                    "Category",
                    "Quantity"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )


# =====================================================
# AI RECOGNITION
# =====================================================

elif menu == "🤖 AI Recognition":

    st.title(
        "🤖 AI Product Recognition"
    )

    st.write(
        "Upload or capture a product image."
    )

    # LOAD MODEL

    try:

        with open(
            "model.pkl",
            "rb"
        ) as file:

            model = pickle.load(file)

    except Exception:

        model = None

    product_names = {

        "horlicks":
            "Horlicks",

        "harpic":
            "Harpic",

        "kissan":
            "Kissan",

        "soya_sos":
            "Soya Sauce",

        "coriander_powder":
            "Coriander Powder",

        "oil":
            "Oil"
    }

    st.subheader(
        "📁 Upload Product Image"
    )

    uploaded_image = st.file_uploader(
        "Choose an image",
        type=[
            "jpg",
            "jpeg",
            "png"
        ]
    )

    if uploaded_image is not None:

        file_bytes = uploaded_image.read()

        image = cv2.imdecode(
            np.frombuffer(
                file_bytes,
                np.uint8
            ),
            cv2.IMREAD_COLOR
        )

        st.image(
            image,
            channels="BGR",
            caption="Uploaded Product"
        )

        if st.button(
            "🔍 Recognize Product",
            key="recognize_upload"
        ):

            if model is None:

                st.error(
                    "❌ AI model not found!"
                )

            else:

                resized = cv2.resize(
                    image,
                    (100, 100)
                )

                flattened = resized.flatten()

                prediction = model.predict(
                    [flattened]
                )[0]

                product_name = product_names.get(
                    prediction,
                    prediction
                )

                st.success(
                    f"🤖 Predicted Product: {product_name}"
                )

                matched = products[
                    products["Product"]
                    == product_name
                ]

                if not matched.empty:

                    product = matched.iloc[0]

                    st.subheader(
                        "📦 Product Information"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write(
                            "**Product:**",
                            product["Product"]
                        )

                        st.write(
                            "**Category:**",
                            product["Category"]
                        )

                        st.write(
                            "**Quantity:**",
                            product["Quantity"]
                        )

                    with col2:

                        st.write(
                            "**Expiry Date:**",
                            product["ExpiryDate"]
                        )

                        st.write(
                            "**Days Left:**",
                            product["Days Left"]
                        )

                        st.write(
                            "**Status:**",
                            product["Expiry Status"]
                        )

    st.divider()

    # CAMERA

    st.subheader(
        "📷 Scan Product Using Camera"
    )

    camera_image = st.camera_input(
        "Take a picture of the product"
    )

    if camera_image is not None:

        if st.button(
            "🤖 Recognize Camera Image",
            key="recognize_camera"
        ):

            file_bytes = camera_image.getvalue()

            image = cv2.imdecode(
                np.frombuffer(
                    file_bytes,
                    np.uint8
                ),
                cv2.IMREAD_COLOR
            )

            if model is not None:

                resized = cv2.resize(
                    image,
                    (100, 100)
                )

                flattened = resized.flatten()

                prediction = model.predict(
                    [flattened]
                )[0]

                product_name = product_names.get(
                    prediction,
                    prediction
                )

                st.success(
                    f"🤖 Predicted Product: {product_name}"
                )


# =====================================================
# ANALYTICS
# =====================================================

elif menu == "📊 Analytics":

    st.title(
        "📊 Inventory Analytics"
    )

    st.subheader(
        "Products by Category"
    )

    category_counts = products[
        "Category"
    ].value_counts()

    st.bar_chart(
        category_counts
    )

    st.divider()

    st.subheader(
        "📦 Product Quantities"
    )

    quantity_data = products[
        [
            "Product",
            "Quantity"
        ]
    ].set_index("Product")

    st.bar_chart(
        quantity_data
    )

    st.divider()

    st.subheader(
        "📅 Expiry Status Summary"
    )

    status_counts = products[
        "Expiry Status"
    ].value_counts()

    st.bar_chart(
        status_counts
    )


# =====================================================
# RESTOCK RECOMMENDATIONS
# =====================================================

elif menu == "🛒 Restock Recommendations":

    st.title(
        "🛒 Smart Restock Recommendations"
    )

    st.write(
        "The system recommends restocking based on current quantity."
    )

    recommendations = []

    for _, product in products.iterrows():

        quantity = int(
            product["Quantity"]
        )

        if quantity <= 2:

            recommendation = (
                "🔴 RESTOCK NOW"
            )

        elif quantity <= 5:

            recommendation = (
                "🟠 RESTOCK SOON"
            )

        else:

            recommendation = (
                "🟢 STOCK SUFFICIENT"
            )

        recommendations.append(
            {
                "Product":
                    product["Product"],

                "Category":
                    product["Category"],

                "Quantity":
                    quantity,

                "Recommendation":
                    recommendation
            }
        )

    recommendation_df = pd.DataFrame(
        recommendations
    )

    st.dataframe(
        recommendation_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader(
        "💡 Recommendation Logic"
    )

    st.write(
        "🔴 Quantity ≤ 2 → Restock Now"
    )

    st.write(
        "🟠 Quantity 3–5 → Restock Soon"
    )

    st.write(
        "🟢 Quantity > 5 → Stock Sufficient"
    )


# =====================================================
# FOOTER
# =====================================================

st.sidebar.divider()

st.sidebar.caption(
    "Smart Inventory Management System"
)

st.sidebar.caption(
    "AI + Computer Vision + SQLite + Streamlit"
)

