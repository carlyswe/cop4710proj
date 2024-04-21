import csv
import mysql.connector

def process_csv_file(file_path):
    db = mysql.connector.connect(
        host='db-newhomes.c9weqm4g04ms.us-east-2.rds.amazonaws.com',
        user='admin',
        password='cop4710!',
        database='realtorsite'
    )

    try:
        cursor = db.cursor()
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                try:
                    # Handle null or placeholder values
                    for key, value in row.items():
                        if value == '' or value == '#####':
                            row[key] = None

                    # Convert data types
                    beds = int(row['beds']) if row['beds'] else None
                    status = row['status'] 
                    full_baths = int(row['full_baths']) if row['full_baths'] else None
                    half_baths = int(row['half_baths']) if row['half_baths'] else None
                    sqft = int(row['sqft']) if row['sqft'] else None
                    year_built = int(row['year_built']) if row['year_built'] else None
                    price = float(row['list_price']) if row['list_price'] else None
                    latitude = float(row['latitude']) if row['latitude'] else None
                    longitude = float(row['longitude']) if row['longitude'] else None
                    zip_code = row['zip_code']

                    # Ensure the zip code exists in the database
                    query = "SELECT COUNT(*) FROM ZipCodes WHERE ZipCode = %s"
                    cursor.execute(query, (zip_code,))
                    if cursor.fetchone()[0] == 0:
                        query = "INSERT INTO ZipCodes (ZipCode, City) VALUES (%s, %s)"
                        cursor.execute(query, (zip_code, row['city']))

                    # Insert home data into Homes table
                    query = """
                        INSERT INTO Homes (
                            ZipCode, property_url, status, style, street, unit, city,
                            beds, full_baths, half_baths, sqft, year_built, price, photo,
                            latitude, longitude
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                    """
                    cursor.execute(query, (
                        zip_code, row['status'], row['property_url'], row['style'], row['street'], row['unit'],
                        row['city'], beds, full_baths, half_baths, sqft, year_built, price,
                        row['primary_photo'], latitude, longitude
                    ))

                    print(f"Home added: {row['property_url']}")
                    db.commit()

                except mysql.connector.Error as error:
                    print(f"Error processing row: {error}")
                    db.rollback()

    except mysql.connector.Error as error:
        print(f"Error establishing database connection or cursor: {error}")

    finally:
        if db.is_connected():
            cursor.close()
            db.close()

# Example usageßß
process_csv_file(r'/Users/adelinebelova/Data/forsaleupdated.csv')