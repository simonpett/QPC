import sqlite3
import csv

# Open the CSV file
with open('data/busstopinfo.csv', 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)

    # Connect to the SQLite database
    conn = sqlite3.connect('QPC.db')
    cursor = conn.cursor()

    # drop old table if exists and create new table in the database
    cursor.execute('DROP TABLE IF EXISTS bus_stops')
    cursor.execute('CREATE TABLE bus_stops (id INTEGER PRIMARY KEY, bus_stop_number INTEGER, name TEXT, suburb TEXT, latitude INTEGER, longitude INTEGER)')
    next(csv_reader) # skip the header row

    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Extract the data from the row
        id = row[0]
        bus_stop_number = row[2]
        name = row[3]
        suburb = row[10]
        latitude = row[8]
        longitude = row[9]

        # Insert the data into the database
        cursor.execute('INSERT INTO bus_stops (id, bus_stop_number, name, suburb, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)', (id, bus_stop_number, name, suburb, latitude, longitude))

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()