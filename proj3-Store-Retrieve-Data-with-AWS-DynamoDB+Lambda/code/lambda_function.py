import boto3
import json
import uuid
import datetime
import base64
import os

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ContactMessages')

# Function to load HTML file content
def load_html(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def lambda_handler(event, context):
    method = event.get('httpMethod', '')

    # Serve Contact Us page
    if method == 'GET':
        html_content = load_html('contact-us.html')
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': html_content
        }

    # Handle Form Submission (POST)
    elif method == 'POST':
        # Decode form data
        body = event.get('body', '')
        if event.get('isBase64Encoded', False):
            body = base64.b64decode(body).decode('utf-8')

        # Parse form data (key=value&key2=value2)
        params = dict(x.split('=') for x in body.split('&'))

        # Get form fields
        name = params.get('name', '')
        email = params.get('email', '')
        message = params.get('message', '')

        # Insert into DynamoDB
        table.put_item(Item={
            'name': name,
            'email': email,
            'message': message,
            'timestamp': str(datetime.datetime.utcnow())
        })

        # Return success page
        html_content = load_html('success.html')
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': html_content
        }

    # Unsupported Method
    else:
        return {
            'statusCode': 405,
            'body': 'Method Not Allowed'
        }