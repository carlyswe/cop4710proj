import csv
import mysql.connector

def load_crime_data(csv_file):
    # Connect to the MySQL database
    db = mysql.connector.connect(
        host='',
        user='',
        password='',
        database=''
    )
    cursor = db.cursor()

    # Read the CSV file
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Insert the crime data into the CountyCrimeData table
            query = """
                INSERT INTO CountyCrimeData (
                    CountyName, Population, Total_Arrests, Arrest_Rate_per_100000, Total_Adult_Arrests,
                    Total_Juvenile_Arrests, Murder, Rape, Robbery, Aggravated_Assault, Burglary,
                    Larceny, Motor_Vehicle_Theft, Manslaughter, Kidnap_Abduction, Arson, Simple_Assault,
                    Drug_Arrest, Bribery, Embezzlement, Fraud, Counterfeit_Forgery, Extortion_Blackmail,
                    Intimidation, Prostitution, NonForcible_Sex_Offenses, Stolen_Property, DUI,
                    Destruction_Vandalism, Gambling, Weapons_Violations, Liquor_Law_Violations, Misc
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                row['County'], row['Population'], row['TotalArrests'], row['ArrestRate'], row['TotalAdultArrests'],
                row['TotalJuvenileArrests'], row['Murder'], row['Rape'], row['Robbery'], row['AggravatedAssault'],
                row['Burglary'], row['Larceny'], row['MotorVehicleTheft'], row['Manslaughter'], row['Kidnap/Abduction'],
                row['Arson'], row['SimpleAssault'], row['DrugArrest'], row['Bribery'], row['Embezzlement'],
                row['Fraud'], row['Counterfeit/Forgery'], row['Extortion/Blackmail'], row['Intimidation'],
                row['Prostitution'], row['Non-ForcibleSexOffenses'], row['StolenProperty'], row['DUI'],
                row['Destruction/Vandalism'], row['Gambling'], row['WeaponsViolations'], row['LiquorLawViolations'],
                row['Misc']
            )

            try:
                cursor.execute(query, values)
                db.commit()
                print(f"Crime data for {row['County']} loaded successfully.")
            except mysql.connector.Error as error:
                db.rollback()
                print(f"Error loading crime data for {row['County']}: {error}")

            # Update the population in the Districts table
            query = "UPDATE Districts SET Population = %s WHERE DistrictName = %s"
            values = (row['Population'], row['County'])

            try:
                cursor.execute(query, values)
                db.commit()
                print(f"Population for {row['County']} updated successfully.")
            except mysql.connector.Error as error:
                db.rollback()
                print(f"Error updating population for {row['County']}: {error}")

    cursor.close()
    db.close()

# Usage example
load_crime_data(r'C:\Users\dunlo\PycharmProjects\realestateproj\datatbl\crimedata.csv')