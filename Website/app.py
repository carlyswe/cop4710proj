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
            #pricepersqft = request.form['pricepersqft']
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

    cur.execute('SELECT * FROM Homes LIMIT 6')
    rows = cur.fetchall()

    return render_template("viewlistings.html", rows = rows)


@app.route('/house/<listingID>', methods = ['POST', 'GET'])
def house(listingID):
    con = database()
    cur = con.cursor(dictionary = True)

    query = "SELECT * FROM Homes WHERE listingID = %s"

    cur.execute(query, (listingID,))

    houseinfo = cur.fetchone()


    #format price to have commas


    return render_template("house.html", houseinfo=houseinfo, path='/house'+listingID)


@app.route('/editlisting/<listingID>', methods = ['POST', 'GET'])
def editlisting(listingID):
    con = database()
    con = con.cursor()






if __name__ == '__main__':
    app.run(debug = True)