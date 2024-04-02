import csv
import mysql.connector

# Establish a connection to the MySQL server
connection = mysql.connector.connect(
    host='',
    user='',
    password='',
    database=''
)

# Create a cursor object to execute queries
cursor = connection.cursor()

# Open the CSV file
with open(r'C:\Users\dunlo\PycharmProjects\realestateproj\datatbl\schoolgrades.csv', 'r') as file:
    csv_reader = csv.reader(file)

    # Skip the header rows until reaching the actual data
    while True:
        header = next(csv_reader)
        if header[0].strip().isdigit():
            break

    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Extract the relevant data from the row
        district_number = row[0].strip() if row[0].strip() else None
        district_name = row[1].strip() if row[1].strip() else None
        school_number = row[2].strip() if row[2].strip() else None
        virtual_provider_number = row[3].strip() if row[3].strip() else None
        school_name = row[4].strip() if row[4].strip() else None
        english_language_arts_achievement = float(row[5].strip()) if row[5].strip() else None
        mathematics_achievement = float(row[6].strip()) if row[6].strip() else None
        science_achievement = float(row[7].strip()) if row[7].strip() else None
        total_points_earned = float(row[8].strip()) if row[8].strip() else None
        total_components = int(row[9].strip()) if row[9].strip() else None
        percent_of_total_possible_points = float(row[10].strip()) if row[10].strip() else None
        percent_tested = float(row[11].strip()) if row[11].strip() else None
        informational_baseline_grade_2023 = row[12].strip()[:1] if row[12].strip() else None
        grade_2022 = row[13].strip()[:1] if row[13].strip() else None
        grade_2021 = row[14].strip()[:1] if row[14].strip() else None
        grade_2019 = row[15].strip()[:1] if row[15].strip() else None
        grade_2018 = row[16].strip()[:1] if row[16].strip() else None
        grade_2017 = row[17].strip()[:1] if row[17].strip() else None
        grade_2016 = row[18].strip()[:1] if row[18].strip() else None
        informational_baseline_grade_2015 = row[19].strip()[:1] if row[19].strip() else None
        grade_2014 = row[20].strip()[:1] if row[20].strip() else None
        grade_2013 = row[21].strip()[:1] if row[21].strip() else None
        grade_2012 = row[22].strip()[:1] if row[22].strip() else None
        grade_2011 = row[23].strip()[:1] if row[23].strip() else None
        grade_2010 = row[24].strip()[:1] if row[24].strip() else None
        grade_2009 = row[25].strip()[:1] if row[25].strip() else None
        grade_2008 = row[26].strip()[:1] if row[26].strip() else None
        grade_2007 = row[27].strip()[:1] if row[27].strip() else None
        grade_2006 = row[28].strip()[:1] if row[28].strip() else None
        grade_2005 = row[29].strip()[:1] if row[29].strip() else None
        grade_2004 = row[30].strip()[:1] if row[30].strip() else None
        grade_2003 = row[31].strip()[:1] if row[31].strip() else None
        grade_2002 = row[32].strip()[:1] if row[32].strip() else None
        grade_2001 = row[33].strip()[:1] if row[33].strip() else None
        grade_2000 = row[34].strip()[:1] if row[34].strip() else None
        grade_1999 = row[35].strip()[:1] if row[35].strip() else None
        was_collocated_rule_used = bool(row[36].strip()) if row[36].strip() else None
        collocated_number =  None
        charter_school = bool(row[38].strip()) if row[38].strip() else None
        title_i = bool(row[39].strip()) if row[39].strip() else None
        alt_ese_center = bool(row[40].strip()) if row[40].strip() else None
        school_type = row[41].strip() if row[41].strip() else None

        # Check if minority_percent is a numeric value
        minority_percent_str = row[42].strip()
        if minority_percent_str.replace('.', '', 1).isdigit():
            minority_percent = float(minority_percent_str)
        else:
            minority_percent = None

        # Check if minority_percent is a numeric value
        econ_disadvantaged_percentstr = row[42].strip()
        if econ_disadvantaged_percentstr.replace('.', '', 1).isdigit():
            econ_disadvantaged_percent = float(minority_percent_str)
        else:
            econ_disadvantaged_percent = None

        # Prepare the SQL INSERT statement
        query = """
            INSERT INTO Schools (
                DistrictNumber, DistrictName, SchoolNumber, VirtualProviderNumber,
                SchoolName, EnglishLanguageArtsAchievement, MathematicsAchievement,
                ScienceAchievement, TotalPointsEarned, TotalComponents,
                PercentOfTotalPossiblePoints, PercentTested,
                InformationalBaselineGrade2023, Grade2022, Grade2021, Grade2019,
                Grade2018, Grade2017, Grade2016, InformationalBaselineGrade2015,
                Grade2014, Grade2013, Grade2012, Grade2011, Grade2010, Grade2009,
                Grade2008, Grade2007, Grade2006, Grade2005, Grade2004, Grade2003,
                Grade2002, Grade2001, Grade2000, Grade1999, WasCollocatedRuleUsed,
                CollocatedNumber, CharterSchool, TitleI, Alt_ESE_Center, SchoolType,
                MinorityPercent, EconDisadvantagedPercent
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
        """

        # Execute the INSERT statement
        cursor.execute(query, (
            district_number, district_name, school_number, virtual_provider_number,
            school_name, english_language_arts_achievement, mathematics_achievement,
            science_achievement, total_points_earned, total_components,
            percent_of_total_possible_points, percent_tested,
            informational_baseline_grade_2023, grade_2022, grade_2021, grade_2019,
            grade_2018, grade_2017, grade_2016, informational_baseline_grade_2015,
            grade_2014, grade_2013, grade_2012, grade_2011, grade_2010, grade_2009,
            grade_2008, grade_2007, grade_2006, grade_2005, grade_2004, grade_2003,
            grade_2002, grade_2001, grade_2000, grade_1999, was_collocated_rule_used,
            collocated_number, charter_school, title_i, alt_ese_center, school_type,
            minority_percent, econ_disadvantaged_percent
        ))

# Commit the changes and close the cursor and connection
connection.commit()
cursor.close()
connection.close()