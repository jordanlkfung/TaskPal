TK_SILENCE_DEPRECATION=1
import tkinter as tk
from tkinter import ttk, font
import os
from dotenv import load_dotenv
import requests
from responses import CollectionResponse
from typing import List

import sv_ttk

load_dotenv()
prod = True
api_version = "v1"
BASE_URL = os.getenv("BASE_URL") if prod else "http://127.0.0.1:8000/api/"+api_version
root = tk.Tk()


    
root.title("TaskPal")


class urls:
    def __init__(self):
        self.user = f'{BASE_URL}/user'
        self.collection = f'{BASE_URL}/collection'
        self.task = f'{BASE_URL}/task'

class app:
    def __init__(self, root:tk.Tk):
        self.root = root
        self.token = None
        self.nav = ttk.Frame(self.root)
        self.content = ttk.Frame(self.root)
        self.content.place(relwidth=1, relheight=1)
        self.initScreen()
    
    def loginfunc(self, email, password):
        response = requests.post(f'{BASE_URL}/user/login', json={"email":email, 'password':password})
        self.token = response.headers['Authorization']
        if self.token:
            self.collectionsScreen()

    def signupfunc(self, email, password):
        response = requests.post(f'{BASE_URL}/user/signup', json={"email":email, 'password':password})
        self.token = response.headers['Authorization']
        if self.token:
            self.collectionsScreen()

    def initScreen(self):
        def toLoginForm():
            self.userForm("Login", self.loginfunc)
        for i in self.content.winfo_children():
            i.destroy()
        title_font = font.Font(family='Helvetica', size=24, weight='bold')
        # ttk.Label(self.content,text="Welcome To TaskPal").pack(pady=20, anchor='center')
        # ttk.Button(self.content, text="Login", command=toLoginForm).pack(pady=10, anchor='center')
        # ttk.Button(self.content, text="Sign Up", command=lambda x= "Sign Up": self.userForm(x, self.signupfunc)).pack(pady=10, anchor='center')

        
        ttk.Label(self.content, text="Welcome To TaskPal", font=title_font).place(relx=0.5, rely=0.3, anchor="center", )
        ttk.Button(self.content, text="Login", command=toLoginForm).place(relx=0.5, rely=0.4, anchor="center")
        ttk.Button(self.content, text="Sign Up", command=lambda x="Sign Up": self.userForm(x, self.signupfunc)).place(relx=0.5, rely=0.5, anchor="center")

    def userForm(self, buttonText, func):
        root =self.content
        for i in self.content.winfo_children():
            i.destroy()
        ttk.Button(self.content,text="back", command=self.initScreen).pack()
        ttk.Label(self.content, text=buttonText).pack()
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
        button = ttk.Button(root, text=buttonText, command=lambda x=email.get(), y=password.get():func(x,y))
        button.pack(padx=10)
    
    def collectionsScreen(self):
        for i in self.content.winfo_children():
            i.destroy()
        loading = ttk.Label(self.content, text="Loading")
        loading.pack()

        response = requests.get(f'{BASE_URL}/collection/get',
                                   headers={"Authorization":self.token})
        collections:List[CollectionResponse] = response.json()
        print(collections)
        loading.destroy()
        
        for i, collection in enumerate(collections):
            ttk.Label(self.content, text=collection.name).grid(column=0, row=i)
            ttk.Button(self.content, text="View").grid(column=1, row=i)
    
    def taskScreen(self):
        pass
    
    def createScreen():
        pass
            
app(root)
sv_ttk.use_light_theme()

root.mainloop()