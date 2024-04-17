import csv
import mysql.connector

# Establish a connection to the MySQL server
connection = mysql.connector.connect(
        host='db-newhomes.c9weqm4g04ms.us-east-2.rds.amazonaws.com',
        user='admin',
        password='cop4710!',
        database='realtorsite'
    )

# Create a cursor object to execute queries
cursor = connection.cursor()

# Open the CSV file
with open(r'/Users/adelinebelova/Data/schoolgrades.csv', 'r') as file:
    csv_reader = csv.reader(file)

    # Skip the header rows until reaching the actual data
    while True:
        header = next(csv_reader)
        if header[0].strip().isdigit():
            break

    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Extract the relevant data from the row
        district_number = int(row[0].strip()) if row[0].strip() else None
        district_name = row[1].strip() if row[1].strip() else None
        school_number = int(row[2].strip()) if row[2].strip() else None
        school_name = row[4].strip() if row[4].strip() else None
        grade_2022 = row[17].strip()[:1] if row[17].strip() else None

        # Check if the district already exists in the database
        query = "SELECT COUNT(*) FROM Counties WHERE DistrictNumber = %s"
        cursor.execute(query, (district_number,))
        count = cursor.fetchone()[0]

        if count == 0:
            # District does not exist, insert a new record into Counties table
            query = "INSERT INTO Counties (DistrictNumber, DistrictName, Grade2022) VALUES (%s, %s, %s)"
            try:
                cursor.execute(query, (district_number, district_name, grade_2022))
            except mysql.connector.errors.DatabaseError as err:
                print(f"Error inserting record into Counties table: {err}")
                continue

        # Check if the school already exists in the database
        query = "SELECT COUNT(*) FROM Schools WHERE SchoolID = %s"
        cursor.execute(query, (school_number,))
        count = cursor.fetchone()[0]

        if count == 0:
            # School does not exist, insert a new record into Schools table
            query = "INSERT INTO Schools (SchoolID, DistrictNumber, SchoolName, Grade2022) VALUES (%s, %s, %s, %s)"
            try:
                cursor.execute(query, (school_number, district_number, school_name, grade_2022))
            except mysql.connector.errors.DatabaseError as err:
                print(f"Error inserting record into Schools table: {err}")
                continue

# Commit the changes and close the cursor and connection
connection.commit()
cursor.close()
connection.close()