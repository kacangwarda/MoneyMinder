import streamlit as st
import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import random

def gold_investment(c, conn):
    # Page Title
    st.markdown("<h1 style='color: #DAA520; font-weight: bold; text-align: center;'>💰 24K Gold Price Tracker 💰</h1>", unsafe_allow_html=True)

    # Introduction Section
    st.markdown("<p style='color: #000000; text-align: center; font-size: 16px;'>Stay up-to-date with the latest 24K gold prices and make informed investment decisions.</p>", unsafe_allow_html=True)

    # Create two columns for better layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # Gold Price Section
        st.markdown("<h2 style='color: #000000; font-weight: bold;'>Live Gold Price</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #000000;'>Fetching live data for 24K gold price...</p>", unsafe_allow_html=True)

        # Function to fetch live 24K gold price
        def fetch_24k_gold_price():
            url = "https://www.livepriceofgold.com/malaysia-gold-price-per-gram.html"
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                table = soup.find('table', class_='data-table-price')
                if table:
                    rows = table.find_all('tr')
                    for row in rows[1:]:
                        cols = row.find_all('td')
                        cols = [col.text.strip() for col in cols]
                        if cols and "24K" in cols[0]:  # Check if the row is for 24K gold
                            gold_price = cols[1]
                            return float(gold_price.replace("MYR", "").replace(",", "").strip())
                else:
                    st.warning("Could not find the relevant data table.")
            else:
                st.error("Failed to fetch data. Please check the URL or try again later.")
            return None

        # Placeholder for displaying the gold price
        price_display = st.empty()

        # Display live 24K gold price
        def update_price_display():
            gold_price_value = fetch_24k_gold_price()
            if gold_price_value:
                price_display.markdown(
                    f"""
                    <div style='background-color: #F9F9F9; border: 4px solid #DAA520; padding: 10px; border-radius: 10px; text-align: center; width: fit-content;'>
                        <p style='color: #000000; font-size: 22px; font-weight: bold;'>1 gram 24K gold</p>
                        <p style='color: #000000; font-size: 25px; font-weight: bold;'>= MYR {gold_price_value:.2f}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                return gold_price_value
            else:
                price_display.markdown("<p style='color: #FF0000;'>Unable to display 24K gold price at this moment.</p>", unsafe_allow_html=True)
                return None

        gold_price_value = update_price_display()

        # Option to refresh data
        if st.button("🔄 Refresh Data"):
            with st.spinner("Updating data..."):
                time.sleep(2)  # Simulate a delay for user experience
                gold_price_value = update_price_display()

    with col2:
        # Gold Purchase Calculator Section
        if gold_price_value:
            # Gold Purchase Calculator Header
            st.markdown("""
                <h2 style='color: #000000; font-weight: bold;'>
                    Gold Purchase Calculator
                </h2>""", unsafe_allow_html=True)

            # Gold Input Section
            grams = st.number_input(
                "Enter grams of gold to buy:",
                min_value=0.0,
                step=0.1,
                key="grams"
            )

            # Calculate total cost button
            if st.button("💰 Calculate Total Cost"):
                total_cost = grams * gold_price_value
                st.markdown(f"<p style='color: #000000; font-size: 18px; font-weight: bold;'>Total cost for {grams} grams of 24K gold: MYR {total_cost:.2f}</p>", unsafe_allow_html=True)

                # Add Modify and Buy options side by side
                modify_col, buy_col = st.columns([1, 1])
                with modify_col:
                    if st.button("✏️ Modify Amount"):
                        st.experimental_rerun()  # Reset the input for a new amount
                with buy_col:
                    if st.button("🛒 Buy Gold"):
                        username = st.session_state.username
                        c.execute("INSERT INTO investments (username, category, amount) VALUES (?, ?, ?)", (username, 'gold', total_cost))
                        conn.commit()
                        st.success("Successfully bought gold! Your investment has been recorded.")
                        st.experimental_rerun()  # Refresh the app to show the updated total in the savings page
