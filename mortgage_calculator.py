import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("🏠 Indian Home Loan EMI Calculator")

home_value = st.number_input("Property Cost (₹)", min_value=0, value=5000000)

st.write("### Enter Loan Details")
col1, col2 = st.columns(2)

deposit = col1.number_input("Down Payment (₹)", min_value=0, value=1000000)

# Sliders for Interest Rate and Loan Tenure
interest_rate_slider = st.slider("Select Interest Rate (Annual %)", min_value=0.0, max_value=15.0, value=7.5, step=0.1)
loan_term_slider = st.slider("Select Loan Tenure (Years)", min_value=1, max_value=30, value=20)

# Calculate the repayments.
loan_amount = home_value - deposit
monthly_interest_rate = (interest_rate_slider / 100) / 12
number_of_payments = loan_term_slider * 12
monthly_payment = (
    loan_amount
    * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
    / ((1 + monthly_interest_rate) ** number_of_payments - 1)
)

# Display the repayments.
total_payments = monthly_payment * number_of_payments
total_interest = total_payments - loan_amount

st.write("### Repayments")
col1, col2, col3 = st.columns(3)
col1.metric(label="Monthly Repayments", value=f"₹{monthly_payment:,.2f}")
col2.metric(label="Total Repayments", value=f"₹{total_payments:,.0f}")
col3.metric(label="Total Interest", value=f"₹{total_interest:,.0f}")

# Create a data-frame with the payment schedule.
schedule = []
remaining_balance = loan_amount

for i in range(1, number_of_payments + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i / 12)  # Calculate the year into the loan
    schedule.append(
        [
            i,
            monthly_payment,
            principal_payment,
            interest_payment,
            remaining_balance,
            year,
        ]
    )

df = pd.DataFrame(
    schedule,
    columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"],
)

# Display the Payment Schedule as a Table (Amortization Schedule)
st.write("### Payment Schedule (Amortization Schedule)")
st.dataframe(df)  # Display the amortization schedule as a table

# Show loan repayment progress
repayment_progress = (loan_amount - remaining_balance) / loan_amount
st.progress(repayment_progress)  # Visualize loan repayment progress as a bar

# Display the data-frame as a chart.
st.write("### Payment Schedule Chart")
payments_df = df[["Year", "Remaining Balance"]].groupby("Year").min()
st.line_chart(payments_df)
