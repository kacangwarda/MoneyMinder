import streamlit as st
import pandas as pd
import sqlite3

# Profile Page
def profile_page(c, conn):
    st.markdown("<h2 style='color: #000000; font-weight: bold;'>Profile Page</h2>", unsafe_allow_html=True)

    # Display current profile information
    c.execute("SELECT salary FROM profiles WHERE username = ?", (st.session_state.username,))
    profile = c.fetchone()
    if profile:
        salary = profile[0]
        st.markdown(f"<p style='color: #000000; font-size: 18px; font-weight: bold;'>Monthly Salary: RM {salary}</p>", unsafe_allow_html=True)

    # Update salary
    new_salary = st.number_input("Update Monthly Salary", min_value=0.0, value=salary)
    if st.button("Update Salary"):
        c.execute("UPDATE profiles SET salary = ? WHERE username = ?", (new_salary, st.session_state.username))
        conn.commit()
        st.success("Salary updated successfully!")

    # Add new commitment
    st.markdown("<h3 style='color: #000000;'>Add New Commitment</h3>", unsafe_allow_html=True)
    commitment_name = st.text_input("New Commitment Name")
    commitment_amount = st.number_input("New Commitment Amount", min_value=0.0)
    if st.button("Add New Commitment"):
        c.execute("INSERT INTO commitments (username, commitment_name, amount) VALUES (?, ?, ?)", 
                  (st.session_state.username, commitment_name, commitment_amount))
        conn.commit()
        st.success(f"Commitment '{commitment_name}' of RM {commitment_amount} added successfully.")
        st.session_state.refresh = not st.session_state.get('refresh', False)  # Toggle refresh state

    # Load and display current commitments with a 'Select' column for deletion
    st.markdown("<h3 style='color: #000000;'>Current Commitments</h3>", unsafe_allow_html=True)
    c.execute("SELECT rowid, commitment_name, amount FROM commitments WHERE username = ?", 
              (st.session_state.username,))
    commitments = c.fetchall()
    commitment_data = pd.DataFrame(commitments, columns=['ID', 'Commitment Name', 'Amount'])

    if not commitment_data.empty:

        # Display the commitments with delete buttons
        for i, row in commitment_data.iterrows():
            col1, col2, col3 = st.columns([4, 3, 2])
            col1.markdown(f"<p style='color: #000000;'>{row['Commitment Name']}</p>", unsafe_allow_html=True)
            col2.markdown(f"<p style='color: #000000;'>RM {row['Amount']}</p>", unsafe_allow_html=True)
            if col3.button("Delete", key=f"delete_{row['ID']}"):
                c.execute("DELETE FROM commitments WHERE rowid = ?", (row['ID'],))
                conn.commit()
                st.success(f"Commitment '{row['Commitment Name']}' removed successfully.")
                st.session_state.refresh = not st.session_state.get('refresh', False)  # Toggle refresh state
    else:
        st.info("No commitments to display.")
