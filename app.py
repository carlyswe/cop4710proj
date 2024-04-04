from flask import Flask, render_template
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



@app.route('/addlisting', methods = ['POST'])
def addlisting():
    con = database()
    cur = con.cursor()

    cur.execute()


if __name__ == '__main__':
    app.run(debug = True)