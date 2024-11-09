import streamlit as st
import plotly.graph_objects as go

# Function to Calculate Tax and Zakat with Interactive Plotly Chart
def calculate_zakat_tax(c):
    st.markdown(
        "<h2 style='color: #FF5733; font-weight: bold;'>Automated Tax and Zakat Calculator</h2>", 
        unsafe_allow_html=True
    )

    # Retrieve or enter salary
    if 'username' in st.session_state:
        c.execute("SELECT salary FROM profiles WHERE username = ?", (st.session_state.username,))
        salary = c.fetchone()[0]
    else:
        salary = None

    # Allow user to enter salary if it’s not retrieved
    if not salary:
        salary = st.number_input("Enter your monthly salary (RM):", min_value=0.0, format="%.2f")
    
    # Set fixed Zakat and Tax rates
    zakat_rate = 0.025  # 2.5%
    tax_rate = 0.10     # 10%

    if salary > 0:
        # Calculations
        zakat = salary * zakat_rate
        tax = salary * tax_rate
        remaining_salary = salary - zakat - tax
        
        # Display details
        st.markdown(
            f"<p style='color: #333333; font-size: 20px; font-weight: bold;'>Total Salary: RM {salary:.2f}</p>", 
            unsafe_allow_html=True
        )
        st.markdown(
            f"<p style='color: #333333; font-size: 20px; font-weight: bold;'>Zakat (2.5%): RM {zakat:.2f}</p>", 
            unsafe_allow_html=True
        )
        st.markdown(
            f"<p style='color: #333333; font-size: 20px; font-weight: bold;'>Estimated Tax (10%): RM {tax:.2f}</p>", 
            unsafe_allow_html=True
        )
        st.markdown(
            f"<p style='color: #333333; font-size: 20px; font-weight: bold;'>Remaining Salary after Deductions: RM {remaining_salary:.2f}</p>", 
            unsafe_allow_html=True
        )
        
        # Plot interactive donut chart with Plotly
        fig = go.Figure(data=[go.Pie(
            labels=['Zakat', 'Tax', 'Remaining Salary'],
            values=[zakat, tax, remaining_salary],
            hole=0.4,
            textinfo='label+percent',
            hovertemplate='%{label}: RM %{value:.2f} (%{percent})',
            marker=dict(colors=['#FF5733', '#FFC300', '#C0C0C0'], line=dict(color='#FFFFFF', width=2)),
            name=''  # Remove trace name to avoid "trace0" in hover
        )])

        fig.update_layout(
            title="Salary Distribution: Zakat, Tax, and Remaining Salary",
            annotations=[dict(text="Distribution", x=0.5, y=0.5, font_size=20, showarrow=False)],
            showlegend=True
        )
        
        # Display the plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)

# Usage example
# Assuming `c` is your database cursor
# calculate_zakat_tax(c)
