import csv
import sqlite3

with open('data/schoolinfo.csv', 'r') as file:
    csv_reader = csv.reader(file)

    conn = sqlite3.connect('QPC.db')
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS schools')
    cursor.execute('CREATE TABLE schools (id INTEGER PRIMARY KEY, name TEXT, suburb TEXT, latitude INTEGER, longitude INTEGER)')
    next(csv_reader) # skip the header row

    for row in csv_reader:
        id = row[0]
        name = row[2]
        suburb = row[18]
        latitude = row[38]
        longitude = row[37]

        cursor.execute('INSERT INTO schools (id, name, suburb, latitude, longitude) VALUES (?, ?, ?, ?, ?)', (id, name, suburb, latitude, longitude))

    conn.commit()
    conn.close()