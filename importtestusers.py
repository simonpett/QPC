import sqlite3

# Connect to the database
conn = sqlite3.connect('QPC.db')
c = conn.cursor()
c.execute('drop table if exists users')

# Create the user table
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        occupation TEXT,
        email TEXT,
        password TEXT,
        businessname TEXT,
        is_admin BOOLEAN DEFAULT 0
    )
''')

# Insert test data rows
test_data = [
    ('John', 'Doe', 'Engineer', 'john.doe@example.com', 'password123', 'ABC Company'),
    ('Jane', 'Smith', 'Designer', 'jane.smith@example.com', 'password456', 'XYZ Corporation'),
    ('Mike', 'Johnson', 'Manager', 'mike.johnson@example.com', 'password789', '123 Industries')
]
c.executemany('INSERT INTO users (first_name, last_name, occupation, email, password, businessname) VALUES (?, ?, ?, ?, ?, ?)', test_data)

# Commit the changes and close the connection
conn.commit()
conn.close()


