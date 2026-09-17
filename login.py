import streamlit as st


# =========================================================
# LOGIN DETAILS
# =========================================================

USERNAME = "admin"
PASSWORD = "admin123"


# =========================================================
# LOGIN FUNCTION
# =========================================================

def login():

    st.title("🔐 Smart Inventory Login")

    st.write("Please login to access the inventory system.")

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username == USERNAME and password == PASSWORD:

            st.session_state["logged_in"] = True

            st.success(
                "Login successful!"
            )

            st.rerun()

        else:

            st.error(
                "❌ Invalid username or password"
            )


# =========================================================
# CHECK LOGIN
# =========================================================

if "logged_in" not in st.session_state:

    st.session_state["logged_in"] = False


if not st.session_state["logged_in"]:

    login()

else:

    st.title("📦 Smart Inventory Management")

    st.success(
        "You are logged in successfully!"
    )

    if st.button("Logout"):

        st.session_state["logged_in"] = False

        st.rerun()