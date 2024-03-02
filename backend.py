import requests
import json
import mysql.connector
import pandas as pd
import sqlite3
from tabulate import tabulate


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
# Create a cursor
cursor = con.cursor()

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
#cursor = con.cursor()
    cursor.execute(add_user, data_user)
query = "SELECT * FROM test_database.zoom_participant_list"
cursor.execute(query)
result = cursor.fetchall()
# Get column names
columns = [desc[0] for desc in cursor.description]

# Convert the result into a DataFrame
result_df = pd.DataFrame(result, columns=columns)

# Display the result as a table with borders and lines
print(tabulate(result_df, headers='keys', tablefmt='pretty'))
#result = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
#print(result)
#print(tabulate(myresult, headers=['Name', 'User_Email', 'Join_Time', 'Leave_Time', 'Duration'], tablefmt='psql'))
'''
result = cursor.fetchall()
widths = []
columns = []
tavnit = '|'
separator = '+' 

for cd in cursor.description:
    widths.append(max(cd[2], len(cd[0])))
    columns.append(cd[0])

for w in widths:
    tavnit += " %-"+"%ss |" % (w,)
    separator += '-'*w + '--+'

print(separator)
print(tavnit % tuple(columns))
print(separator)
for row in result:
    print(tavnit % row)
print(separator)
'''
#for row in result:
    #print(row)
    #print("\n")
    #cursor.execute("INSERT INTO test_database.zoom_participant_list(Name, User_Email, Join_Time, Leave_Time, Duration) VALUES (%s,%s,%s,%s,%s)",(Name, User_Email, Join_Time, Leave_Time, Duration))
con.commit()
cursor.close()
