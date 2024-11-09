import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go

def view_savings(c, conn):
    st.markdown(
        "<h2 style='color: #000000; font-weight: bold;'>Savings Planning</h2>", 
        unsafe_allow_html=True
    )

    # Fetch user's salary
    c.execute("SELECT salary FROM profiles WHERE username = ?", (st.session_state.username,))
    salary = c.fetchone()[0]

    # Re-query total expenses and commitments from the database
    total_expenses = pd.read_sql_query(
        "SELECT SUM(amount) as total FROM expenses WHERE username = ?", conn, params=(st.session_state.username,)
    ).iloc[0]['total']
    total_expenses = total_expenses if total_expenses else 0.0

    total_commitments = pd.read_sql_query(
        "SELECT SUM(amount) as total FROM commitments WHERE username = ?", conn, params=(st.session_state.username,)
    ).iloc[0]['total']
    total_commitments = total_commitments if total_commitments else 0.0

    # Include zakat and tax in total commitments
    zakat = salary * 0.025
    tax = salary * 0.10
    total_commitments += zakat + tax

    # Re-query total investment in gold from the database
    total_investment = pd.read_sql_query(
        "SELECT SUM(amount) as total FROM investments WHERE username = ? AND category = ?", conn, params=(st.session_state.username, 'gold')
    ).iloc[0]['total']
    total_investment = total_investment if total_investment else 1627.21

    # Calculate remaining amount after all expenses, commitments, and investments
    remaining_amount = salary - total_expenses - total_commitments - total_investment

    # Display financial summary with consistent styling
    st.markdown(f"<p style='color: #000000; font-size: 20px; font-weight: bold;'>Total Expenses: RM {total_expenses:.2f}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #000000; font-size: 20px; font-weight: bold;'>Total Commitments: RM {total_commitments:.2f}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #000000; font-size: 20px; font-weight: bold;'>Total Investment: RM {total_investment:.2f}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #000000; font-size: 20px; font-weight: bold;'>Remaining Amount: RM {remaining_amount:.2f}</p>", unsafe_allow_html=True)

    # Notification messages based on remaining amount
    if remaining_amount > 0:
        st.success("You are managing your finances well!")
    else:
        st.warning("Your expenses exceed your income. Consider reducing spending.")

    # Percentage-based spending suggestion
    percentages = {
        'Food and beverages': 0.20,
        'Transportation': 0.15,
        'Financial services': 0.10,
        'Shopping': 0.10,
        'Telecommunications': 0.05,
        'Entertainment': 0.10,
        'Medical': 0.15,
        'Other': 0.15
    }

    st.markdown("<h3 style='color: #000000; font-weight: bold;'>Spending Suggestions Based on Salary</h3>", unsafe_allow_html=True)
    categories = []
    suggested_amounts = []
    for category, perc in percentages.items():
        suggested_amount = salary * perc
        categories.append(category)
        suggested_amounts.append(suggested_amount)
        st.markdown(
            f"<p style='color: #000000; font-size: 18px; font-weight: bold;'>"
            f"{category} ({perc*100}%): RM {suggested_amount:.2f}</p>",
            unsafe_allow_html=True
        )

        # Notify if user is nearing the limit
        category_expense = pd.read_sql_query(
            "SELECT SUM(amount) as total FROM expenses WHERE username = ? AND category = ?",
            conn, params=(st.session_state.username, category)
        ).iloc[0]['total']
        category_expense = category_expense if category_expense else 0.0
        if category_expense >= suggested_amount * 0.9:
            st.warning(f"You are nearing your suggested limit for {category}.")

    # Plotting interactive donut chart for spending suggestions
    fig = go.Figure(data=[go.Pie(labels=categories, values=suggested_amounts, hole=0.4)])
    fig.update_traces(hoverinfo='label+percent+value', textinfo='percent', textfont_size=14,
                      marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(
        title_text='Spending Suggestions Based on Salary',
        title_font=dict(color='#FFFFFF'),
        annotations=[dict(text='Spending', x=0.5, y=0.5, font_size=20, showarrow=False)],
        font=dict(color='#000000')
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig)

# Sample usage
# conn = sqlite3.connect('database.db')
# c = conn.cursor()
# view_savings(c, conn)
# conn.close()
