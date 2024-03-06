import tkinter as tk
from tkinter import *
from tkinter import ttk
import mysql.connector
import pyttsx3
from PIL import Image, ImageTk
import main as m
from main import window
from tkinter import messagebox

engine = pyttsx3.init()
global admin

def verifyAdmin(username, password, is_signup):
    '''
    In this function i have established a connection to my database "python_mini_project" and table "admin_data"
    this function verifies weather the admin data is registered in database or not
    if data is there then success message is displayed else failure
    '''

    try:
        con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root@123",
        database="python_mini_project"
    )
        print("Database Status: Connection Established Successfully")

        
        
        if is_signup:
            cursor = con.cursor()
            # Insert new admin data into the database
            #sql = ("INSERT INTO python_mini_project.admin_data (username,password,admin_name) VALUES (%s,%s,%s);", (username, password,"test"))
            
            sql1 = """INSERT INTO python_mini_project.admin_data (username, password,admin_name) VALUES (%s, %s,%s)"""
                      
            val2 = (username, password,"Test")
            cursor.execute(sql1,val2)
            con.commit()
            #print("Signup Status: Signup Success")
            messagebox.showinfo("Signup Success", "Admin account created successfully!")
            #admin = tk.Tk()
            #admin.destroy()
            #admin.title("SignUp Panel")
            
            #status_label = tk.Label(admin, text="Sign Up Successfull!", bg="green", fg="white")
            #status_label.place(x=50,y=90)
            #admin.update()
            
            
            return True
        else:
            cursor = con.cursor()
            sql = "select * from admin_data where username=%s and password=%s"
            val = (username, password)
            cursor.execute(sql,val)
            result = cursor.fetchone()
            if result:
                print("Login Status: Login Success")
                return True
            else:
                print("Login Status: Login Failure")
                return False
        
    except mysql.connector.Error as err:
        print("Database Status: There was an error connecting to the database")
        return False
    finally:
        if con:
            con.close()
            print("Database Status: Connection Closed Successfully")
            #print()
def signup():
    username = signup_username.get()
    password = signup_password.get()

    if verifyAdmin(username, password, True):
        print("Signup Success", "Admin account created successfully!")
    else:
        print("Signup Failed", "Failed to create admin account.")

def open_signup_form():
    # Create a new Tkinter window for the sign-up form
    signup_form = tk.Toplevel()
    signup_form.title("Sign Up")
    signup_form.geometry("300x200")

    # Create labels and entry widgets for username and password fields
    signup_username_label = tk.Label(signup_form, text="Username1:")
    signup_username_label.pack()
    global signup_username
    signup_username = tk.Entry(signup_form)
    signup_username.pack()

    signup_password_label = tk.Label(signup_form, text="Password1:")
    signup_password_label.pack()
    global signup_password
    signup_password = tk.Entry(signup_form, show="*")
    signup_password.pack()

    # Create a button to trigger the sign-up process
    signup_button = tk.Button(signup_form, text="Sign Up", command=signup)
    signup_button.pack()
    

def adminWindow():
    '''
    In this function i have created a login window for admin
    which have input fields such as username and password as well as submit button to submit the form
    '''

    # creating a new Tkinter window
    admin = tk.Tk()
    admin.title("Admin Panel")
    icon = PhotoImage(file = "C:\\Users\\AWI-Guest\\Desktop\\ActivateWork\\Projects\\Zoom\\Images\\Project-Icon.png")
    admin.iconphoto(False, icon)

    # setting window on the center of the screen
    window_width = 1000
    window_height = 500

    screen_width = admin.winfo_screenwidth()
    screen_height = admin.winfo_screenheight()

    x = (screen_width/2) - (window_width/2)
    y = (screen_height/2) - (window_height/2)

    admin.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))
    admin.resizable(width=False, height=False)

    admin.configure(bg='white')
    
    # setting canvas frame - start
    canvas = Canvas(admin, width=window_width, height=40, bg="blue")
    canvas.create_text(470, 20, text="Admin Login", fill="white", font=("Helvetica", 12, "bold"))
    canvas.pack()
    # setting canvas frame - end

    #canvas = Canvas(width=600, height=145)
    #canvas.configure(bg="white")
    #canvas.place(x=350,y=150)
    #image = PhotoImage(file="C:\\Users\\AWI-Guest\\Desktop\\ActivateWork\\Projects\\Zoom\\Images\\sbmp.png")
    #cropped_image = image.subsample(2, 2)
    #canvas.create_image(0, 0, anchor=NW, image=cropped_image)

    global username_text  # Declare as global to make it accessible to other functions
    global password_text  # Declare as global to make it accessible to other functions


    # setting login fields --> Username & Password

    username_label = tk.Label(admin, text="Username: ", bg="white",font=("Helvatica", 10, "bold"))
    username_label.pack()
    username_text = tk.Entry(admin, width=20, font=("Helvetica", 11), relief="groove", bd=2)
    username_text.place(x=100,y=150)
    username_label.place(x=20,y=150)

    password_label = tk.Label(admin, text="Password: ", bg="white",font=("Helvatica", 10, "bold"))
    password_label.pack()
    password_text = tk.Entry(admin, show="*", width=20, font=("Helvetica", 11), relief="groove", bd=2)
    password_text.place(x=100,y=220)
    password_label.place(x=20,y=220)
    

    def login():
        '''
        this function displays the label on screen to notify the user weather it is a success or a failure
        the result is retrned to "verifyAdmin()" and it checks wether the admin data exists or not
        ''' 
        result = verifyAdmin(username_text.get(), password_text.get(),False)
        if result:
            status_label = tk.Label(admin, text="You have been successfully logged in!", bg="green", fg="white")
            status_label.place(x=50,y=90)
            admin.update()
            engine.say("Login Successful")
            engine.runAndWait()
            admin.after(500, admin.destroy)
            m.window()

        else:
            status_label = tk.Label(admin, text="There was an error logging you in!", bg="red", fg="white")
            status_label.place(x=60,y=90)
            admin.update()
            engine.say("Login failed please enter correct id or password")
            engine.runAndWait()

    # adding a submit button 
    submit_button = tk.Button(admin, text="Submit", command=login, width=10, bg="blue", fg="white") # the command attribute will run the "login()" function
    submit_button.place(x=140,y=285)
    #sign_up_button = tk.Button(admin, text="Sign Up",width=10, bg="blue", fg="white")
    #sign_up_button.place(x=40,y=350)
    
    signup_button = tk.Button(admin, text="Sign Up", command=open_signup_form,width=10, bg="blue", fg="white")
    signup_button.pack()
    signup_button.place(x=40,y=285)

    admin.mainloop()

# Calling the function 
adminWindow()