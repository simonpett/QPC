import sqlite3

# Create a connection to the database
conn = sqlite3.connect('QPC.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create the properties table
cursor.execute('''
    CREATE TABLE properties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT,
        image TEXT,
        suburb TEXT,
        price REAL,
        bedrooms INTEGER,
        bathrooms INTEGER,
        garages INTEGER,
        latitude INTEGER,
        longitude INTEGER
    )
''')

# Insert some test data into the properties table
properties = [
    ('123 Main St', 'image1.jpg', 'Suburb1', 100000, 2, 1, 1, 40.7128, -74.0060),
    ('456 Elm St', 'image2.jpg', 'Suburb2', 200000, 3, 2, 2, 34.0522, -118.2437),
    ('789 Oak St', 'image3.jpg', 'Suburb3', 300000, 4, 3, 2, 51.5074, -0.1278)
]

cursor.executemany('''
    INSERT INTO properties (address, image, suburb, price, bedrooms, bathrooms, garages, latitude, longitude)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', properties)

# Commit the changes and close the connection
conn.commit()
conn.close()