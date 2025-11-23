from flask import Flask, render_template, request, redirect, jsonify   
import mysql.connector
from werkzeug.security import generate_password_hash
from pydantic import BaseModel

# 1. INITIALIZE FLASK
app = Flask(__name__)

"""
Setup database configurations 
"""
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "CSC312_DB"
}

# SETUP DATABASE CONNECTION 
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Define validation model 
class User(BaseModel):
    username: str
    password: str

# 3. HOMEPAGE ROUTE
@app.route('/')
def home():
    return render_template('index.html')

# 4. SIGNUP ROUTE (GET + POST)
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    # If form is submitted
    if request.method == 'POST':
        # Validate the form data
        try:
            user_data = User(username=request.form['username'], password=request.form['password'])
            username = user_data.username
            password = user_data.password
            hashed_password = generate_password_hash(password)

            # Insert into database
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT username FROM tbl_user WHERE username = %s",
                (username,)
            )
            existing_user = cursor.fetchone()
            
            if existing_user:
                return render_template('signup.html', message='Username already exists')

            # Insert into database 
            sql = "INSERT INTO tbl_user (username, password) VALUES (%s, %s)"
            values = (username, hashed_password)
            cursor.execute(sql, values)
            conn.commit()

            # Close the connection
            cursor.close()
            conn.close()

            return render_template('index.html', message='User registered successfully')

        except Exception as e:
            return render_template('signup.html', message=str(e))
        except mysql.connector.Error as e:
            return render_template('signup.html', message="Something went wrong: {}".format(e))

    # If page is just opened
    return render_template('signup.html')

# 5. RUN THE APP
if __name__ == '__main__':
    app.run(debug=True)
