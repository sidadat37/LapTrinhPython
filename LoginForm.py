import tkinter as tk
from tkinter import messagebox
import mysql.connector
import main

class LoginApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('300x200')
        self.root.title("Login")
        self.root.configure(bg='light blue')

        title_label = tk.Label(self.root, text= "Login", fg= "red", font=("cambria",16), width=25, bg='light blue')
        title_label.pack(pady=10)

        username_label = tk.Label(self.root, text="Username", bg='light blue')
        username_label.pack()

        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        password_label = tk.Label(self.root, text="Password", bg='light blue')
        password_label.pack()

        self.password_entry = tk.Entry(self.root, show='*')
        self.password_entry.pack()

        submit_button = tk.Button(self.root, text="Submit", command=self.check_credentials, bg='light green')
        submit_button.pack(pady=10)

        self.root.mainloop()

    def check_credentials(self):
        try:
            # Establish a connection to the database
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="26072003",
                database="sneakershop"
            )

            # Create a cursor object
            mycursor = mydb.cursor()

            # SQL query to check the credentials
            sql = "SELECT * FROM users WHERE username = %s AND password = %s"
            val = (self.username_entry.get(), self.password_entry.get())

            # Execute the query
            mycursor.execute(sql, val)

            # Fetch the result
            result = mycursor.fetchone()

            if result:
                messagebox.showinfo("Login info", "Welcome " + str(result[1]) + "!")
                self.root.destroy()
                main.Main()
            else:
                messagebox.showinfo("Login info", "Incorrect credentials")

            # Close the connection
            mydb.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database error", "Something went wrong: {}".format(err))

if __name__ == "__main__":
    app = LoginApp()
