TK_SILENCE_DEPRECATION=1
import tkinter as tk
from tkinter import ttk
import os
from dotenv import load_dotenv
import requests

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
root = tk.Tk()

def login(data):
    response = requests.post(f'{BASE_URL}/user/login', json=data
    )
    print(response.status_code)
    
    

root.title("TaskPal")

email = tk.StringVar()
email.set("test21@com.com")

email_label = ttk.Label(root, text="Email")
email_label.pack()
email_entry = ttk.Entry(root, textvariable=email, width=30)
email_entry.pack()


password = tk.StringVar()
password.set("testfield1")
password_label = ttk.Label(root, text="Password")
password_label.pack()
password_entry = ttk.Entry(root, textvariable=password, width=30)
password_entry.pack(padx=10)
button = ttk.Button(root, text="Login", command=lambda email=email, password=password:login({
        "email":email.get(),
        "password":password.get()
}))
button.pack(padx=10)

root.mainloop()