import requests
import json
import mysql.connector

from flask import Flask, abort, request
from uuid import uuid4
import requests
import requests.auth
import urllib


# API credentials
api_key = 'oVhfBgjRRe5QCjvFlB5Iw'
api_secret = 'IYMLJO5o05E3LtJ3afdT9tPjgs4bROD3'

CLIENT_ID = api_key # Fill this in with your client ID
CLIENT_SECRET = api_secret # Fill this in with your client secret
REDIRECT_URI = "http://localhost:65010/zoom_callback"

app = Flask(__name__)
@app.route('/')
def homepage():
    text = '<a href="%s">Authenticate with Zoom</a>'
    return text % make_authorization_url()


def make_authorization_url():
    # Generate a random string for the state parameter
    # Save it for use later to prevent xsrf attacks
    
    params = {"client_id": CLIENT_ID,
              "response_type": "code",
              "redirect_uri": REDIRECT_URI}
    url = "https://zoom.us/oauth/authorize?" + urllib.parse.urlencode(params)
    return url



@app.route('/zoom_callback')
def zoom_callback():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    
    code = request.args.get('code')
    access_token = get_token(code)
    # Note: In most cases, you'll want to store the access token, in, say,
    # a session for use in other parts of your web app.
    return "Your user info is: %s" % get_username(access_token)

def get_token(code):
    
    global oAuth
    
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": REDIRECT_URI}

    response = requests.post("https://zoom.us/oauth/token",
                             auth=client_auth,
                             data=post_data)
    token_json = response.json()
    print(token_json)
    
    oAuth = token_json["access_token"]
    
    return token_json["access_token"]
    
    
def get_username(access_token):
    
    headers= {"Authorization": "bearer " + access_token}
    response = requests.get("https://api.zoom.us/v2/users/me", headers=headers)
    me_json = response.json()
    
    # getMeetingInfo(access_token)
        
    return me_json


def getMeetingInfo(access_token):
    # Meeting ID for which you want to get attendees
    meeting_id = '88321453048'

    # API endpoint
    url = f'https://api.zoom.us/v2/report/meetings/{meeting_id}/participants'

    # Headers
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Make GET request
    response = requests.get(url, headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        attendees = response.json()
        participant_list = json.dumps(attendees, indent=4)


        #print(participant_list)
        with open('participant_data.json', 'r') as f:
            data = json.load(f)
        #print(data)
        try:
            con = mysql.connector.connect(
                user = 'root',
                password = 'root@123',
                host = 'localhost',
                port = 3306,
                database = 'test_database'
            )
            if con.is_connected():
                print("Connected!")
        except Exception as e:
            print("Cannot Connect! Try Again!")
        cursor = con.cursor()
        #cursor.execute("create table zoom_participant_list (Name varchar(255), User_Email varchar(255), Join_Time datetime, Leave_Time datetime, Duration int(5))")
        
        for item in data['participants']:
            Name = item['name']
            User_Email = item['user_email']
            Join_Time = item['join_time']
            Leave_Time = item['leave_time']
            Duration = item['duration']
            cursor.execute("INSERT INTO zoom_participant_list (Name,User_Email,Join_Time,Leave_Time,Duration)")
            con.commit()
        #print(type(Name))

        
    else:
        print(f'Failed to retrieve attendees. Status code:{response.status_code}, Error: {response.text}')




if __name__ == '__main__':
    app.run(debug=True, port=65010)













# # Generate JWT token
# import jwt
# import datetime

# token_exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)  # Token expires in 1 hour
# token_payload = {
#     'iss': api_key,
#     'exp': token_exp
# }





# # API endpoint
# url1 = f'https://zoom.us/oauth/token'

# headers = {
#     'Authorization': f'Basic 3Q_qrPdJQ-GJBpIPbcZ6Yw',
#     'Content-Type': 'application/x-www-form-urlencoded'
# }

# # Make GET request
# response = requests.get(url1, headers=headers)


# jwt_token = jwt.encode(token_payload, api_secret, algorithm='HS256')
# #jwt_token = "eyJzdiI6IjAwMDAwMSIsImFsZyI6IkhTNTEyIiwidiI6IjIuMCIsImtpZCI6IjJhYzBkNmQyLTk0YTEtNGNlZi1hMmE3LWQ0NDMzNzI4ZjQ4MCJ9.eyJ2ZXIiOjksImF1aWQiOiI1ZmQ5YWU1YjNiMWRmNzc2OTY2Nzc5NDk4ZDVkYTY3MiIsImNvZGUiOiJGcm1VRzY1clRZdXdzUko0WFVCVG5tZ2ZTdzNxS1EzTVEiLCJpc3MiOiJ6bTpjaWQ6cHJobG5xdkNSQ0cyaGZIb3FvZWZRIiwiZ25vIjowLCJ0eXBlIjowLCJ0aWQiOjAsImF1ZCI6Imh0dHBzOi8vb2F1dGguem9vbS51cyIsInVpZCI6IkVZczVFZk1iUmptTzlzTVRobFJTYkEiLCJuYmYiOjE3MDkzMzc3ODgsImV4cCI6MTcwOTM0MTM4OCwiaWF0IjoxNzA5MzM3Nzg4LCJhaWQiOiJWX19QNXF3NlE5ZUVjbDJrZHljMmhRIn0.Rb9AsCuTD0FJyI3RBgvoCv6v018qYEVMcHglhmhdWuKTlSe9WSwW01Wv3VyfvL3fU5b2zfLe4NRgu1VIwp0ESQ"
