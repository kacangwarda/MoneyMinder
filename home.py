import streamlit as st
import plotly.graph_objects as go
import sqlite3
import pandas as pd

# Home Page
def home():
    st.markdown(f"#### <span style='color:black'>Welcome to MoneyMinder, {st.session_state.first_name}! Manage your finances smartly and efficiently.</span>", unsafe_allow_html=True)

    # Connect to the database and retrieve user data
    conn = sqlite3.connect('moneyminder.db')
    c = conn.cursor()

    c.execute("SELECT salary FROM profiles WHERE username = ?", (st.session_state.username,))
    salary = c.fetchone()[0]
    
    total_expenses = pd.read_sql_query("SELECT SUM(amount) as total FROM expenses WHERE username = ?", conn, params=(st.session_state.username,)).iloc[0]['total']
    if total_expenses is None:
        total_expenses = 0.0

    total_commitments = pd.read_sql_query("SELECT SUM(amount) as total FROM commitments WHERE username = ?", conn, params=(st.session_state.username,)).iloc[0]['total']
    if total_commitments is None:
        total_commitments = 0.0

    # Current Balance Calculation
    current_balance = salary - total_commitments - total_expenses

    # Salary and Commitments Interactive Donut Chart
    labels1 = ['Remaining Salary', 'Commitments']
    values1 = [salary - total_commitments, total_commitments]
    fig1 = go.Figure(data=[go.Pie(labels=labels1, values=values1, hole=0.4, marker=dict(colors=['#00cc96', '#ff6692']), name='')])
    fig1.update_traces(hovertemplate='%{label}<br>RM %{value}<br>%{percent:.1f}%', textinfo='value+percent', textfont_size=16)
    fig1.update_layout(title_text='Salary vs Commitments', title_font_size=20, annotations=[dict(text='Salary', x=0.5, y=0.5, font_size=20, showarrow=False)])

    # Current Balance and Daily Expenses Interactive Donut Chart
    labels2 = ['Current Balance', 'Daily Expenses']
    values2 = [current_balance, total_expenses]
    fig2 = go.Figure(data=[go.Pie(labels=labels2, values=values2, hole=0.4, marker=dict(colors=['#636efa', '#ffa15a']), name='')])
    fig2.update_traces(hovertemplate='%{label}<br>RM %{value}<br>%{percent:.1f}%', textinfo='value+percent', textfont_size=16)
    fig2.update_layout(title_text='Current Balance vs Daily Expenses', title_font_size=20, annotations=[dict(text='Balance', x=0.5, y=0.5, font_size=20, showarrow=False)])

    # Investment Money Interactive Donut Chart (No data yet)
    labels3 = ['Investment Money', 'Not Invested']
    values3 = [0, 100]  # Placeholder values
    fig3 = go.Figure(data=[go.Pie(labels=labels3, values=values3, hole=0.4, marker=dict(colors=['#ab63fa', '#f3f3f3']), name='')])
    fig3.update_traces(hovertemplate='%{label}<br>RM %{value}<br>%{percent:.1f}%', textinfo='value+percent', textfont_size=16)
    fig3.update_layout(title_text='Investment Money', title_font_size=20, annotations=[dict(text='Investment', x=0.5, y=0.5, font_size=20, showarrow=False)])

    # Display the charts
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    st.plotly_chart(fig3)

    # Close the database connection
    conn.close()

# Assuming that salary, commitments, and daily_expenses are set in session_state
if 'username' not in st.session_state:
    st.session_state.username = 'default_user'  # Example username
