import streamlit as st
import pandas as pd
from db import init_db, add_expense, view_expenses

# Initialize database
init_db()

st.set_page_config(page_title="Personal Expense Tracker", page_icon="💰", layout="centered")

st.title("💰 Personal Expense Tracker")

# Sidebar for navigation
menu = ["Add Expense", "View Expenses"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Expense":
    st.subheader("Add a New Expense")
    
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Other"])
    amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
    description = st.text_area("Description")

    if st.button("Add Expense"):
        add_expense(str(date), category, amount, description)
        st.success("Expense added successfully!")

elif choice == "View Expenses":
    st.subheader("All Expenses")
    data = view_expenses()
    
    if data:
        df = pd.DataFrame(data, columns=["ID", "Date", "Category", "Amount", "Description"])
        st.dataframe(df)

        # Summary
        total_amount = df["Amount"].sum()
        st.write(f"### Total Spent: ₹{total_amount:.2f}")

        # Pie chart - expenses by category
        st.subheader("Expenses by Category")
        category_summary = df.groupby("Category")["Amount"].sum()
        st.bar_chart(category_summary)  # You can change to pie chart below

        # Monthly summary
        st.subheader("Monthly Summary")
        df["Date"] = pd.to_datetime(df["Date"])
        df["Month"] = df["Date"].dt.to_period("M")
        monthly_summary = df.groupby("Month")["Amount"].sum()
        st.line_chart(monthly_summary)

        # Download CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "expenses.csv", "text/csv")
    else:
        st.warning("No expenses found.")

