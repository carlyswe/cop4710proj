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
            english_language_arts_achievement = float(row[2].strip()) if row[2].strip() else None
            mathematics_achievement = float(row[3].strip()) if row[3].strip() else None
            science_achievement = float(row[4].strip()) if row[4].strip() else None
            social_studies_achievement = float(row[5].strip()) if row[5].strip() else None
            middle_school_acceleration = float(row[6].strip()) if row[6].strip() else None
            grad_rate_2021_22 = float(row[7].strip()) if row[7].strip() else None
            career_accel_2021_22 = float(row[8].strip()) if row[8].strip() else None
            total_points_earned = float(row[9].strip()) if row[9].strip() else None
            total_components = int(row[10].strip()) if row[10].strip() else None
            percent_of_total_possible_points = float(row[11].strip()) if row[11].strip() else None
            percent_tested = float(row[12].strip()) if row[12].strip() else None
            informational_baseline_grade_2023 = row[13].strip() if row[13].strip() else None
            grade_2022 = row[14].strip() if row[14].strip() else None
            grade_2021 = row[15].strip() if row[15].strip() else None
            grade_2019 = row[16].strip() if row[16].strip() else None
            grade_2018 = row[17].strip() if row[17].strip() else None
            grade_2017 = row[18].strip() if row[18].strip() else None
            grade_2016 = row[19].strip() if row[19].strip() else None
            informational_baseline_grade_2015 = row[20].strip() if row[20].strip() else None
            grade_2014 = row[21].strip() if row[21].strip() else None
            grade_2013 = row[22].strip() if row[22].strip() else None
            grade_2012 = row[23].strip() if row[23].strip() else None
            grade_2011 = row[24].strip() if row[24].strip() else None
            grade_2010 = row[25].strip() if row[25].strip() else None

            # Check if the district already exists in the table
            check_query = "SELECT COUNT(*) FROM Districts WHERE DistrictNumber = %s"
            cursor.execute(check_query, (district_number,))
            count = cursor.fetchone()[0]

            if count > 0:
                # District already exists, update the existing record
                update_query = """
                        UPDATE Districts
                        SET DistrictName = %s,
                            EnglishLanguageArtsAchievement = %s,
                            MathematicsAchievement = %s,
                            ScienceAchievement = %s,
                            SocialStudiesAchievement = %s,
                            MiddleSchoolAcceleration = %s,
                            GradRate_2021_22 = %s,
                            Career_Accel_2021_22 = %s,
                            TotalPointsEarned = %s,
                            TotalComponents = %s,
                            PercentOfTotalPossiblePoints = %s,
                            PercentTested = %s,
                            InformationalBaselineGrade2023 = %s,
                            Grade2022 = %s,
                            Grade2021 = %s,
                            Grade2019 = %s,
                            Grade2018 = %s,
                            Grade2017 = %s,
                            Grade2016 = %s,
                            InformationalBaselineGrade2015 = %s,
                            Grade2014 = %s,
                            Grade2013 = %s,
                            Grade2012 = %s,
                            Grade2011 = %s,
                            Grade2010 = %s
                        WHERE DistrictNumber = %s
                    """
                update_values = (
                    district_name, english_language_arts_achievement, mathematics_achievement,
                    science_achievement, social_studies_achievement, middle_school_acceleration,
                    grad_rate_2021_22, career_accel_2021_22, total_points_earned,
                    total_components, percent_of_total_possible_points, percent_tested,
                    informational_baseline_grade_2023, grade_2022, grade_2021, grade_2019,
                    grade_2018, grade_2017, grade_2016, informational_baseline_grade_2015,
                    grade_2014, grade_2013, grade_2012, grade_2011, grade_2010,
                    district_number
                )
                cursor.execute(update_query, update_values)
            else:
                # District doesn't exist, insert a new record
                insert_query = """
                        INSERT INTO Districts (
                            DistrictNumber, DistrictName, EnglishLanguageArtsAchievement,
                            MathematicsAchievement, ScienceAchievement, SocialStudiesAchievement,
                            MiddleSchoolAcceleration, GradRate_2021_22, Career_Accel_2021_22,
                            TotalPointsEarned, TotalComponents, PercentOfTotalPossiblePoints,
                            PercentTested, InformationalBaselineGrade2023, Grade2022, Grade2021,
                            Grade2019, Grade2018, Grade2017, Grade2016,
                            InformationalBaselineGrade2015, Grade2014, Grade2013, Grade2012,
                            Grade2011, Grade2010
                        )
                        VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s
                        )
                    """
                insert_values = (
                    district_number, district_name, english_language_arts_achievement,
                    mathematics_achievement, science_achievement, social_studies_achievement,
                    middle_school_acceleration, grad_rate_2021_22, career_accel_2021_22,
                    total_points_earned, total_components, percent_of_total_possible_points,
                    percent_tested, informational_baseline_grade_2023, grade_2022, grade_2021,
                    grade_2019, grade_2018, grade_2017, grade_2016,
                    informational_baseline_grade_2015, grade_2014, grade_2013, grade_2012,
                    grade_2011, grade_2010
                )
                cursor.execute(insert_query, insert_values)

            break

    # Iterate over each remaining row in the CSV file
    for row in csv_reader:
        # Extract the relevant data from the row
        district_number = row[0].strip() if row[0].strip() else None
        district_name = row[1].strip() if row[1].strip() else None
        english_language_arts_achievement = float(row[2].strip()) if row[2].strip() else None
        mathematics_achievement = float(row[3].strip()) if row[3].strip() else None
        science_achievement = float(row[4].strip()) if row[4].strip() else None
        social_studies_achievement = float(row[5].strip()) if row[5].strip() else None
        middle_school_acceleration = float(row[6].strip()) if row[6].strip() else None
        grad_rate_2021_22 = float(row[7].strip()) if row[7].strip() else None
        career_accel_2021_22 = float(row[8].strip()) if row[8].strip() else None
        total_points_earned = float(row[9].strip()) if row[9].strip() else None
        total_components = int(row[10].strip()) if row[10].strip() else None
        percent_of_total_possible_points = float(row[11].strip()) if row[11].strip() else None
        percent_tested = float(row[12].strip()) if row[12].strip() else None
        informational_baseline_grade_2023 = row[13].strip() if row[13].strip() else None
        grade_2022 = row[14].strip() if row[14].strip() else None
        grade_2021 = row[15].strip() if row[15].strip() else None
        grade_2019 = row[16].strip() if row[16].strip() else None
        grade_2018 = row[17].strip() if row[17].strip() else None
        grade_2017 = row[18].strip() if row[18].strip() else None
        grade_2016 = row[19].strip() if row[19].strip() else None
        informational_baseline_grade_2015 = row[20].strip() if row[20].strip() else None
        grade_2014 = row[21].strip() if row[21].strip() else None
        grade_2013 = row[22].strip() if row[22].strip() else None
        grade_2012 = row[23].strip() if row[23].strip() else None
        grade_2011 = row[24].strip() if row[24].strip() else None
        grade_2010 = row[25].strip() if row[25].strip() else None

        # Check if the district already exists in the table
        check_query = "SELECT COUNT(*) FROM Districts WHERE DistrictNumber = %s"
        cursor.execute(check_query, (district_number,))
        count = cursor.fetchone()[0]

        if count > 0:
            # District already exists, update the existing record
            update_query = """
                    UPDATE Districts
                    SET DistrictName = %s,
                        EnglishLanguageArtsAchievement = %s,
                        MathematicsAchievement = %s,
                        ScienceAchievement = %s,
                        SocialStudiesAchievement = %s,
                        MiddleSchoolAcceleration = %s,
                        GradRate_2021_22 = %s,
                        Career_Accel_2021_22 = %s,
                        TotalPointsEarned = %s,
                        TotalComponents = %s,
                        PercentOfTotalPossiblePoints = %s,
                        PercentTested = %s,
                        InformationalBaselineGrade2023 = %s,
                        Grade2022 = %s,
                        Grade2021 = %s,
                        Grade2019 = %s,
                        Grade2018 = %s,
                        Grade2017 = %s,
                        Grade2016 = %s,
                        InformationalBaselineGrade2015 = %s,
                        Grade2014 = %s,
                        Grade2013 = %s,
                        Grade2012 = %s,
                        Grade2011 = %s,
                        Grade2010 = %s
                    WHERE DistrictNumber = %s
                """
            update_values = (
                district_name, english_language_arts_achievement, mathematics_achievement,
                science_achievement, social_studies_achievement, middle_school_acceleration,
                grad_rate_2021_22, career_accel_2021_22, total_points_earned,
                total_components, percent_of_total_possible_points, percent_tested,
                informational_baseline_grade_2023, grade_2022, grade_2021, grade_2019,
                grade_2018, grade_2017, grade_2016, informational_baseline_grade_2015,
                grade_2014, grade_2013, grade_2012, grade_2011, grade_2010,
                district_number
            )
            cursor.execute(update_query, update_values)
        else:
            # District doesn't exist, insert a new record
            insert_query = """
                    INSERT INTO Districts (
                        DistrictNumber, DistrictName, EnglishLanguageArtsAchievement,
                        MathematicsAchievement, ScienceAchievement, SocialStudiesAchievement,
                        MiddleSchoolAcceleration, GradRate_2021_22, Career_Accel_2021_22,
                        TotalPointsEarned, TotalComponents, PercentOfTotalPossiblePoints,
                        PercentTested, InformationalBaselineGrade2023, Grade2022, Grade2021,
                        Grade2019, Grade2018, Grade2017, Grade2016,
                        InformationalBaselineGrade2015, Grade2014, Grade2013, Grade2012,
                        Grade2011, Grade2010
                    )
                    VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s
                    )
                """
            insert_values = (
                district_number, district_name, english_language_arts_achievement,
                mathematics_achievement, science_achievement, social_studies_achievement,
                middle_school_acceleration, grad_rate_2021_22, career_accel_2021_22,
                total_points_earned, total_components, percent_of_total_possible_points,
                percent_tested, informational_baseline_grade_2023, grade_2022, grade_2021,
                grade_2019, grade_2018, grade_2017, grade_2016,
                informational_baseline_grade_2015, grade_2014, grade_2013, grade_2012,
                grade_2011, grade_2010
            )
            cursor.execute(insert_query, insert_values)

    # Commit the changes and close the cursor and connection
connection.commit()
cursor.close()
connection.close()