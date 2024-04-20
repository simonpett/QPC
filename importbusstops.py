import sqlite3
import csv
# open the bus stop data from the CSV file and insert it into the SQLite database
with open('data/busstopinfo.csv', 'r') as file:     # Open the CSV file in read mode
    csv_reader = csv.reader(file)                   # Create a CSV reader object
    conn = sqlite3.connect('QPC.db')                # Connect to the SQLite database
    cursor = conn.cursor()                          # Create a cursor object
    cursor.execute('DROP TABLE IF EXISTS bus_stops') # drop old table if exists and create new table in the database
    cursor.execute('''CREATE TABLE bus_stops (id INTEGER PRIMARY KEY, bus_stop_number INTEGER, name TEXT, suburb TEXT, 
                    latitude INTEGER, longitude INTEGER)''')
    next(csv_reader)                                # skip the header row
    for row in csv_reader:                          # Iterate over each row in the CSV file and insert the data into the database
        cursor.execute('INSERT INTO bus_stops (id, bus_stop_number, name, suburb, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)',
                       (row[0], row[2], row[3], row[10], row[8], row[9]))
    conn.commit()                                   # Commit the changes and close the database connection
    conn.close()                                    # Close the database connection