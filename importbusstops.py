import sqlite3
import csv

# Open the CSV file
with open('data/busstopinfo.csv', 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)

    # Connect to the SQLite database
    conn = sqlite3.connect('QPC.db')
    cursor = conn.cursor()

    # Create a table in the database
    cursor.execute('DROP TABLE IF EXISTS bus_stops')
    cursor.execute('CREATE TABLE bus_stops (id INTEGER PRIMARY KEY, name TEXT, suburb TEXT, latitude INTEGER, longitude INTEGER)')

    next(csv_reader)

    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Extract the data from the row
        id = row[0]
        name = row[2]
        suburb = row[10]
        latitude = row[8]
        longitude = row[9]

        # Insert the data into the database
        cursor.execute('INSERT INTO bus_stops (id, name, suburb, latitude, longitude) VALUES (?, ?, ?, ?, ?)', (id, name, suburb, latitude, longitude))

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()