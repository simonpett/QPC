import csv
import sqlite3
# open the government school data from the CSV file and insert it into the SQLite database
with open('data/schoolinfo.csv', 'r') as file:      # Open the CSV file in read mode    
    csv_reader = csv.reader(file)                   # Create a CSV reader object
    conn = sqlite3.connect('QPC.db')                # Connect to the SQLite database
    cursor = conn.cursor()                          # Create a cursor object
    cursor.execute('DROP TABLE IF EXISTS schools')  # drop old table if exists and create new table in the database
    cursor.execute('CREATE TABLE schools (id INTEGER PRIMARY KEY, name TEXT, suburb TEXT, latitude INTEGER, longitude INTEGER)')
    next(csv_reader)                                # skip the header row
    for row in csv_reader:                          # Iterate over each row in the CSV file and insert the data into the database
        cursor.execute('INSERT INTO schools (id, name, suburb, latitude, longitude) VALUES (?, ?, ?, ?, ?)', 
                       (row[0], row[2], row[18], row[38], row[37]))
    conn.commit()                                   # Commit the changes and close the database connection
    conn.close()                                    # Close the database connection