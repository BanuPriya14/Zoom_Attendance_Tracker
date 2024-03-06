import mysql.connector
import pandas as pd
from tabulate import tabulate
import json
import tkinter as tk
from tkinter import ttk

def fetch_and_display_data(host, user, password, database, query, json_file):
    # Load participant data from JSON
    with open('participant_data.json', 'r') as f:
        data = json.load(f)

    try:
        # Connect to MySQL database
        con = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            database=database
        )
        if con.is_connected():
            print("Connected!")
    except Exception as e:
        print("Cannot Connect! Try Again!")
        return

    # Create a cursor
    cursor = con.cursor()

    # Iterate over the data and insert each participant into the database
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

        cursor.execute(add_user, data_user)

    # Execute the query to fetch data
    cursor.execute(query)

    # Fetch the result
    result = cursor.fetchall()

    # Get column names
    columns = [desc[0] for desc in cursor.description]

    # Convert the result into a DataFrame
    result_df = pd.DataFrame(result, columns=columns)

    # Close cursor and connection
    cursor.close()
    con.close()

    return result_df

def sort_table(df, column):
    return df.sort_values(by=column)

def filter_table(df, column, filter_text):
    # Convert column to string type before applying .str accessor
    if df[column].dtype != 'object':
        df[column] = df[column].astype(str)
    return df[df[column].str.contains(filter_text, case=False)]


def display_table_in_window(df):
    def sort_table_handler():
        sorted_df = sort_table(df, combo_sort.get())
        label.config(text=sorted_df.to_string())

    def filter_table_handler():
        filtered_df = filter_table(df, combo_filter.get(), entry_filter.get())
        label.config(text=filtered_df.to_string())

    root = tk.Tk()

    # Create a frame for sorting and filtering
    frame = tk.Frame(root)
    frame.pack()

    # Create a sorting dropdown
    combo_sort = ttk.Combobox(frame, values=df.columns.tolist())
    combo_sort.pack(side=tk.LEFT)
    combo_sort.set("Sort by")

    # Create a button for sorting
    btn_sort = tk.Button(frame, text="Sort", command=sort_table_handler)
    btn_sort.pack(side=tk.LEFT)

    # Create a filter dropdown
    combo_filter = ttk.Combobox(frame, values=df.columns.tolist())
    combo_filter.pack(side=tk.LEFT)
    combo_filter.set("Filter by")

    # Create an entry for filter criteria
    entry_filter = tk.Entry(frame)
    entry_filter.pack(side=tk.LEFT)

    # Create a button for filtering
    btn_filter = tk.Button(frame, text="Filter", command=filter_table_handler)
    btn_filter.pack(side=tk.LEFT)

    # Create a Tkinter label to display the table
    label = tk.Label(root, text=df.to_string(), justify='left', font=('Courier', 10))
    label.pack()

    root.mainloop()

# Example usage:
host = 'localhost'
user = 'root'
password = 'root@123'
database = 'test_database'
query = "SELECT * FROM test_database.zoom_participant_list"
json_file = 'participant_data.json'

result_df = fetch_and_display_data(host, user, password, database, query, json_file)
display_table_in_window(result_df)

