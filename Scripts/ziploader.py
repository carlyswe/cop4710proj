import csv
import mysql.connector

# Establish a connection to the MySQL server
connection = mysql.connector.connect(
        host='db-newhomes.c9weqm4g04ms.usa-east-2.rds.amazonaws.com',
        user='admin',
        password='cop4710!',
        database='realtorsite'
    )

# Create a cursor object to execute queries
cursor = connection.cursor()

# Open the CSV file
with open(r'C:\Users\dunlo\PycharmProjects\realestateproj\datatbl\flzips.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row

    # Iterate over each row in the CSV file
    for row in csv_reader:
        zip_code = row[0].strip()[:5]  # Truncate zip code to first 5 characters
        city = row[2].strip()
        county = row[4].strip()

        # Skip rows with empty, blank, or non-numeric zip codes
        if not zip_code or not zip_code.isdigit():
            continue

        # Check if the zip code already exists in the database
        query = "SELECT COUNT(*) FROM ZipCodes WHERE ZipCode = %s"
        cursor.execute(query, (zip_code,))
        count = cursor.fetchone()[0]

        if count > 0:
            # Zip code already exists, skip the insertion
            continue

        # Prepare the SQL INSERT statement
        query = "INSERT INTO ZipCodes (ZipCode, City, County) VALUES (%s, %s, %s)"

        try:
            # Execute the INSERT statement
            cursor.execute(query, (zip_code, city, county))
        except mysql.connector.errors.DatabaseError as err:
            print(f"Error inserting record: {err}")
            continue

# Commit the changes and close the cursor and connection
connection.commit()
cursor.close()
connection.close()