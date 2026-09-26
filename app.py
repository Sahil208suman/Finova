import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.data.data_manager import load_transactions, save_transaction


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Finova",
    page_icon="💰",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("💰 Finova")
st.subheader("AI-Powered Personal Finance Assistant")

st.write(
    "Track your finances, analyze spending patterns, "
    "and make smarter financial decisions."
)


# --------------------------------------------------
# LOAD TRANSACTIONS
# --------------------------------------------------

if "transactions" not in st.session_state:
    st.session_state.transactions = load_transactions()


# --------------------------------------------------
# ADD TRANSACTION
# --------------------------------------------------

st.header("➕ Add Transaction")

col1, col2 = st.columns(2)

with col1:
    description = st.text_input(
        "Description",
        placeholder="e.g. Salary, Grocery, Rent"
    )

    amount = st.number_input(
        "Amount",
        min_value=0.0,
        step=100.0,
        format="%.2f"
    )


with col2:
    transaction_type = st.selectbox(
        "Transaction Type",
        ["Income", "Expense"]
    )

    if transaction_type == "Income":
        categories = [
            "Salary",
            "Business",
            "Investment",
            "Other"
        ]
    else:
        categories = [
            "Food",
            "Rent",
            "Transport",
            "Shopping",
            "Bills",
            "Entertainment",
            "Health",
            "Other"
        ]

    category = st.selectbox(
        "Category",
        categories
    )


# --------------------------------------------------
# SAVE TRANSACTION
# --------------------------------------------------

if st.button("💾 Save Transaction", type="primary"):

    if description.strip() == "":
        st.warning("Please enter a description.")

    elif amount <= 0:
        st.warning("Please enter an amount greater than 0.")

    else:
        st.session_state.transactions = save_transaction(
            description,
            amount,
            transaction_type,
            category
        )

        st.success("✅ Transaction saved successfully!")


# --------------------------------------------------
# FINANCIAL SUMMARY
# --------------------------------------------------

st.header("📊 Financial Summary")

df = st.session_state.transactions


if not df.empty:

    # Calculate income
    income = df.loc[
        df["Type"].str.lower() == "income",
        "Amount"
    ].sum()

    # Calculate expenses
    expenses = df.loc[
        df["Type"].str.lower() == "expense",
        "Amount"
    ].sum()

    # Calculate savings
    savings = income - expenses

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💵 Total Income",
            f"₹{income:,.2f}"
        )

    with col2:
        st.metric(
            "💸 Total Expenses",
            f"₹{expenses:,.2f}"
        )

    with col3:
        st.metric(
            "🏦 Savings",
            f"₹{savings:,.2f}"
        )

else:

    st.info("No transactions available yet.")


# --------------------------------------------------
# TRANSACTION HISTORY
# --------------------------------------------------

st.header("📋 Transaction History")

if not df.empty:
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No transactions found.")


# --------------------------------------------------
# DAY 5 - SPENDING ANALYSIS
# --------------------------------------------------

st.header("📈 Spending Analysis")

if not df.empty:

    # Select only expenses
    expenses_df = df[
        df["Type"].str.lower() == "expense"
    ]

    if not expenses_df.empty:

        # Group expenses by category
        category_spending = (
            expenses_df
            .groupby("Category")["Amount"]
            .sum()
            .sort_values(ascending=False)
        )

        st.subheader("💸 Spending by Category")

        # Display table
        spending_table = category_spending.reset_index()

        spending_table.columns = [
            "Category",
            "Amount"
        ]

        st.dataframe(
            spending_table,
            use_container_width=True,
            hide_index=True
        )

        # Create chart
        fig, ax = plt.subplots()

        category_spending.plot(
            kind="bar",
            ax=ax
        )

        ax.set_title("Spending by Category")
        ax.set_xlabel("Category")
        ax.set_ylabel("Amount (₹)")

        plt.xticks(rotation=45)

        st.pyplot(fig)

        # Highest spending category
        highest_category = category_spending.idxmax()
        highest_amount = category_spending.max()

        st.info(
            f"💡 Your highest spending category is "
            f"**{highest_category}** with "
            f"**₹{highest_amount:,.2f}**."
        )

    else:
        st.info(
            "No expenses available yet. "
            "Add an Expense transaction to see spending analysis."
        )

else:

    st.info(
        "Add some transactions to see your spending analysis."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption("Finova — Your personal finance assistant 💰")
