from flask import Flask, render_template, request, redirect
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

#crime map
@app.route('/crimemap', methods=['GET', 'POST'])
def crimemap():
    if request.method == "POST":
        try:
            print("IN HEREEEEEE")

            county = request.form['county']

            county = str(county)

            print(county)

            con = database()
            cur = con.cursor(dictionary = True)

            cur.execute("SELECT * FROM CrimeStatistics WHERE CrimeStatistics.CountyName = %s", (county,))

            print("below the query")

            crime = cur.fetchone()

            print(crime)

            print("below the fetch")


            con.close()

        except mysql.connector.Error as err:
            print("SOMETHING WENT WRONG !!!!!!!!!: {}".format(err))


        return render_template("crimemap.html", crime=crime)

    else:
        print("here")
        crime = {'Total_Arrests': 0, 'Manslaughter': 0, 'Simple_Assault': 0, 'Larceny': 0, 'Kidnap_Abduction': 0, 'Burglary': 0, 'crimeGrade': 'N/A'}
    return render_template("crimemap.html", crime=crime)







    return render_template ('crimemap.html')

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
        con.commit()
        con.close()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        msg = "Unable to delete listing. Please check Listing ID."
    return render_template("deletelisting.html", msg="Listing has been deleted.")


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
            style = request.form['style'] or None

            print("here")

            #what ab listing id when adding??

            con = database()
            cur = con.cursor()

            query = 'INSERT INTO Homes (beds, full_baths, half_baths, sqft, year_built, style, street, unit, city, ZipCode, price, photo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

            vals = (numbed, numfullbaths, numhalfbaths, sqft, yearbuilt, style, street, unit, city, zipcode, price, photourl)

            cur.execute(query, vals)

            msg = "Home Added Successfully."
            #redirect to view it as a listing but need to pass listing id for buildable url
            #return redirect(/house, )

            con.commit()

            con.close()

        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            msg = "Unable to add listing."
            print("error")

    return render_template('addlisting.html', msg = msg)

@app.route('/viewlistings', methods = ['POST', 'GET'])
def viewListings():

    con = database()

    cur = con.cursor(dictionary = True)

    cur.execute('SELECT * FROM Homes LIMIT 6' )
    rows = cur.fetchall()

    con.close()

    return render_template("viewlistings.html", rows = rows)


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
    cur.execute("SELECT DistrictNumber, DistrictName FROM Counties WHERE DistrictName = %s", (county,))
    districtinfo = cur.fetchone()
    districtnum = int(districtinfo["DistrictNumber"])
    districtname = str(districtinfo["DistrictName"])

    print(districtnum)

    #get school info
    cur.execute("SELECT * FROM Schools WHERE DistrictNumber = %s", (districtnum,))
    schools = cur.fetchall()


    #query to get crime info
    cur.execute("SELECT * FROM CrimeStatistics WHERE CrimeStatistics.CountyName = %s", (districtname,))
    crime = cur.fetchone()

    ##print(houseinfo)

    con.close()

    #join statistics on county name

    return render_template("house.html", houseinfo=houseinfo, schools=schools, districtname=districtname, crime=crime, path='/house'+listingID)


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