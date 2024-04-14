import sqlite3

# Connect to the database
conn = sqlite3.connect('QPC.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS properties')
# Create the properties table
cursor.execute('''
    CREATE TABLE properties (
        id INTEGER PRIMARY KEY,
        address1 TEXT,
        address2 TEXT,
        suburb TEXT,
        postcode TEXT,
        state TEXT,
        image TEXT,
        lat REAL,
        long REAL,
        description TEXT,
        price INTEGER,
        type TEXT,
        age INTEGER,
        bedrooms INTEGER,
        bathrooms INTEGER,
        carspace INTEGER,
        housearea INTEGER,
        landarea INTEGER,
        toilets INTEGER,
        pool INTEGER,
        airconditioning INTEGER,
        fenced INTEGER
    )
''')

# Insert records into the properties table
properties = [
    # sandgate regis lat long for testing
    (1, '123 Main St', '', 'Sandgate', '4017', 'QLD', 'DALLE2024-02-2420.49.59-1.webp', -27.3102, 153.0621, 'A quaint townhouse that combines simplicity with functionality, embodying affordable urban living. Perfect for commute to city, with weekends on the bay with low maintenance.', 850000, 'House', 10, 3, 2, 2, 200, 400, 2, 1, 1, 1),
    (2, '456 Elm St', '', 'Hendra', '4011', 'QLD', 'DALLE2024-02-2420.44.40-2.webp', -27.4192, 153.0737, 'A simple yet charming house featureing the classic Queenslander style, with corrugated iron roof and a wide front porch, surrounded by a well-kept garden. Movie in with nothing to do.', 600000, 'House', 17, 2, 1, 1, 100, 200, 1, 0, 1, 0),
    (3, '789 Oak St', '', 'Sunnybank', '4109', 'QLD', 'DALLE2024-02-2420.54.23-3.webp', -27.5800, 153.0606, 'A renovators delight small house nestled in friendly neighbourhood hlighting the community vibe and enhancement opportunities. Perfect for investor or DIY renovations.', 750000, 'House', 25, 4, 3, 2, 250, 500, 3, 1, 0, 1),
    (4, '321 Pine St', '', 'Clayfield', '4011', 'QLD', 'DALLE2024-02-2420.50.39-4.webp', -27.4195, 153.0584, 'A renovators dream. This home presents a fantastic opportunity for renovation in an amazing location. Building plans are already approved for the right investor or new home owner.', 1200000, 'Town House', 55, 5, 4, 3, 300, 600, 4, 1, 1, 1),
    (5, '654 Maple St', '', 'Newstead', '4006', 'QLD', 'DALLE2024-02-2420.43.31-5.webp', -27.4484, 153.0439, 'A stunning contemporary house that blends modern design with tropical elegence. The home featuers expansive glass walls, a flat roof, and an infinity pool, set against the view of Brisbanes urban backdrop.', 2500000, 'House', 3, 3, 2, 1, 450, 600, 2, 0, 1, 0),
    (6, '987 Birch St', '', 'Deagon', '4017', 'QLD', 'DALLE2024-02-2420.48.53-6.webp', -27.3271, 153.0619, 'A cozy, compact affordable home with a tin roof and wooden siding in a growing neighborhood. Alternatively perfect for development, full of potential.', 600000, 'House', 32, 3, 2, 2, 200, 400, 2, 1, 1, 1),
    (7, '135 Cedar St', '', 'Moorooka', '4105', 'QLD', 'DALLE2024-02-2420.43.07-7.webp', -27.5329, 153.0249, 'The beautiful statly home features a modern Queenslander style, known for its high ceiling, large verandas, and a tropical garden. Large gardens and pool perfect for entertaining.', 2000000, 'House', 20, 5, 3, 2, 700, 1000, 4, 1, 0, 1),
    (8, '246 Walnut St', '', 'Chandler', '4155', 'QLD', 'DALLE2024-02-2420.45.01-8.webp', -27.5140, 153.1564, 'A contemporary, multi-level townhouse in a vibrant neighbourhood with a combination of glass, steel, and wooden accents, featuring a small front yard and a cozy balcony.', 800000, 'Apartment', 5, 2, 1, 1, 100, 200, 1, 0, 1, 0),
    (9, '357 Ash St', '', 'Oxley', '4075', 'QLD', 'DALLE2024-02-2420.46.59-9.webp', -27.5531, 153.9739, 'An older, classic Queenslander house exuding vintage charm with its traditional high pitched tin roof, wrap-around verandas, and a mature garden. Perfect for investor or growing family.', 3000000, 'House', 65, 4, 3, 2, 250, 500, 3, 1, 0, 1),
    (10, '468 Oak St', '', 'Chermside West', '4032', 'QLD', 'DALLE2024-02-2420.41.35-10.webp', -27.3858, 153.0310, 'A modern two-bedroom house. The exterior is elegantly designed with a mix of wood, stone and glass materials, featuring large windows, a landscaped garden, in a serene neighborhood.', 950000, 'House', 5, 4, 2, 3, 300, 600, 4, 1, 1, 1),
    (11, '789 Gum St', '', 'Ascot', '4007', 'QLD', 'DALLE2024-02-2422.31.06-12.webp', -27.4307, 153.0621, 'A luxurious mansion with exquisite architectural design, featuring spacious rooms, high-end finishes, a grand entrance, and a beautifully landscaped garden.', 5000000, 'House', 9, 6, 5, 4, 800, 1200, 5, 1, 1, 1),
    (12, '79 Wattle St', '', 'Hamilton', '4007', 'QLD', 'DALLE2024-02-2420.51.19-11.webp', -27.4364, 153.0710, 'A charming small house, this quaint property offers a unique opportunity for refurbishment, with a simple layout and a somewhat neglected garden ready for inspiration.' , 1600000, 'House', 71, 6, 5, 4, 800, 1200, 5, 1, 1, 1),
    # wire owl coffee lat long for testing
    (13, '89 Bamboo St', '', 'Sandgate', '4017', 'QLD', 'DALLE2024-02-2520.44.22-13.webp', -27.3234, 153.0775, 'A charming Queenslander cottage shack. This quaint cottage embodies the essence of traditional Queensland architecture. First time on the market in 60 years.' , 1100000, 'House', 82, 3, 1, 1, 250, 500, 2, 0, 0, 0)

]


cursor.executemany('''
    INSERT INTO properties (
        id, address1, address2, suburb, postcode, state, image, lat, long, description, price, type, age, bedrooms, bathrooms, carspace, housearea, landarea, toilets, pool, airconditioning, fenced
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', properties)

# Commit the changes and close the connection
conn.commit()
conn.close()