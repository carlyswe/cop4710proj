import csv
import json
import mysql.connector
import datetime

def process_csv_file(file_path):
    # Establish a connection to the MySQL database
    db = mysql.connector.connect(
        host='',
        user='',
        password='',
        database=''
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

                    # Split the alternate photos into a list
                    alt_photos = row['alt_photos'].split(', ') if row['alt_photos'] else []

                    # Convert decimal types to float or set to None if empty or invalid
                    list_price = float(row['list_price']) if row['list_price'] else None
                    sold_price = None
                    if row['sold_price']:
                        try:
                            sold_price = float(row['sold_price'])
                            if sold_price < 0 or sold_price > 9999999999.99:
                                raise ValueError("Sold price out of range")
                        except (ValueError, TypeError):
                            print(f"Invalid sold price value: {row['sold_price']}. Setting to None.")
                            sold_price = None
                    price_per_sqft = float(row['price_per_sqft']) if row['price_per_sqft'] else None
                    latitude = float(row['latitude']) if row['latitude'] else None
                    longitude = float(row['longitude']) if row['longitude'] else None
                    hoa_fee = float(row['hoa_fee']) if row['hoa_fee'] else None

                    # Convert integer types to int or set to None if empty or invalid
                    beds = int(row['beds']) if row['beds'] else None
                    full_baths = int(row['full_baths']) if row['full_baths'] else None
                    half_baths = int(row['half_baths']) if row['half_baths'] else None
                    sqft = int(row['sqft']) if row['sqft'] else None
                    year_built = int(row['year_built']) if row['year_built'] else None
                    days_on_mls = int(row['days_on_mls']) if row['days_on_mls'] else None
                    lot_sqft = int(row['lot_sqft']) if row['lot_sqft'] else None
                    stories = int(row['stories']) if row['stories'] else None

                    # Convert date types to datetime.date or set to None if empty or invalid
                    try:
                        list_date = datetime.datetime.strptime(row['list_date'], '%Y-%m-%d').date() if row['list_date'] else None
                    except ValueError:
                        try:
                            list_date = datetime.datetime.strptime(row['list_date'], '%m/%d/%Y').date() if row['list_date'] else None
                        except ValueError:
                            list_date = None

                    try:
                        last_sold_date = datetime.datetime.strptime(row['last_sold_date'], '%Y-%m-%d').date() if row['last_sold_date'] else None
                    except ValueError:
                        try:
                            last_sold_date = datetime.datetime.strptime(row['last_sold_date'], '%m/%d/%Y').date() if row['last_sold_date'] else None
                        except ValueError:
                            last_sold_date = None

                    # Prepare the SQL query to insert or update the listing
                    query = """
                        INSERT INTO Listings (
                            property_url, mls, mls_id, status, style, street, unit, city, state, zip_code,
                            beds, full_baths, half_baths, sqft, year_built, days_on_mls, list_price,
                            list_date, sold_price, last_sold_date, lot_sqft, price_per_sqft, latitude,
                            longitude, stories, hoa_fee, parking_garage, primary_photo, alt_photos
                        )
                        VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                        ON DUPLICATE KEY UPDATE
                            property_url = VALUES(property_url), mls = VALUES(mls), mls_id = VALUES(mls_id),
                            status = VALUES(status), style = VALUES(style), street = VALUES(street),
                            unit = VALUES(unit), city = VALUES(city), state = VALUES(state),
                            zip_code = VALUES(zip_code), beds = VALUES(beds), full_baths = VALUES(full_baths),
                            half_baths = VALUES(half_baths), sqft = VALUES(sqft), year_built = VALUES(year_built),
                            days_on_mls = VALUES(days_on_mls), list_price = VALUES(list_price),
                            list_date = VALUES(list_date), sold_price = VALUES(sold_price),
                            last_sold_date = VALUES(last_sold_date), lot_sqft = VALUES(lot_sqft),
                            price_per_sqft = VALUES(price_per_sqft), latitude = VALUES(latitude),
                            longitude = VALUES(longitude), stories = VALUES(stories), hoa_fee = VALUES(hoa_fee),
                            parking_garage = VALUES(parking_garage), primary_photo = VALUES(primary_photo),
                            alt_photos = VALUES(alt_photos)
                    """

                    # Execute the SQL query with the row data
                    cursor.execute(query, (
                        row['property_url'], row['mls'], row['mls_id'], row['status'], row['style'],
                        row['street'], row['unit'], row['city'], row['state'], row['zip_code'],
                        beds, full_baths, half_baths, sqft, year_built, days_on_mls, list_price,
                        list_date, sold_price, last_sold_date, lot_sqft, price_per_sqft,
                        latitude, longitude, stories, hoa_fee, row['parking_garage'],
                        row['primary_photo'], json.dumps(alt_photos)
                    ))

                    # Check if the listing was inserted or updated
                    if cursor.rowcount == 1:
                        print(f"Listing added: {row['property_url']}")
                    else:
                        print(f"Listing updated (duplicate): {row['property_url']}")

                except mysql.connector.Error as error:
                    if error.errno == 1264:  # Out of range value for column 'sold_price'
                        print(f"Skipping row due to out of range value for 'sold_price': {row['property_url']}")
                    else:
                        raise error

        # Commit the changes to the database
        db.commit()

    except mysql.connector.Error as error:
        print(f"Error: {error}")
        db.rollback()  # Rollback the transaction if an error occurs

    finally:
        # Close the cursor and database connection
        if db.is_connected():
            cursor.close()
            db.close()



# Example usage
process_csv_file(r'C:\Users\dunlo\PycharmProjects\realestateproj\scripts\HomeHarvest_Florida_20240327_232001_forsale.csv')
process_csv_file(r'C:\Users\dunlo\PycharmProjects\realestateproj\scripts\HomeHarvest_Florida_20240327_213248_forrent.csv')