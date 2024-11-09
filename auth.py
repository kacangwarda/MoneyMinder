import streamlit as st
import hashlib
import sqlite3
import time

# Utility function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Sign Up Function
def sign_up(c, conn):
    st.header("Create an Account")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    
    if st.button("Sign Up"):
        hashed_password = hash_password(password)
        if username and password and first_name and last_name:
            try:
                # Insert user data into the database
                c.execute("INSERT INTO users (username, password, first_name, last_name) VALUES (?, ?, ?, ?)",
                          (username, hashed_password, first_name, last_name))
                conn.commit()
                st.success("Account created successfully! Redirecting to login page...")
                time.sleep(1)
                st.session_state.auth_choice = 'Login'
            except sqlite3.IntegrityError:
                st.error("Username already exists. Please choose a different one.")
        else:
            st.error("All fields are required. Please fill them out.")

# Login Function
def login(c):
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    
    if st.button("Login"):
        if username and password:
            hashed_password = hash_password(password)
            c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
            user = c.fetchone()
            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.first_name = user[2]
                st.session_state.last_name = user[3]
                st.success(f"Welcome back, {user[2]}! Redirecting to home page...")
                time.sleep(1)
            else:
                st.error("Invalid username or password.")
        else:
            st.error("Please enter both username and password.")

# Entry Point
def main(c, conn):
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'auth_choice' not in st.session_state:
        st.session_state.auth_choice = 'Login'

    if st.session_state.logged_in:
        st.header(f"Welcome to the Home Page, {st.session_state.first_name}!")
    else:
        st.session_state.auth_choice = st.sidebar.radio("Login or Sign Up", ['Login', 'Sign Up'], index=(0 if st.session_state.auth_choice == 'Login' else 1))
        if st.session_state.auth_choice == 'Sign Up':
            sign_up(c, conn)
        elif st.session_state.auth_choice == 'Login':
            login(c)


