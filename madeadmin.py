import sqlite3
conn = sqlite3.connect('QPC.db')
cursor = conn.cursor()
query = "UPDATE users SET is_admin = TRUE WHERE email = 'johnsmith@gmail.com'"
cursor.execute(query)
conn.commit()
cursor.close()
conn.close()



