from flask import Flask, render_template, request
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


@app.route('/addlisting', methods = ['POST', 'GET'])
def addlisting():
    if request.method == 'POST':
        try:

            price = request.form['price']
            sqft = request.form['sqft']
            numbed = request.form['numbeds']
            numfullbaths = request.form['numfullbaths']
            numhalfbaths = request.form['numhalfbaths']
            yearbuilt = request.form['yearbuilt']
            pricepersqft = request.form['pricepersqft']
            photourl = request.form['photourl']
            street = request.form['street']
            city = request.form['city']
            zipcode = request.form['zipcode']
            unit = request.form['unit']
            style = request.form['style']

            #what ab listing id when adding??

            con = database()
            cur = con.cursor()

            query = 'INSERT INTO Homes (beds, full_baths, half_baths, sqft, year_built, style, street, unit, city, ZipCode, price, photo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

            vals = (numbed, numfullbaths, numhalfbaths, sqft, yearbuilt, style, street, unit, city, zipcode, price, photourl)

            cur.execute(query, vals)

            con.close()
        except:
            print("error lol")

    return render_template("addlisting.html")

@app.route('/viewlistings', methods = ['POST', 'GET'])
def viewListings():

    con = database()

    cur = con.cursor(dictionary = True)

    cur.execute('SELECT * FROM Homes')
    rows = cur.fetchall()

    return render_template("viewlistings.html", rows = rows)



if __name__ == '__main__':
    app.run(debug = True)