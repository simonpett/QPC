import sqlite3
# create a set of test users and insert them into the SQLite database
conn = sqlite3.connect('QPC.db')            # Connect to the SQLite database
c = conn.cursor()                           # Create a cursor object
c.execute('drop table if exists users')     # drop old table if exists and create new table in the database
c.execute('''
    CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT, occupation TEXT, email TEXT,
                password TEXT, businessname TEXT, is_admin BOOLEAN DEFAULT 0)''')
# create a list of test users
test_data = [
    ('John', 'Doe', 'Engineer', 'john.doe@example.com', 'password123', 'ABC Company'),
    ('Jane', 'Smith', 'Designer', 'jane.smith@example.com', 'password456', 'XYZ Corporation'),
    ('Mike', 'Johnson', 'Manager', 'mike.johnson@example.com', 'password789', '123 Industries')
]  # insert the test users
c.executemany('INSERT INTO users (first_name, last_name, occupation, email, password, businessname) VALUES (?, ?, ?, ?, ?, ?)', test_data)
conn.commit()                               # Commit the changes and close the database connection
conn.close()                                # Close the database connection


