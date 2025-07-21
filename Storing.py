import json
import sqlite3



def database_setup():
    conn = sqlite3.connect('Spendings.db')
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                category TEXT,
                amount REAL,
                description TEXT
                )''')
    conn.commit()
    conn.close()





# def save_to_json(expense_data):
#     """Save to JSON file - FREE storage option"""
#     filename = "expenses.json"
#
#     try:
#         with open(filename, 'r') as f:
#             expenses = json.load(f)
#     except FileNotFoundError:
#         expenses = []
#
#     expenses.append(expense_data)
#
#     with open(filename, 'w') as f:
#         json.dump(expenses, f, indent=2)