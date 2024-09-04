from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = 'data/finance_data.json'

# Load existing data from JSON
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"months": {}, "expenses": {}}

# Save data back to JSON
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', data=data)

@app.route('/update', methods=['POST'])
def update_data():
    data = load_data()

    # Get form data
    month = request.form.get('month')
    goal = request.form.get('goal')
    result = request.form.get('result')
    date = request.form.get('date')
    balance = request.form.get('balance')

    # Update the month data
    data["months"][month] = {
        "goal": goal,
        "result": result,
        "date": date,
        "balance": balance
    }

    # Save updated data
    save_data(data)

    return redirect(url_for('index'))

@app.route('/edit_month/<month>', methods=['GET', 'POST'])
def edit_month(month):
    data = load_data()
    if request.method == 'POST':
        # Get updated form data
        goal = request.form.get('goal')
        result = request.form.get('result')
        date = request.form.get('date')
        balance = request.form.get('balance')

        # Update the month data
        data["months"][month] = {
            "goal": goal,
            "result": result,
            "date": date,
            "balance": balance
        }
        save_data(data)
        return redirect(url_for('index'))

    # Pre-fill form with existing data
    return render_template('edit_month.html', month=month, details=data["months"][month])

@app.route('/edit_expense/<category>', methods=['GET', 'POST'])
def edit_expense(category):
    data = load_data()
    if request.method == 'POST':
        # Get updated form data
        amount = request.form.get('amount')

        # Update the expense data
        data["expenses"][category] = amount
        save_data(data)
        return redirect(url_for('index'))

    # Pre-fill form with existing data
    return render_template('edit_expense.html', category=category, amount=data["expenses"][category])

@app.route('/remove_month/<month>', methods=['POST'])
def remove_month(month):
    data = load_data()
    if month in data['months']:
        del data['months'][month]
        save_data(data)
    return redirect(url_for('index'))

@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = load_data()

    # Get form data for new expense
    category = request.form.get('category')
    amount = request.form.get('amount')

    # Add to expenses
    data["expenses"][category] = amount

    # Save updated data
    save_data(data)

    return redirect(url_for('index'))

@app.route('/remove_expense/<category>', methods=['POST'])
def remove_expense(category):
    data = load_data()
    if category in data['expenses']:
        del data['expenses'][category]
        save_data(data)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5025)
