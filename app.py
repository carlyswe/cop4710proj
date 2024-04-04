from flask import Flask, render_template, request
import mysql.connector
import mysql
#pip install mysql-connector or use pip3 if error occurs

app = Flask(__name__)

#homepage
@app.route('/')
def index():
    return render_template ('index.html')

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


@app.route('/addlisting', methods = ['POST', 'GET'])
def addlisting():
    if request.method == 'POST':
        try:
            con = database()
            cur = con.cursor()

            cur.execute()
        except:
            print("error lol")

    return render_template("addlisting.html")


if __name__ == '__main__':
    app.run(debug = True)