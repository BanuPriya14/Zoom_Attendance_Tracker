import requests
import json
import mysql.connector

# API credentials
api_key = 'smdiXiQBQyGCi33lQj5Tg'
api_secret = 'GUb452sabnTh9BrFZlK4aiNHid6mZs3u'

# Generate JWT token
import jwt
import datetime

token_exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)  # Token expires in 1 hour
token_payload = {
    'iss': api_key,
    'exp': token_exp
}
#jwt_token = jwt.encode(token_payload, api_secret, algorithm='HS256')
jwt_token = "eyJzdiI6IjAwMDAwMSIsImFsZyI6IkhTNTEyIiwidiI6IjIuMCIsImtpZCI6IjJhYzBkNmQyLTk0YTEtNGNlZi1hMmE3LWQ0NDMzNzI4ZjQ4MCJ9.eyJ2ZXIiOjksImF1aWQiOiI1ZmQ5YWU1YjNiMWRmNzc2OTY2Nzc5NDk4ZDVkYTY3MiIsImNvZGUiOiJGcm1VRzY1clRZdXdzUko0WFVCVG5tZ2ZTdzNxS1EzTVEiLCJpc3MiOiJ6bTpjaWQ6cHJobG5xdkNSQ0cyaGZIb3FvZWZRIiwiZ25vIjowLCJ0eXBlIjowLCJ0aWQiOjAsImF1ZCI6Imh0dHBzOi8vb2F1dGguem9vbS51cyIsInVpZCI6IkVZczVFZk1iUmptTzlzTVRobFJTYkEiLCJuYmYiOjE3MDkzMzc3ODgsImV4cCI6MTcwOTM0MTM4OCwiaWF0IjoxNzA5MzM3Nzg4LCJhaWQiOiJWX19QNXF3NlE5ZUVjbDJrZHljMmhRIn0.Rb9AsCuTD0FJyI3RBgvoCv6v018qYEVMcHglhmhdWuKTlSe9WSwW01Wv3VyfvL3fU5b2zfLe4NRgu1VIwp0ESQ"

# Meeting ID for which you want to get attendees
meeting_id = '88321453048'

# API endpoint
url = f'https://api.zoom.us/v2/report/meetings/{meeting_id}/participants'

# Headers
headers = {
    'Authorization': f'Bearer {jwt_token}',
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



