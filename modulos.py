class Transaction:
    def __init__(self, amount, category, date):
        self.amount = amount
        self.category = category
        self.date = date

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.income = []
        self.expenses = []

    def add_income(self, amount, source, date):
        self.income.append(Transaction(amount, source, date))

    def add_expense(self, amount, category, date):
        self.expenses.append(Transaction(amount, category, date))

    def get_total_income(self):
        return sum(transaction.amount for transaction in self.income)

    def get_total_expenses(self):
        return sum(transaction.amount for transaction in self.expenses)

    def generate_report(self):
        total_income = self.get_total_income()
        total_expenses = self.get_total_expenses()
        balance = total_income - total_expenses
        return total_income, total_expenses, balance
