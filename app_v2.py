from flask import Flask, render_template, request, redirect, url_for, session
from expense_manager import ExpenseManager
import numpy as np

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a real secret key in production


def get_manager():
    friends = session.get('friends', [])
    expenses = session.get('expenses', [])
    manager = ExpenseManager(friends)
    for expense in expenses:
        manager.add_expense(expense['payer'], expense['beneficiaries'], expense['amount'])
    return manager


@app.route('/')
def index():
    if 'friends' not in session:
        session['friends'] = []
    if 'expenses' not in session:
        session['expenses'] = []
    return render_template('index2.html', friends=session['friends'])


@app.route('/add_friend', methods=['POST'])
def add_friend():
    friend_name = request.form['friend_name']
    if friend_name and friend_name not in session['friends']:
        session['friends'].append(friend_name)
        session.modified = True
    return redirect(url_for('index'))


@app.route('/add_expense', methods=['POST'])
def add_expense():
    payer = request.form['payer']
    amount = float(request.form['amount'])
    beneficiaries = request.form.getlist('beneficiaries')

    expense = {
        'payer': payer,
        'amount': amount,
        'beneficiaries': beneficiaries
    }

    session['expenses'].append(expense)
    session.modified = True
    return redirect(url_for('index'))


@app.route('/settlements')
def settlements():
    manager = get_manager()
    settlements_table = manager.display_settlements()
    settlements = manager.calculate_settlements()
    return render_template('settlements.html', friends=session['friends'], settlements=settlements,
                           settlements_table=settlements_table)


@app.route('/suggested_payments')
def suggested_payments():
    manager = get_manager()
    transactions = manager.suggest_payments()
    return render_template('suggested_payments.html', transactions=transactions)


if __name__ == '__main__':
    app.run(debug=True)