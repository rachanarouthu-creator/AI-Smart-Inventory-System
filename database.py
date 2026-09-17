import sqlite3
import pandas as pd


# =========================================================
# CREATE DATABASE
# =========================================================

def create_database():

    connection = sqlite3.connect(
        "inventory.db"
    )

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT NOT NULL,
            category TEXT NOT NULL,
            expiry_date TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# =========================================================
# IMPORT PRODUCTS FROM CSV
# =========================================================

def import_products():

    connection = sqlite3.connect(
        "inventory.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM products"
    )

    count = cursor.fetchone()[0]

    if count == 0:

        products = pd.read_csv(
            "products.csv"
        )

        for _, row in products.iterrows():

            cursor.execute(
                """
                INSERT INTO products
                (product, category, expiry_date, quantity)
                VALUES (?, ?, ?, ?)
                """,
                (
                    row["Product"],
                    row["Category"],
                    row["ExpiryDate"],
                    int(row["Quantity"])
                )
            )

    connection.commit()
    connection.close()


# =========================================================
# GET PRODUCTS
# =========================================================

def get_products():

    connection = sqlite3.connect(
        "inventory.db"
    )

    products = pd.read_sql_query(
        "SELECT * FROM products",
        connection
    )

    connection.close()

    return products


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    create_database()

    import_products()

    products = get_products()

    print("\n================================")
    print("SMART INVENTORY DATABASE")
    print("================================")

    print(products)

    print("\nDatabase created successfully!")