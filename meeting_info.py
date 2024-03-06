import requests
import json
import mysql.connector

# API credentials
#api_key = 'smdiXiQBQyGCi33lQj5Tg'
#api_secret = 'GUb452sabnTh9BrFZlK4aiNHid6mZs3u'

# Generate JWT token
#import jwt
#import datetime

#token_exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)  # Token expires in 1 hour
#token_payload = {
    #'iss': api_key,
    #'exp': token_exp
#}
#jwt_token = jwt.encode(token_payload, api_secret, algorithm='HS256')
#jwt_token = "eyJzdiI6IjAwMDAwMSIsImFsZyI6IkhTNTEyIiwidiI6IjIuMCIsImtpZCI6ImZlMTk5ZDRmLTYyZWUtNDYzOS05MmM5LTNmZmJhNjlkYzliZiJ9.eyJ2ZXIiOjksImF1aWQiOiIxOTg4N2QzNWJhMDQ3OThmZGJmOWM2OTBkZjJkZGQwMSIsImNvZGUiOiI0VVg1TFRTTTE2T3RaWGx4UTVYUmlPVHFfeU5FUExQQ3ciLCJpc3MiOiJ6bTpjaWQ6cnp5aHU0eFhRcmFwUDRubWtwa0xnIiwiZ25vIjowLCJ0eXBlIjowLCJ0aWQiOjAsImF1ZCI6Imh0dHBzOi8vb2F1dGguem9vbS51cyIsInVpZCI6IkVZczVFZk1iUmptTzlzTVRobFJTYkEiLCJuYmYiOjE3MDk2NjM2ODUsImV4cCI6MTcwOTY2NzI4NSwiaWF0IjoxNzA5NjYzNjg1LCJhaWQiOiJWX19QNXF3NlE5ZUVjbDJrZHljMmhRIn0.iFnyfLb31xJgESjMQPChtncFbLVI4I4bCtsxR19LdcfxEGySYRDZUmE5Pj_4zdISavWYi-nqCdFINDAmXJRf2A"

# Meeting ID for which you want to get attendees
#my_meeting_id = '88321453048'

# API endpoint
#url = f'https://api.zoom.us/v2/report/users/banugus@gmail.com/meetings?from=2024-02-02&to=2024-03-03&page_size=30'

# Headers
#headers = {
    #'Authorization': f'Bearer {jwt_token}',
    #'Content-Type': 'application/json'
#}

# Make GET request
#response = requests.get(url, headers=headers)

# Check if request was successful
#if response.status_code == 200:
    #meeting_ids = response.json()
    #meeting_id_list = json.dumps(meeting_ids, indent=4)


    #print(participant_list)
with open('meeting_id.json', 'r') as f:
    meeting_id_data = json.load(f)
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
#print(meeting_id_data)      
for item in meeting_id_data['meetings']:
    Meeting_ID = item['id']
    Meeting_Topic = item['topic']
    No_of_Participants = item['participants_count']
    Total_Minutes = item['total_minutes']
    Duration = item['duration']
    print(Meeting_ID)
    print(Meeting_Topic)
    print(No_of_Participants)
    print(Total_Minutes)
    print(Duration)

 
 
    #cursor.execute("CREATE TABLE test_database.Meeting_List (Meeting_ID INT(255) PRIMARY KEY, Meeting_Topic VARCHAR(255) NOT NULL, No_of_Participants INT(100), Total_Minutes INT,Duration INT(100))")        
        
        
    add_meeting = """INSERT INTO test_database.Meeting_List 
                      (Meeting_ID,Meeting_Topic,No_of_Participants,Total_Minutes,Duration) 
                      VALUES (%s, %s, %s, %s, %s)"""
                      
                        
                      
    data_meeting = (Meeting_ID,Meeting_Topic,No_of_Participants,Total_Minutes,Duration)

    cursor.execute(add_meeting, data_meeting)
               
    con.commit()
    #print(type(Name))

    
#else:
    #print(f'Failed to retrieve attendees. Status code:{response.status_code}, Error: {response.text}')
