from flask import Flask, render_template, request, redirect
import mysql.connector
from werkzeug.security import generate_password_hash

# 1. INITIALIZE FLASK
app = Flask(__name__)

# 2. CONNECT TO MYSQL DATABASE
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",   
    database="mydb"            # <--  name of the database I created
)
cursor = db.cursor()

# 3. HOMEPAGE ROUTE
@app.route('/')
def home():
    return render_template('index.html')

# 4. SIGNUP ROUTE (GET + POST)
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    # If form is submitted
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash (encrypt) the password
        hashed_password = generate_password_hash(password)

        # Insert into database
        sql = "INSERT INTO tbl_user (username, password) VALUES (%s, %s)"
        values = (username, hashed_password)
        cursor.execute(sql, values)
        db.commit()

        # Go back to homepage after signup
        return redirect('/')

    # If page is just opened
    return render_template('signup.html')

# 5. RUN THE APP
if __name__ == '__main__':
    app.run(debug=True)
