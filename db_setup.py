import sqlite3

# Database Setup
conn = sqlite3.connect('moneyminder.db', check_same_thread=False)
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY, password TEXT, first_name TEXT, last_name TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS profiles
             (username TEXT PRIMARY KEY, salary REAL, food_percentage REAL, rent_percentage REAL, utilities_percentage REAL, miscellaneous_percentage REAL, FOREIGN KEY(username) REFERENCES users(username))''')
c.execute('''CREATE TABLE IF NOT EXISTS commitments
             (username TEXT, commitment_name TEXT, amount REAL, FOREIGN KEY(username) REFERENCES users(username))''')
c.execute('''CREATE TABLE IF NOT EXISTS expenses
             (username TEXT, expense_name TEXT, category TEXT, amount REAL, FOREIGN KEY(username) REFERENCES users(username))''')
c.execute('''CREATE TABLE IF NOT EXISTS investments (
             investment_id INTEGER PRIMARY KEY AUTOINCREMENT, 
             username TEXT NOT NULL, 
             amount REAL CHECK(amount >= 0), 
             FOREIGN KEY(username) REFERENCES users(username) ON DELETE CASCADE)''')


conn.commit()
