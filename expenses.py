import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go

# Function to Track Expenses
def track_expenses(c, conn):
    st.markdown("<h2 style='color: #000000; font-weight: bold;'>Track Your Expenses</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #000000;'>Add and categorize your expenses.</p>", unsafe_allow_html=True)
    
    # User inputs for expenses
    expense_name = st.text_input("Expense Name")
    category = st.selectbox("Category", ['Food & Beverages', 'Transportation', 'Financial services', 'Shopping', 'Telecommunications', 'Entertainment', 'Medical', 'Others'])
    amount = st.number_input("Amount", min_value=0.0)

    if st.button("Add Expense"):
        username = st.session_state.username
        c.execute("INSERT INTO expenses (username, expense_name, category, amount) VALUES (?, ?, ?, ?)", (username, expense_name, category, amount))
        conn.commit()
        st.success(f"Expense '{expense_name}' of {amount} added under '{category}'.")

    # Load expenses from the database
    c.execute("SELECT rowid, expense_name, category, amount FROM expenses WHERE username = ?", (st.session_state.username,))
    rows = c.fetchall()
    expense_data = pd.DataFrame(rows, columns=['ID', 'Expense Name', 'Category', 'Amount'])

    # Display the expenses table if not empty
    if not expense_data.empty:
        st.subheader("Your Expenses")
        
        # Adding delete functionality for each expense
        for i, row in expense_data.iterrows():
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.markdown(f"<p style='color: #000000;'>{row['Expense Name']}</p>", unsafe_allow_html=True)
            col2.markdown(f"<p style='color: #000000;'>{row['Category']}</p>", unsafe_allow_html=True)
            col3.markdown(f"<p style='color: #000000;'>RM {row['Amount']:.2f}</p>", unsafe_allow_html=True)
            if col4.button("Delete", key=row['ID']):
                c.execute("DELETE FROM expenses WHERE rowid = ?", (row['ID'],))
                conn.commit()
                st.success(f"Successfully deleted expense '{row['Expense Name']}'")

        # Visualization of expenses using Plotly
        st.subheader("Expenses Breakdown")
        expense_summary = expense_data.groupby('Category')['Amount'].sum()
        fig = go.Figure(data=[go.Bar(x=expense_summary.index, y=expense_summary.values)])
        fig.update_traces(hoverinfo='x+y', textfont_size=12, marker=dict(line=dict(color='#000000', width=2)))
        fig.update_layout(
            title_text='Expenses Breakdown by Category',
            xaxis_title='Category',
            yaxis_title='Total Amount (RM)',
            template='plotly_white'
        )
        st.plotly_chart(fig)

# Sample usage
# conn = sqlite3.connect('database.db')
# c = conn.cursor()
# track_expenses(c, conn)
# conn.close()
