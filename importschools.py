import csv
import sqlite3

# Open the CSV file
with open('data/schoolinfo.csv', 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)

    # Connect to the SQLite database
    conn = sqlite3.connect('QPC.db')
    cursor = conn.cursor()

    # drop old table if exists and create new table in the database
    cursor.execute('DROP TABLE IF EXISTS schools')
    cursor.execute('CREATE TABLE schools (id INTEGER PRIMARY KEY, name TEXT, suburb TEXT, latitude INTEGER, longitude INTEGER)')
    next(csv_reader) # skip the header row

    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Extract the data from the row
        id = row[0]
        name = row[2]
        suburb = row[18]
        latitude = row[38]
        longitude = row[37]

        # Insert the data into the database
        cursor.execute('INSERT INTO schools (id, name, suburb, latitude, longitude) VALUES (?, ?, ?, ?, ?)', (id, name, suburb, latitude, longitude))

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()