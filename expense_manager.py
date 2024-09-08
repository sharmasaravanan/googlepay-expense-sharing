import numpy as np
from prettytable import PrettyTable


class ExpenseManager:
    def __init__(self, friends):
        self.friends = friends
        self.expense_matrix = np.zeros((len(friends), len(friends)))  # Rows: Who paid, Columns: Who it's for

    def add_expense(self, payer, beneficiaries, amount):
        payer_idx = self.friends.index(payer)
        share_per_person = amount / len(beneficiaries)
        for beneficiary in beneficiaries:
            beneficiary_idx = self.friends.index(beneficiary)
            self.expense_matrix[payer_idx][beneficiary_idx] += share_per_person

    def calculate_settlements(self):
        total_paid = np.sum(self.expense_matrix, axis=1)  # How much each person paid
        total_owed = np.sum(self.expense_matrix, axis=0)  # How much each person owes
        net_balance = total_paid - total_owed  # Positive: person should receive, Negative: person owes
        return net_balance

    def display_settlements(self):
        settlements = self.calculate_settlements()
        table = PrettyTable()
        table.field_names = ["Friend", "Settlement"]
        for i, friend in enumerate(self.friends):
            if settlements[i] > 0:
                table.add_row([friend, f"Should Receive ₹{settlements[i]:.2f}"])
            elif settlements[i] < 0:
                table.add_row([friend, f"Owes ₹{-settlements[i]:.2f}"])
            else:
                table.add_row([friend, "Is Settled"])
        return table

    def suggest_payments(self):
        settlements = self.calculate_settlements()
        creditors = [(self.friends[i], amt) for i, amt in enumerate(settlements) if amt > 0]
        debtors = [(self.friends[i], -amt) for i, amt in enumerate(settlements) if amt < 0]
        transactions = []

        while debtors and creditors:
            debtor, debt_amount = debtors.pop(0)
            creditor, credit_amount = creditors.pop(0)
            payment = min(debt_amount, credit_amount)
            transactions.append((debtor, creditor, payment))

            debt_amount -= payment
            credit_amount -= payment

            if debt_amount > 0:
                debtors.insert(0, (debtor, debt_amount))
            if credit_amount > 0:
                creditors.insert(0, (creditor, credit_amount))

        return transactions