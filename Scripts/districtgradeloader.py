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
with open(r'C:\Users\dunlo\PycharmProjects\realestateproj\datatbl\districtgrades.csv', 'r') as file:
    csv_reader = csv.reader(file)

    # Skip the header rows until reaching the actual data
    while True:
        header = next(csv_reader)
        if header[0].strip().isdigit():
            # Process the first data row
            row = header
            district_number = row[0].strip() if row[0].strip() else None
            district_name = row[1].strip() if row[1].strip() else None
            grade_2022 = row[14].strip() if row[14].strip() else None

            # Check if the district already exists in the table
            check_query = "SELECT COUNT(*) FROM Counties WHERE DistrictNumber = %s"
            cursor.execute(check_query, (district_number,))
            count = cursor.fetchone()[0]

            if count > 0:
                # District already exists, update the existing record
                update_query = """
                        UPDATE Counties
                        SET DistrictName = %s,
                            Grade2022 = %s
                        WHERE DistrictNumber = %s
                    """
                update_values = (district_name, grade_2022, district_number)
                cursor.execute(update_query, update_values)
            else:
                # District doesn't exist, insert a new record
                if grade_2022:
                    insert_query = """
                            INSERT INTO Counties (DistrictNumber, DistrictName, Grade2022)
                            VALUES (%s, %s, %s)
                        """
                    insert_values = (district_number, district_name, grade_2022)
                    cursor.execute(insert_query, insert_values)
                else:
                    print(f"Skipping insertion for district {district_number} due to missing Grade2022 value.")

            break

    # Iterate over each remaining row in the CSV file
    for row in csv_reader:
        # Extract the relevant data from the row
        district_number = row[0].strip() if row[0].strip() else None
        district_name = row[1].strip() if row[1].strip() else None
        grade_2022 = row[14].strip() if row[14].strip() else None

        # Check if the district already exists in the table
        check_query = "SELECT COUNT(*) FROM Counties WHERE DistrictNumber = %s"
        cursor.execute(check_query, (district_number,))
        count = cursor.fetchone()[0]

        if count > 0:
            # District already exists, update the existing record
            update_query = """
                    UPDATE Counties
                    SET DistrictName = %s,
                        Grade2022 = %s
                    WHERE DistrictNumber = %s
                """
            update_values = (district_name, grade_2022, district_number)
            cursor.execute(update_query, update_values)
        else:
            # District doesn't exist, insert a new record
            if grade_2022:
                insert_query = """
                        INSERT INTO Counties (DistrictNumber, DistrictName, Grade2022)
                        VALUES (%s, %s, %s)
                    """
                insert_values = (district_number, district_name, grade_2022)
                cursor.execute(insert_query, insert_values)
            else:
                print(f"Skipping insertion for district {district_number} due to missing Grade2022 value.")

# Commit the changes and close the cursor and connection
connection.commit()
cursor.close()
connection.close()