from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector
import mysql
#pip install mysql-connector or use pip3 if error occurs

app = Flask(__name__)

#homepage
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template ('Index.html')

#this is connects us to database
def database():
    hostname = "db-newhomes.c9weqm4g04ms.us-east-2.rds.amazonaws.com"
    username = "admin"
    password = "cop4710!"
    db = mysql.connector.connect(
        host = hostname,
        user = username,
        passwd = password,
        database = "realtorsite")

    return db

@app.route('/crimemap', methods=['GET', 'POST'])
def crimemap():
    db = database()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT DistrictName FROM Counties")
    counties = cursor.fetchall()

    selected_county_data = {}
    avg_data = {}
    if request.method == 'POST':
        selected_county = request.json['county']
        print(f"Selected county: {selected_county}")
        # Fetch crime data for selected county
        cursor.execute("""
            SELECT 
                Burglary, Larceny, Motor_Vehicle_Theft,
                Manslaughter, Kidnap_Abduction, Arson, Simple_Assault,
                Drug_Arrest, Bribery, Embezzlement, Fraud,
                Counterfeit_Forgery, Extortion_Blackmail, Intimidation,
                Prostitution, NonForcible_Sex_Offenses, Stolen_Property,
                DUI, Destruction_Vandalism, Gambling, Weapons_Violations,
                Liquor_Law_Violations, Misc
            FROM CrimeStatistics
            WHERE CountyName = %s
        """, (selected_county,))
        selected_county_data = cursor.fetchone()
        # Fetch average data for comparison
        cursor.execute("""
            SELECT 
                AVG(Total_Arrests) as AvgTotal_Arrests,
                AVG(Burglary) as AvgBurglary,
                AVG(Arson) as AvgArson,
                AVG(Bribery) as AvgBribery,
                AVG(Larceny) as AvgLarceny,
                AVG(Motor_Vehicle_Theft) as AvgMotor_Vehicle_Theft
            FROM CrimeStatistics
        """)
        avg_data = cursor.fetchone()

        print("Selected county data:", selected_county_data)
        print("Average data:", avg_data)

        return jsonify({
            'selected_county_data': selected_county_data,
            'avg_data': avg_data
        })

    cursor.close()
    db.close()

    return render_template('crimemap.html', counties=[county['DistrictName'] for county in counties])

#delete listing function
@app.route('/deletelisting', methods = ['POST', 'GET'])
def deletelisting():
    msg = ""
    if request.method == 'POST':
        try:
            ID = request.form['listingID']

            con = database()
            cur = con.cursor()


            query = "DELETE FROM Homes WHERE listingID = %s"

            cur.execute(query,(ID,))

            msg = "Listing has been sucessfully deleted."


            con.commit()

            con.close()

        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            msg = "Unable to delete listing. Please check Listing ID."
            print("error")

    return render_template('deletelisting.html', msg = msg)


@app.route('/deletelisting/<listingID>', methods=['POST', 'GET'])
def deletedirectlisting(listingID):
    try:
        con = database()
        cur = con.cursor()

        query = "DELETE FROM Homes WHERE listingID = %s"
        cur.execute(query, (listingID, ))
        msg = "Listing has been deleted."
        con.commit()
        con.close()

    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        msg = "Unable to delete listing. Please check Listing ID."
    return render_template("deletelisting.html", msg=msg)



@app.route('/addlisting', methods = ['POST', 'GET'])
def addlisting():
    msg = ""
    if request.method == 'POST':
        try:

            price = request.form['price']
            sqft = request.form['sqft']
            numbed = request.form['numbeds']
            numfullbaths = request.form['numfullbaths']
            numhalfbaths = request.form['numhalfbaths']
            yearbuilt = request.form['yearbuilt'] or None
            photourl = request.form['photourl'] or None
            street = request.form['street']
            city = request.form['city']
            zipcode = request.form['zipcode']
            unit = request.form['unit'] or None
            longitude = request.form['longitude'] or None
            latitude = request.form['latitude'] or None

            print("here")

            #what ab listing id when adding??

            con = database()
            cur = con.cursor()

            query = 'INSERT INTO Homes (beds, full_baths, half_baths, sqft, year_built, street, unit, city, ZipCode, price, photo, longitude, latitude) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

            vals = (numbed, numfullbaths, numhalfbaths, sqft, yearbuilt, street, unit, city, zipcode, price, photourl, longitude, latitude)

            cur.execute(query, vals)
            con.commit()

            msg = "Home Added Successfully."
            #redirect to view it as a listing but need to pass listing id for buildable url
            #return redirect(/house, )


            cur.execute("SELECT listingID FROM Homes ORDER BY listingID DESC LIMIT 1")


            listingadded = cur.fetchone()

            con.close()

            return redirect("/house/" + str(listingadded[0]))


        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            msg = "Unable to add listing."
            print("error")

    return render_template('addlisting.html', msg = msg)

@app.route('/viewlistings', methods=['POST', 'GET'])
def viewListings():

    #if they have submitted filtering options
    if request.method == 'POST':
        form_data = request.form
        print(form_data)
        safetygrade = request.form['safetyGrade']
        city = request.form['city']
        schoolgrade = request.form['schoolGrade']


        if(city != "all"):
            con = database()
            cur = con.cursor(dictionary=True)

            cur.execute('SELECT listingID, city, street, photo, latitude, longitude, price FROM Homes WHERE city = %s ORDER BY RAND() LIMIT 24',
                (city,))
            rows = cur.fetchall()

            con.close()

            con = database()
            cur = con.cursor()

            cur.execute('''SELECT COUNT(*) FROM Homes WHERE City = %s''', (city,))
            numlistings = cur.fetchone()

            con.close()

        #if saftey grade is selected
        elif(safetygrade != "all"):
            #if school grade isnt selected then search only by safety grade
            if(schoolgrade == "all"):
                print("only safety")
                con = database()
                cur = con.cursor(dictionary=True)
                cur.execute("SELECT Homes.listingID, Homes.city, Homes.street, Homes.photo, Homes.latitude, Homes.longitude, Homes.price FROM Homes JOIN ZipCodes ON Homes.ZipCode = ZipCodes.ZipCode JOIN CrimeStatistics ON ZipCodes.County = CrimeStatistics.CountyName WHERE CrimeStatistics.crimeGrade =%s ORDER BY RAND() LIMIT 24 ", (safetygrade,))
                rows = cur.fetchall()

                con.close()
                con = database()
                cur = con.cursor()

                cur.execute("SELECT COUNT(*) FROM Homes JOIN ZipCodes ON Homes.ZipCode = ZipCodes.ZipCode JOIN CrimeStatistics ON ZipCodes.County = CrimeStatistics.CountyName WHERE CrimeStatistics.crimeGrade =%s ", (safetygrade,))
                numlistings = cur.fetchone()

                con.close()

            #query for both school grade and safety grade
            else:

                print("here")
                con = database()
                cur = con.cursor(dictionary=True)
                cur.execute("SELECT Homes.listingID, Homes.city, Homes.street, Homes.photo, Homes.latitude, Homes.longitude, Homes.price FROM Homes JOIN ZipCodes ON Homes.ZipCode = ZipCodes.ZipCode JOIN CrimeStatistics ON ZipCodes.County = CrimeStatistics.CountyName JOIN Counties ON ZipCodes.County = Counties.DistrictName WHERE CrimeStatistics.crimeGrade = %s AND Counties.Grade2022 = %s ORDER BY RAND() LIMIT 24 ", (safetygrade, schoolgrade))
                rows = cur.fetchall()

                con.close()

                con = database()
                cur = con.cursor()

                cur.execute('SELECT COUNT(*) FROM Homes JOIN ZipCodes ON Homes.ZipCode = ZipCodes.ZipCode JOIN CrimeStatistics ON ZipCodes.County = CrimeStatistics.CountyName JOIN Counties ON ZipCodes.County = Counties.DistrictName WHERE CrimeStatistics.crimeGrade = %s AND Counties.Grade2022 = %s ', (safetygrade, schoolgrade))
                numlistings = cur.fetchone()

                con.close()


        #if only school grade is selected
        elif(schoolgrade != "all"):
            con = database()
            cur = con.cursor(dictionary=True)

            cur.execute('SELECT Homes.listingID, Homes.city, Homes.street, Homes.photo, Homes.latitude, Homes.longitude, Homes.price FROM Homes JOIN ZipCodes ON Homes.ZipCode = ZipCodes.ZipCode JOIN Counties ON ZipCodes.County = Counties.DistrictName WHERE Counties.Grade2022 = %s ORDER BY RAND() LIMIT 24', (schoolgrade,))
            rows = cur.fetchall()

            con.close()

            con = database()
            cur = con.cursor()

            cur.execute('''SELECT COUNT(*) FROM Homes JOIN ZipCodes ON Homes.ZipCode = ZipCodes.ZipCode JOIN Counties ON ZipCodes.County = Counties.DistrictName WHERE Counties.Grade2022 = %s''', (schoolgrade,))
            numlistings = cur.fetchone()

            con.close()

        else:

            con = database()
            cur = con.cursor(dictionary=True)

            # Modify the query to fetch latitude and longitude along with other details
            cur.execute(
                'SELECT listingID, city, street, photo, latitude, longitude, price FROM Homes ORDER BY RAND() LIMIT 24')
            rows = cur.fetchall()
            con.close()

            con = database()
            cur = con.cursor()

            con = database()
            cur = con.cursor()

            cur.execute('SELECT COUNT(*) FROM Homes')
            numlistings = cur.fetchone()

            con.close()

        con = database()
        cur = con.cursor(dictionary=True)

        cur.execute("SELECT DISTINCT City FROM ZipCodes ORDER BY City ASC")
        cities = cur.fetchall()

        con.close()

        print(rows)

        return render_template("viewlistings.html", rows=rows, cities=cities, numlistings=numlistings)


    con = database()
    cur = con.cursor(dictionary=True)

    # Modify the query to fetch latitude and longitude along with other details
    cur.execute('SELECT listingID, city, street, photo, latitude, longitude, price FROM Homes ORDER BY RAND() LIMIT 24')
    rows = cur.fetchall()

    con.close()

    con = database()
    cur = con.cursor(dictionary=True)


    cur.execute("SELECT DISTINCT City FROM ZipCodes ORDER BY City ASC")
    cities = cur.fetchall()

    con.close()

    con = database()
    cur = con.cursor()

    cur.execute('SELECT COUNT(*) FROM Homes')
    numlistings = cur.fetchone()

    print(numlistings)

    con.close()

    print(rows)

    return render_template("viewlistings.html", rows=rows, cities=cities, numlistings=numlistings)
@app.route('/house/<listingID>', methods = ['POST', 'GET'])
def house(listingID):
    con = database()
    cur = con.cursor(dictionary = True)

    query = "SELECT * FROM Homes WHERE listingID = %s"

    cur.execute(query, (listingID,))

    houseinfo = cur.fetchone()


    #query to get school data


    #join zipcodes to house where they match and then get the county then return all schools in that county and the grade

    #getting the county based on home
    cur.execute("SELECT County FROM ZipCodes JOIN Homes ON ZipCodes.ZipCode = Homes.ZipCode WHERE Homes.listingID = %s", (listingID,))
    county = cur.fetchone()

    print(county)

    county = str(county["County"])

    #get the district number
    cur.execute("SELECT * FROM Counties WHERE DistrictName = %s", (county,))
    districtinfo = cur.fetchone()
    districtnum = int(districtinfo["DistrictNumber"])
    districtname = str(districtinfo["DistrictName"])
    districtgrade = str(districtinfo["Grade2022"])

    print(districtnum)

    #get school info
    cur.execute("SELECT * FROM Schools WHERE DistrictNumber = %s", (districtnum,))
    schools = cur.fetchall()


    #query to get crime info
    cur.execute("Select * FROM CrimeStatistics WHERE CrimeStatistics.statisticsID = %s", (districtnum,))
    crime = cur.fetchone()
    print(crime)

    ##print(houseinfo)

    con.close()

    #join statistics on county name

    return render_template("house.html", houseinfo=houseinfo, schools=schools, districtgrade = districtgrade, districtname=districtname, crime=crime, path='/house'+listingID)


@app.route('/editlisting/<listingID>', methods = ['POST', 'GET'])
def editlisting(listingID):
    con = database()
    cur = con.cursor(dictionary=True)

    query = "SELECT * FROM Homes WHERE listingID = %s"

    cur.execute(query, (listingID,))

    houseinfo = cur.fetchone()

    print(houseinfo)

    con.close()

    return render_template("editlisting.html", houseinfo=houseinfo, path='/editlisting'+listingID)


@app.route("/edit/<listingID>", methods = ['POST', 'GET'])
def edit(listingID):
    if request.method == 'POST':
        con = database()
        cur = con.cursor()
        try:

            print("hereeeeeee")

            price = request.form['price']

            print("here1")
            sqft = request.form['sqft']

            print("here2")
            numbed = request.form['numbeds']

            print("here3")
            numfullbaths = request.form['numfullbaths']

            print("here4")
            numhalfbaths = request.form['numhalfbaths'] or None

            print("here5")
            yearbuilt = request.form['yearbuilt'] or None

            print("here6")
            photourl = request.form['photo']

            print("here7")
            street = request.form['street']

            print("here8")
            city = request.form['city']

            print("here9")
            zipcode = request.form['zipcode']

            print("here10")
            unit = request.form['unit'] or None


            print("here12")



            query = "UPDATE Homes SET price = %s, sqft = %s, beds = %s, full_baths = %s, half_baths = %s, year_built = %s, photo = %s, street = %s, city = %s, ZipCode = %s, unit = %s WHERE listingID = %s"

            cur.execute(query, (price, sqft, numbed, numfullbaths, numhalfbaths, yearbuilt, photourl, street, city, zipcode, unit, listingID))
            con.commit()

        except Exception as e:
            con.rollback()
            print("Exception: ", e)

        con.close()
        return redirect("/house/"+listingID)

if __name__ == '__main__':
    app.run(debug = True)