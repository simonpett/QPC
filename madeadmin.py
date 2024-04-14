import sqlite3
# Connect to the database
conn = sqlite3.connect('QPC.db')
# Create a cursor object to interact with the database
cursor = conn.cursor()

# Update the users table
query = "UPDATE users SET is_admin = TRUE WHERE email = 'johnsmith@gmail.com'"

# Execute the query
cursor.execute(query)

# Commit the changes to the database
conn.commit()

# Close the cursor and database connection
cursor.close()
conn.close()