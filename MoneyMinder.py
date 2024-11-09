import streamlit as st
import sqlite3
from db_setup import conn, c
from auth import sign_up, login
from reginfo import complete_profile
from profilepage import profile_page
from home import home
from expenses import track_expenses
from savings import view_savings
from investment import gold_investment
from calczt import calculate_zakat_tax

# Main Function
def main():
    # Global CSS styling for the app
    page_wall = """
    <style>
    [data-testid="stAppViewContainer"] {
    background-image: url("https://www.uncclearn.org/wp-content/uploads/2019/11/06_sustainable_finance-1024x466.jpg");
    background-size: cover;
    background-blend-mode: normal;
    }
    h1.primary-header {
    color: #FFFFFF;
    font-size: 3em;
    font-weight: bold;
    text-shadow: 2px 2px 5px #000000;
    }
    .sidebar-text {
    color: #FFFFFF;
    font-size: 1.2em;
    font-weight: bold;
    text-shadow: 1px 1px 3px #000000;
    }
    .main-content-text {
    color: #000000;
    font-size: 1.1em;
    font-weight: bold;
    background-color: rgba(255, 255, 255, 0.8);
    padding: 10px;
    border-radius: 5px;
    }
    </style>
    """

    st.markdown(page_wall, unsafe_allow_html=True)
    # Application Title
    st.markdown("<h1 class='primary-header'>MoneyMinder: Integrated Expense Tracking and Investment Insights</h1>", unsafe_allow_html=True)

    # User Authentication
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        auth_choice = st.sidebar.radio("Login or Sign Up", ['Login', 'Sign Up'])
        if auth_choice == 'Sign Up':
            sign_up(c, conn)
        elif auth_choice == 'Login':
            login(c)
    else:
        # Load appropriate page based on sidebar selection
        option = st.sidebar.selectbox("Choose a feature", ['Home', 'Profile', 'Track Expenses', 'View Savings', 'Tax and Zakat Calculator', 'Gold Investment'])
        if option == 'Home':
            st.markdown("<div class='main-content-text'>", unsafe_allow_html=True)
            home()  # Call the home page function
            st.markdown("</div>", unsafe_allow_html=True)
        elif option == 'Profile':
            st.markdown("<div class='main-content-text'>", unsafe_allow_html=True)
            profile_page(c, conn)
            st.markdown("</div>", unsafe_allow_html=True)
        elif option == 'Track Expenses':
            st.markdown("<div class='main-content-text'>", unsafe_allow_html=True)
            track_expenses(c, conn)
            st.markdown("</div>", unsafe_allow_html=True)
        elif option == 'View Savings':
            st.markdown("<div class='main-content-text'>", unsafe_allow_html=True)
            view_savings(c, conn)
            st.markdown("</div>", unsafe_allow_html=True)
        elif option == 'Tax and Zakat Calculator':
            st.markdown("<div class='main-content-text'>", unsafe_allow_html=True)
            calculate_zakat_tax(c)
            st.markdown("</div>", unsafe_allow_html=True)
        elif option == 'Gold Investment':
            st.markdown("<div class='main-content-text'>", unsafe_allow_html=True)
            gold_investment(c, conn)
            st.markdown("</div>", unsafe_allow_html=True)

# Entry Point
if __name__ == "__main__":
    main()
