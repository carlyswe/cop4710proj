import csv
import mysql
import mysql.connector

def process_csv_file(file_path):
    # Establish a connection to the MySQL database
    db = mysql.connector.connect(
        host='db-newhomes.c9weqm4g04ms.us-east-2.rds.amazonaws.com',
        user='admin',
        password='cop4710!',
        database='realtorsite'
    )

    try:
        # Create a cursor object to execute SQL queries
        cursor = db.cursor()

        # Open the CSV file
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file)

            # Iterate over each row in the CSV file
            for row in csv_reader:
                try:
                    # Check for null or '#####' values and replace them with None
                    for key, value in row.items():
                        if value == '' or value == '#####':
                            row[key] = None

                    # Convert integer types to int or set to None if empty or invalid
                    beds = int(row['beds']) if row['beds'] else None
                    full_baths = int(row['full_baths']) if row['full_baths'] else None
                    half_baths = int(row['half_baths']) if row['half_baths'] else None
                    sqft = int(row['sqft']) if row['sqft'] else None
                    year_built = int(row['year_built']) if row['year_built'] else None
                    price = float(row['list_price']) if row['list_price'] else None

                    # Get the zip code from the row
                    zip_code = row['zip_code']

                    # Check if the zip code exists in the ZipCodes table
                    query = "SELECT COUNT(*) FROM ZipCodes WHERE ZipCode = %s"
                    cursor.execute(query, (zip_code,))
                    count = cursor.fetchone()[0]

                    if count == 0:
                        # Zip code does not exist, insert a new record into ZipCodes table
                        query = "INSERT INTO ZipCodes (ZipCode, City) VALUES (%s, %s)"
                        cursor.execute(query, (zip_code, row['city']))

                    # Prepare the SQL query to insert or update the home
                    query = """
                        INSERT INTO Homes (
                             ZipCode, property_url, style, street, unit, city,
                            beds, full_baths, half_baths, sqft, year_built, price, photo
                        )
                        VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                        ON DUPLICATE KEY UPDATE
                            ZipCode = VALUES(ZipCode), property_url = VALUES(property_url),
                            style = VALUES(style), street = VALUES(street), unit = VALUES(unit),
                            city = VALUES(city), beds = VALUES(beds), full_baths = VALUES(full_baths),
                            half_baths = VALUES(half_baths), sqft = VALUES(sqft),
                            year_built = VALUES(year_built), price = VALUES(price), photo = VALUES(photo)
                    """

                    # Execute the SQL query with the row data
                    cursor.execute(query, (
                        zip_code, row['property_url'], row['style'],
                        row['street'], row['unit'], row['city'], beds, full_baths,
                        half_baths, sqft, year_built, price, row['primary_photo']
                    ))

                    # Check if the home was inserted or updated
                    if cursor.rowcount == 1:
                        print(f"Home added: {row['property_url']}")
                    else:
                        print(f"Home updated (duplicate): {row['property_url']}")

                    # Commit the changes to the database
                    db.commit()

                except mysql.connector.Error as error:
                    if error.errno == 1264:  # Out of range value for column 'price'
                        print(f"Skipping row due to out of range value for 'price': {row['property_url']}")
                    else:
                        raise error



    except mysql.connector.Error as error:
        print(f"Error: {error}")
        db.rollback()  # Rollback the transaction if an error occurs

    finally:
        # Close the cursor and database connection
        if db.is_connected():
            cursor.close()
            db.close()

# Example usage
process_csv_file('/Users/carlysweeney/Downloads/dataloading/Data/forsale.csv')
process_csv_file('/Users/carlysweeney/Downloads/dataloading/Data/forrent.csv')