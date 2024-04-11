import csv
import mysql.connector

def load_crime_data(csv_file):
    # Connect to the MySQL database
    db = mysql.connector.connect(
        host='db-newhomes.c9weqm4g04ms.usa-east-2.rds.amazonaws.com',
        user='admin',
        password='cop4710!',
        database='realtorsite'
    )
    cursor = db.cursor()

    # Read the CSV file
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        county_data = {}
        statistics_id = 1

        for row in reader:
            # Preprocess the row data
            for key, value in row.items():
                if ',' in value:
                    row[key] = value.replace(',', '')

            county_name = row['County']
            if county_name in county_data:
                print(f"Duplicate data found for {county_name}. Skipping...")
                continue

            county_data[county_name] = row

            # Insert the crime data into the CrimeStatistics table
            query = """
            INSERT INTO CrimeStatistics (
                statisticsID,
                CountyName,
                totalCrimeIndex,
                Total_Arrests,
                Population,
                Burglary,
                Larceny,
                Motor_Vehicle_Theft,
                Manslaughter,
                Kidnap_Abduction,
                Arson,
                Simple_Assault,
                Drug_Arrest,
                Bribery,
                Embezzlement,
                Fraud,
                Counterfeit_Forgery,
                Extortion_Blackmail,
                Intimidation,
                Prostitution,
                NonForcible_Sex_Offenses,
                Stolen_Property,
                DUI,
                Destruction_Vandalism,
                Gambling,
                Weapons_Violations,
                Liquor_Law_Violations,
                Misc
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                statistics_id,
                row['County'],
                row.get('totalCrimeIndex', 0),
                row['TotalArrests'],
                row['Population'],
                row['Burglary'],
                row['Larceny'],
                row['MotorVehicleTheft'],
                row['Manslaughter'],
                row['Kidnap/Abduction'],
                row['Arson'],
                row['SimpleAssault'],
                row['DrugArrest'],
                row['Bribery'],
                row['Embezzlement'],
                row['Fraud'],
                row['Counterfeit/Forgery'],
                row['Extortion/Blackmail'],
                row['Intimidation'],
                row['Prostitution'],
                row['Non-ForcibleSexOffenses'],
                row['StolenProperty'],
                row['DUI'],
                row['Destruction/Vandalism'],
                row['Gambling'],
                row['WeaponsViolations'],
                row['LiquorLawViolations'],
                row['Misc']
            )
            try:
                cursor.execute(query, values)
                db.commit()
                print(f"Crime data for {row['County']} loaded successfully.")
                statistics_id += 1
            except mysql.connector.Error as error:
                db.rollback()
                print(f"Error loading crime data for {row['County']}: {error}")

    cursor.close()
    db.close()

# Usage example
load_crime_data(r'C:\Users\dunlo\PycharmProjects\realestateproj\datatbl\crimedata.csv')