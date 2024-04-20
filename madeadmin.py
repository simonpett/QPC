import sqlite3  # make a user an admin, change email to the email of the user you want to make an admin
conn = sqlite3.connect('QPC.db')    # Connect to the SQLite database
cursor = conn.cursor()              # Create a cursor object and then execute the sql to make the user an admin
cursor.execute("UPDATE users SET is_admin = TRUE WHERE email = 'johnsmith@gmail.com'")               
conn.commit()                       # Commit the changes and close the database connection
cursor.close()                      # Close the cursor
conn.close()                        # Close the database connection



