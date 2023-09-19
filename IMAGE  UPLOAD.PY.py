
from datetime import datetime
import os
import requests
import mysql.connector
from flask import Flask, request, jsonify
# from google.cloud import storage
from mysql.connector import connect
import base64


app = Flask(__name__)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'api_validation',
    'port':3306
}
@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        data = request.args  # Use request.args to access URL query parameters

        Title = data.get('Title')
        Author = data.get('Author')
        Description = data.get('Description')
        Image_file = request.files.get('Image_data')
        if not Image_file:
            return jsonify({'message': 'No image provided in the request.'}), 400

        if not Image_file.filename.endswith(('.png', '.jpg', '.jpeg')):
            return jsonify({'message': 'The image must be a PNG, JPG, or JPEG file.'}), 400
        
        # Read the contents of the uploaded file
        Image_data =Image_file.read()

        # Convert the image data to a base64-encoded string
        Image_base64 = base64.b64encode(Image_data).decode('utf-8')
        DateOfPost = datetime.now()
        # Insert the data into the table
        insert_query = "INSERT INTO apiuser (Title, ImageData, Author, Description,DateOfPost) VALUES (%s,%s, %s,%s,%s)"
        cursor.execute(insert_query, (Title, Image_base64, Author, Description, DateOfPost ),)

        conn.commit()
        
        # # Upload the image to the Google Cloud Storage bucket
        # client = storage.Client()
        # bucket = client.get_bucket('my-bucket')
        # blob = bucket.blob(Image_file.filename)
        # blob.upload_from_file(Image_file)
        
        return jsonify({'message': 'Image uploaded successfully'})

    except KeyError as e:
        return jsonify({'error': str(e)}),500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            
@app.route('/get/<ID>', methods=['GET'])
def get_image(ID):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        select_query = "SELECT * FROM apiuser WHERE id = %s"
        cursor.execute(select_query, (ID,))
        result = cursor.fetchone()

        if result:
          response_data = {
             'ID': result[0],
             'Title': result[1],
             'Author':  result[2],
             'Description':  result[3],
             'DateOfPost':result[4],
             'ImageData': base64.b64encode(result[5]).decode('utf-8')
            }
          return jsonify(response_data)
            
            
        else:
            return jsonify({'message': 'Post not found'})

    except mysql.connector.Error as db_error:
        error_response = {"error": "Database error: " + str(db_error)}
        return jsonify(error_response), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == '__main__':
  app.run(debug=True)
