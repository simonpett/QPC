import sqlite3  # make user an admin, change email to the value of the user you want to make admin
conn = sqlite3.connect('QPC.db') # Connect to the SQLite database, then create the cursor
cursor = conn.cursor()           # below - execute the sql to make the user an admin
cursor.execute("UPDATE users SET is_admin = TRUE WHERE email = 'johnsmith@gmail.com'")               
conn.commit()                    # Commit the changes and close the database connection
cursor.close()                   # Close the cursor
conn.close()                     # Close the database connection



