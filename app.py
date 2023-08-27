# -------------------------------------------------------------------------------------
#  impot query
from flask import Flask, jsonify, request
import mysql.connector
import json
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import InputRequired, Email, Length, Regexp
import re
# import email_validator
# -----------------------------------------------------------------------------------------------------
# write a code

app = Flask(__name__)







# Password validation regular expression
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

Email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

def validate_password(password):
    return re.match(PASSWORD_REGEX, password)

def validate_email(email):
    return re.match(Email_regex,email)


@app.route('/login', methods=['POST'])
def login():
   
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    if not validate_email(email):
        return jsonify({'message': 'Invalid email format'})

    # Perform email and password validation
    
    if not validate_password(password):
        return jsonify({'message': 'Invalid password format'})
    
    # If validation succeeds, store the values in the database
    mydb = mysql.connector.connect( host="localhost",port=3306, user="root" , password='', database="api_validation")
      # Use the 'connection' attribute
    cursor = mydb.cursor()
    query = "INSERT INTO apiuser (email, password) VALUES (%s, %s)"
    cursor.execute(query, (email, password))
    mydb.commit()
    cursor.close()
    return jsonify({'message': 'Login successful and user data stored in the database'})

@app.route('/apiuser', methods=['GET'])
def getdata():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",  # Provide the correct username
            password="",  # Provide the correct password
            database="api_validation"
        )
        
        # Create a cursor
        cursor = mydb.cursor()

        # Execute a SQL query
        query = "SELECT * FROM apiuser;"
        cursor.execute(query)

        # Fetch the results
        result = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        mydb.close()

        # Process the result and return a response
        # (You should format the result as needed)
        response_data = [{"id": row[0], "name": row[1],"password":row[2]} for row in result]
        return jsonify(response_data)

    except Exception as e:
        return str(e), 500
    
@app.route('/forget_password/<int:id>', methods=['PUT'])
def forget_password(id):
    try:
        data = request.get_json()
        new_password = data['password']

        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",  # Provide the correct username
            password="",  # Provide the correct password
            database="api_validation"
        )

        # Create a cursor
        cursor = mydb.cursor()

        # Execute a SQL query
        query = "UPDATE apiuser SET password = %s WHERE ID = %s;"
        cursor.execute(query, (new_password, id))
        mydb.commit()

        # Close the cursor and connection
        cursor.close()
        mydb.close()

        response = {"message": "Password updated successfully"}
        return jsonify(response), 200

    except mysql.connector.Error as db_error:
        error_response = {"error": "Database error: " + str(db_error)}
        return jsonify(error_response), 500

    except KeyError:
        error_response = {"error": "Invalid data format"}
        return jsonify(error_response), 400

    except Exception as e:
        error_response = {"error": str(e)}
        return jsonify(error_response), 500
        
if __name__ == '__main__':
    app.run(debug=True,port=8888)

