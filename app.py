#IMPORT THE MODULE AND PAKAGES FROM THE PIP
#==========================================================================================
# TITLE: "Secure API User Registration and Management with Flask and MySQL"               
# NAME : SABARIRAJAN KANNAN
# 
# 
#==========================================================================================
# -------------------------------------------------------------------------------------
from flask import Flask, jsonify, request
import mysql.connector
import re
import uuid
import hashlib
from werkzeug.utils import secure_filename  

# -----------------------------------------------------------------------------------------------------
# write a code

app = Flask(__name__)

# # MySQL Configuration




    


# Password validation regular expression
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

Email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

USERNAME_regex = r'^[A-Za-z0-9_]+$'

def validate_password(Password):
    return re.match(PASSWORD_REGEX, Password)

def validate_email(Email):
    return re.match(Email_regex,Email)
def validate_username(Username):
    return re.match(USERNAME_regex,Username)

@app.route('/register',methods=['POST'])

def register():
    try:
        data = request.args  # Use request.args to access URL query parameters

        Username = data.get('Username')
        Email = data.get('Email')
        Phonenumber = data.get('Phonenumber')
        password = data.get('Password')
        Confirm_password=data.get('Password')
        Department = data.get('Department')
        StudentID = data.get('StudentID')
        if not validate_email(Email):
            return jsonify({'message': 'Invalid email format'})
        
        if not validate_password(password):
            return jsonify({'message': 'Invalid password format'})
        
        if password !=  Confirm_password:
            return jsonify({'message': 'Does not match password '})
        
        if not is_valid_phone_number(Phonenumber):
            return jsonify({'message': 'Invalid phone number format'})
        
        if not validate_username(Username):
            return jsonify({'message': 'Invalid Username format'})
        
        # Hash the password using MD5 (not recommended for security, use better hashing methods)
        Password = hashlib.md5(password.encode()).hexdigest()
        confirm_password =hashlib.md5(Confirm_password.encode()).hexdigest()
        
        
        if Password!=  confirm_password:
            return jsonify({'message': 'Does not match Password '})
        unique_userid = str(uuid.uuid4())
        mydb = mysql.connector.connect(host='localhost', user='root', password='', database='api_validation')
        
        cur =mydb.cursor()
        cur.execute("INSERT INTO apiusers (unique_userid,Username,Email,Phonenumber, Password,confirm_password,Department,StudentID) VALUES (%s,%s, %s, %s, %s,%s,%s,%s)",
                    (unique_userid,Username.lower(),Email, Phonenumber, Password, confirm_password,Department,StudentID))
        mydb.commit()
        cur.close()
    
        return jsonify(message="Registration successful"), 201
    except mysql.connector.Error as db_error:
            error_response = {"error": "Database error: " + str(db_error)}
            return jsonify(error_response), 500
    except KeyError:
        error_response = {"error": "Invalid data format"}
        return jsonify(error_response), 400
def is_valid_phone_number(Phonenumber):
    # Check if the phone number has exactly 10 digits
    return len(Phonenumber) == 10

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.args  # Assuming the data is sent in JSON format
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'message': 'Invalid email or password'}), 400

        # Hash the password using MD5 (not recommended for security, use better hashing methods)
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        # Connect to the database
        mydb = mysql.connector.connect(host="localhost", port=3306, user="root", password='', database="api_validation")
        cursor = mydb.cursor()
        query = "SELECT DISTINCT Email,Password FROM apiusers WHERE Email = %s AND Password = %s;"
        cursor.execute(query, (email, hashed_password))
        user = cursor.fetchone()
        cursor.close()
        mydb.close()

        if user:
            return jsonify({'message': 'Login successful'})
        else:
            # Invalid credentials
            return jsonify({'message': 'Invalid email or password'}), 401

    except mysql.connector.Error as db_error:
        error_response = {"error": "Database error: " + str(db_error)}
        return jsonify(error_response), 500
    except KeyError:
        error_response = {"error": "Invalid data format"}
        return jsonify(error_response), 400

@app.route('/updatedetails/<int:StudentID>', methods=['PUT', 'Post'])

def updatedetails(StudentID):
    try:
        data = request.args
        
        DateOfBirth = data.get('DateOfBirth')
        Blood_Group = data.get('Blood_Group')
        Emergencynumber = data.get('Emergencynumber')
        Address = data.get('Address')
        Phonenumber = data.get('Phonenumber')
        if not is_valid_phone_number(Emergencynumber):
            return jsonify({'message': 'Invalid Emergency number format'})
        mydb = mysql.connector.connect( host="localhost",port=3306,user="root", password="", database="api_validation")
        # Create a cursor object to interact with the database
        cursor = mydb.cursor()

        # Add columns to the apiusers table if they do not exist
        cursor.execute("ALTER TABLE apiusers ADD COLUMN IF NOT EXISTS DateOfBirth DATE")
        cursor.execute("ALTER TABLE apiusers ADD COLUMN IF NOT EXISTS Blood_Group VARCHAR(255)")
        cursor.execute("ALTER TABLE apiusers ADD COLUMN IF NOT EXISTS Emergencynumber VARCHAR(255)")
        cursor.execute("ALTER TABLE apiusers ADD COLUMN IF NOT EXISTS Address VARCHAR(255)")
   

        # Update the specific user's data
        update_query = "UPDATE apiusers SET Phonenumber = %s,DateOfBirth = %s, Blood_Group = %s, Emergencynumber = %s, Address = %s  WHERE StudentID = %s"
        cursor.execute(update_query,(Phonenumber,DateOfBirth, Blood_Group, Emergencynumber, Address, StudentID))

        # Commit the changes to the database
        mydb.commit()
        cursor.close()
        mydb.close()

        return "Data updated successfully."
    except mysql.connector.Error as db_error:
        error_response = {"error": "Database error: " + str(db_error)}
        return jsonify(error_response), 500
    except Exception as e:
        return str(e),500
    
def is_EMERGENCY_phone_number(Emergencynumber):
    # Check if the phone number has exactly 10 digits
    return len(Emergencynumber) == 10      
    # api student details all in json format avoid only password because this very secure code
@app.route('/adddetails/<int:StudentID>', methods=['PUT', 'Post'])

def add_details(StudentID):
    try:
        data = request.args
    
        GradeOfMark = data.get('GradeOfMark')
        DEGREE = data.get('DEGREE')
        YearOfGraduate = data.get('YearOfGraduate')
        collegeName = data.get('collegeName')
       
       
        mydb = mysql.connector.connect( host="localhost",port=3306,user="root", password="", database="api_validation")
        # Create a cursor object to interact with the database
        cursor = mydb.cursor()

        # Add columns to the apiusers table if they do not exist
      
        cursor.execute("ALTER TABLE apiusers ADD COLUMN IF NOT EXISTS GradeOfMark VARCHAR(25)")
        cursor.execute("ALTER TABLE apiusers ADD COLUMN IF NOT EXISTS DEGREE VARCHAR(60)")
        cursor.execute("ALTER TABLE apiusers ADD COLUMN IF NOT EXISTS YearOfGraduate year")
        cursor.execute("ALTER TABLE apiusers ADD COLUMN IF NOT EXISTS collegeName VARCHAR(255)")

        # Update the specific user's data
        update_query = "UPDATE apiusers SET GradeOfMark= %s,DEGREE= %s,YearOfGraduate= %s,collegeName= %s WHERE StudentID = %s"
        cursor.execute(update_query,(GradeOfMark,DEGREE,YearOfGraduate ,collegeName, StudentID))

        # Commit the changes to the database
        mydb.commit()
        cursor.close()
        mydb.close()

        return "Data updated successfully."
    except mysql.connector.Error as db_error:
        error_response = {"error": "Database error: " + str(db_error)}
        return jsonify(error_response), 500
    except Exception as e:
        return str(e),500
@app.route('/apiuserall', methods=['GET'])
def getdataall():
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
        query = "SELECT * FROM apiusers;"
        cursor.execute(query)

        # Fetch the results
        result = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        mydb.close()

        # Process the result and return a response
        # (You should format the result as needed)
       
            
        response_data = [{
                "unique_userId": rows[0], 
                "Username": rows[1],
                "Email": rows[2],
                "Phonenumber":rows[3],
                "Department":rows[6],
                "StudentID": rows[7],
                "DateOfBirth": rows[8],
                "Blood_Group": rows[9],
                "Emergencynumber":rows[10],
                "Address":rows[11]
            }for rows in result]
        return jsonify(response_data)
        

    except Exception as e:
        return str(e), 500    
# this particular data will show input param
@app.route('/apiuser/<StudentID>', methods=['GET'])
def getdata(StudentID):
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
        query = "SELECT * FROM apiusers where StudentID = %s;"
        cursor.execute(query,(StudentID,))

        # Fetch the results
        result = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        

        # Process the result and return a response
        # (You should format the result as needed)
        if result:
            
            response_data = {
                "unique_userId": result[0], 
                "Username": result[1],
                "Email": result[2],
                "Phonenumber":result[3],
                "Department":result[6],
                "StudentID": result[7],
                "DateOfBirth": result[8],
                "Blood_Group": result[9],
                "Emergencynumber":result[10],
                "Address":result[11]
            } 
            return jsonify(response_data)
        else:
            return jsonify({"message": "No data found for the provided StudentID."}), 404

    except Exception as e:
        return str(e), 500

@app.route("/coursedetails/<StudentID>", methods=["Get"])
def coursedetails(StudentID):
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
        query = "SELECT * FROM apiusers where StudentID = %s;"
        cursor.execute(query,(StudentID,))

        # Fetch the results
        result = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        

        # Process the result and return a response
        # (You should format the result as needed)
        if result:
            
            response_data = { 
                "DEGREE":result[13],
                "GradeOfMark":result[12],
                "Department":result[6],
                "Username": result[1],
                "StudentID": result[7],
                "collegeName": result[15],
                "YearOfGraduate": result[14]
 
            } 
            return jsonify(response_data)
        else:
            return jsonify({"message": "No data found for the provided StudentID."}), 404

    except Exception as e:
        return str(e), 500


    
   
   
   
if __name__ == '__main__':
    app.run(debug='True',host='192.168.1.5',port=8888)

