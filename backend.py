import requests
import json
import mysql.connector

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

#cursor.execute("create table zoom_participant_list (Name varchar(255), User_Email varchar(255), Join_Time datetime, Leave_Time datetime, Duration int(5))")
      
for item in data['participants']:
    Name = item['name']
    User_Email = item['user_email']
    Join_Time = item['join_time']
    Leave_Time = item['leave_time']
    Duration = item['duration']

    add_user = """INSERT INTO test_database.zoom_participant_list 
              (Name, User_Email, Join_Time, Leave_Time, Duration) 
              VALUES (%s, %s, %s, %s, %s)"""
    data_user = (Name, User_Email, Join_Time, Leave_Time, Duration)
    cursor = con.cursor()
    cursor.execute(add_user, data_user)
    #cursor.execute("INSERT INTO test_database.zoom_participant_list(Name, User_Email, Join_Time, Leave_Time, Duration) VALUES (%s,%s,%s,%s,%s)",(Name, User_Email, Join_Time, Leave_Time, Duration))
    con.commit()
    cursor.close()
#print(type(Name))