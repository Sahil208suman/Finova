
from .transaction import Transaction

class FinanceService:

    def __init__(self):
        self.transactions = []
        self.notifications = []

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

        if transaction.transaction_type.lower() == "expense":
            self.notifications.append(
                f"Expense added: {transaction.description} - ₹{transaction.amount}"
            )

        elif transaction.transaction_type.lower() == "income":
            self.notifications.append(
                f"Income added: {transaction.description} - ₹{transaction.amount}"
            )

    def get_transactions(self):
        return self.transactions

    def get_total_income(self):
        total = 0.0

        for transaction in self.transactions:
            if transaction.transaction_type.lower() == "income":
                total += transaction.amount

        return total

    def get_total_expenses(self):
        total = 0.0

        for transaction in self.transactions:
            if transaction.transaction_type.lower() == "expense":
                total += transaction.amount

        return total

    def get_balance(self):
        return self.get_total_income() - self.get_total_expenses()

    def get_notifications(self):
        return self.notifications

if __name__ == "__main__":
    finance_service = FinanceService()

    transaction = Transaction(
        description="Bought groceries",
        amount=500.0,
        transaction_type="Expense",
        category="Food"
    )

    finance_service.add_transaction(transaction)

    print("All Transactions:")
    print(finance_service.get_transactions())

    print("\nTotal Income:")
    print(finance_service.get_total_income())

    print("\nTotal Expenses:")
    print(finance_service.get_total_expenses())

    print("\nCurrent Balance:")
    print(finance_service.get_balance())

    print("\nNotifications:")
    print(finance_service.get_notifications())
    
