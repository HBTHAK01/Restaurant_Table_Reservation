from flask import Flask, render_template, url_for, request, flash, redirect, session
from flask_session import Session
import mysql.connector
from werkzeug.utils import redirect

app = Flask(__name__)

#add
app.config["SESSION_PERMANENT"] =  False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
#end add

app.secret_key = "abc"  

# Database Part for MySQL
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="Restaurant_Reservation"
)

mycursor = mydb.cursor()

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        email_login = request.form['email_login']
        pass_login = request.form['pass_login']  
              
        # mycursor = mydb.cursor()
        # sql_select = "SELECT Email, Password FROM Users"
        # mycursor.execute(sql_select) 
        # result = mycursor.fetchall()

        # session["email"] = email_login #get email to html 
        mycursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email_login, pass_login, ))
        account = mycursor.fetchone()

        if account:
            # session['name'] = account['name']
            session['name'] = account[0]

            return redirect ("/user_reservation")
        else:
           flash("Email and/or password is incorrect.", "error")

        # print(result)
        # for i in range(len(result)):
        #     if email_login == result[i][0] and pass_login == result[i][1]:
        #         # mycursor.execute('Select First_Name from users where Email = %s', (email_login))
        #         # msg = mycursor.fetchone()
        #         session["name"] = "HELLO"
        #         return redirect ("/user_reservation")
        #     else:
        #         flash("Email and/or password is incorrect.", "error")

    return render_template("index.html")


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        contact = request.form['contact']
        email = request.form['email']
        pass_word = request.form['pass_word']
        pass_c = request.form['pass_c']

        if pass_word == pass_c:
            mycursor = mydb.cursor()
            sql_insert = """INSERT INTO Users (First_Name, Last_Name, Phone_Number, Email, Password)
                            VALUES (%s, %s, %s, %s, %s)"""
            sql_value = (fname, lname, contact, email, pass_word)
            mycursor.execute(sql_insert, sql_value)
            mydb.commit()

            return redirect ("http://127.0.0.1:5000/")
        else:
            flash("Password fields do not match", "error")
        
    return render_template("sign_up.html")

@app.route("/user_reservation", methods=['GET', 'POST'])
def user_reservation():
    # msg = ''
    # # if request.method == 'POST':
    # email = session["email"]

    # mycursor = mydb.cursor()
    # mycursor.execute('Select First_Name from users where Email = %s', (email))
    # msg = mycursor.fetchone()
    return render_template("user_reservation.html")

@app.route("/reservation")
def reservation():
    return render_template("reservation.html")
 
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug = True)