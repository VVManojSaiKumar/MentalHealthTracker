import streamlit as st
from modules import db, guidances, questions, visualization
import sqlite3
import hashlib

# Initialize database connection
conn = db.init_db()
st.set_page_config(layout="wide")

USERNAME = ""
PASSWORD = ""

DATABASE_PATH = "./databases/mental_health.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)  # Replace with your database file
    conn.execute('''CREATE TABLE IF NOT EXISTS users
                    (username TEXT PRIMARY KEY, password_hash TEXT)''')
    return conn

# Hash a password for storing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register a new user
def register_user(username, password):
    conn = get_db_connection()
    password_hash = hash_password(password)
    try:
        conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
    except sqlite3.IntegrityError:
        st.error("Username already exists.")
    finally:
        conn.close()

# Validate login
def validate_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    password_hash = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, password_hash))
    user = cursor.fetchone()
    conn.close()
    return user is not None
    
def validate_username(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Registration page
def register_page():
    st.session_state.page = "reg"
    st.title("Register as a New User")
    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        st.session_state.page = ""
        if new_password != confirm_password:
            st.error("Passwords do not match.")
        elif validate_username(new_username):
            st.error("UserName Already Exist")
        else:
            register_user(new_username, new_password)
            st.success("Registration successful! Please utin.")
            st.session_state.page = "login"
            if st.button("Login Page"):
                trigger_page()
    if st.button("Back to Login"):
        st.session_state.page = ""
        trigger_page()
        st.session_state.page = "login"
        trigger_page()


# Login page
def login_page():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        st.session_state.page = ""

        if validate_user(username, password):
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.success("Login successful!")
            st.session_state.page = "main"
            trigger_page()
        else:
            st.error("Invalid username or password.")
    if st.button("Register here"):
        st.session_state.page = ""
        st.session_state.page = "reg"
        trigger_page()
# Main page
def main_page():

    # Set up the main layout

    col1, spacer, col2 = st.columns([2, 0.2, 3])  # 40-5-60 ratio

    # Left frame (40%) with a radio button for options
    with col1:
    
        st.title("MoodLens")

        st.text("Welcome to the Moodlens App! This app allows you to check in your mental health, visualize your mood overtime, and receive guidance from the AI Powered therapist")
        st.image("logo.png")
        st.header("Select an option")
        option = st.radio(
            "Select an option:",
            ("Home", "Mental Health Check-in ", "Visualization", "Guidance", "Chat Assistance")
        )

    # Right frame (60%) that displays content based on the selected option
    with col2:
        col3, col4 = st.columns([4, 1])  # Adjust ratio for more space between columns

        with col3:
            st.header("MoodLens")

        with col4:
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.current_user = ""
                st.session_state.page = "login"

        
        if option == "Home":
            st.subheader("Home")
            st.write("MoodLens is a web application designed to help individuals track their mental health over time. By completing regular check-ins and recording their feelings,users can gain insights into their emotional patterns and identify areas for improvement.")
            st.subheader("Features")
            st.markdown("""
            * Interactive questionnaires to help users track their mental health.
            * Visualization of mental health data over time.
            * Personalized guidance based on user data and artificial intelligence
            """)
            st.subheader("How to Use")
            st.markdown("""
            1. Navigate to the MoodLens website

    2. Select the "Mental Health Check-In" option to complete a questionnaire about your current mental state

    3. View your mental health data over time in the "Visualization" section of the app

    4. Get personalized guidance from an Al-powered virtual psychologist in the "Guidances" section
            """)
        
        elif option == "Mental Health Check-in ":
            st.subheader("Mental Health Check-in")
            st.write("This section requires detailed information.")
            questions.ask_questions()

            
        elif option == "Visualization":
            st.subheader("Visualization")
            st.write("Here, you can view various statistics.")
            visualization.show_visualization()

            
        elif option == "Guidance":
            st.subheader("Guidance")
            guidances.show_guidance()
            

        elif option == "Chat Assistance":
            st.subheader("Chat Assistance")
            guidances.chatbot()


is_logged_in = st.session_state.get("logged_in", False)  
def trigger_page():
    page = st.session_state.get("page", "login")  
    print(page)
    if(page=="main"):
        main_page()
    elif(page=="reg"):
        register_page()
    elif(page=="login"):
        login_page()

trigger_page()
