import streamlit as st
import pandas as pd
import sqlite3

# Function to Complete Profile
def complete_profile(c, conn):
    st.header("Complete Your Profile")
    salary = st.number_input("Monthly Salary", min_value=0.0)
    st.subheader("Add Monthly Commitments")
    commitment_name = st.text_input("Commitment Name")
    commitment_amount = st.number_input("Commitment Amount", min_value=0.0)
    if st.button("Add Commitment"):
        c.execute("INSERT INTO commitments (username, commitment_name, amount) VALUES (?, ?, ?)", (st.session_state.username, commitment_name, commitment_amount))
        conn.commit()
        st.success(f"Commitment '{commitment_name}' of RM {commitment_amount} added successfully.")

    # Display current commitments
    st.subheader("Current Commitments")
    c.execute("SELECT rowid, commitment_name, amount FROM commitments WHERE username = ?", (st.session_state.username,))
    commitments = c.fetchall()
    if commitments:
        commitment_data = pd.DataFrame(commitments, columns=['ID', 'Commitment Name', 'Amount'])
        st.dataframe(commitment_data)
        for commitment in commitments:
            if st.button(f"Remove {commitment[1]}", key=f"remove_{commitment[0]}"):
                c.execute("DELETE FROM commitments WHERE rowid = ?", (commitment[0],))
                conn.commit()
                st.success(f"Commitment '{commitment[1]}' removed successfully.")
            if st.button(f"Modify {commitment[1]}", key=f"modify_{commitment[0]}"):
                new_commitment_amount = st.number_input(f"New amount for {commitment[1]}", min_value=0.0, value=commitment[2], key=f"new_amount_{commitment[0]}")
                if st.button(f"Save {commitment[1]}", key=f"save_{commitment[0]}"):
                    c.execute("UPDATE commitments SET amount = ? WHERE rowid = ?", (new_commitment_amount, commitment[0]))
                    conn.commit()
                    st.success(f"Commitment '{commitment[1]}' updated successfully.")

    if st.button("Save Profile"):
        # Insert profile data into the database
        c.execute("INSERT INTO profiles (username, salary, food_percentage, rent_percentage, utilities_percentage, miscellaneous_percentage) VALUES (?, ?, ?, ?, ?, ?)",
                  (st.session_state.username, salary, 0.40, 0.20, 0.10, 0.30))
        conn.commit()
        st.success("Profile completed successfully!")
