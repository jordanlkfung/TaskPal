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
        root.geometry("600x500")
        self.root = root
        self.token = None
        self.nav = ttk.Frame(self.root)
        self.content = ttk.Frame(self.root)
        self.content.place(relwidth=1, relheight=1)
        self.initScreen()
    
    def loginfunc(self, email = "test21@com.com", password = 'testfield1'):
        print("request to login")
        response = requests.post(f'{BASE_URL}/user/login', json={"email":email, 'password':password})
        print("Login response")
        if response.status_code == 200:
            self.token = response.headers['Authorization']
            self.collectionsScreen()
        else:
            print("Login response code:" + response.status_code)

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

        
        ttk.Label(self.content, text="Welcome To TaskPal", font=title_font).place(relx=0.5, rely=0.3, anchor="center")
        ttk.Button(self.content, text="Login", command=toLoginForm, padding=5, width=25).place(relx=0.5, rely=0.4, anchor="center")
        ttk.Button(self.content, text="Sign Up", padding=5, width=25, command=lambda x="Sign Up": self.userForm(x, self.signupfunc)).place(relx=0.5, rely=0.5, anchor="center")

    def userForm(self, buttonText, func):
        root = self.content
        for widget in root.winfo_children():
            widget.destroy()

        ttk.Label(root, text=buttonText, font=("Arial", 20, "bold")).place(relx=0.5, rely=0.1, anchor="center")

        ttk.Label(root, text="Email Address:", font=("Arial", 14)).place(relx=0.5, rely=0.28, anchor="center")
        email = tk.StringVar()
        ttk.Entry(root, textvariable=email, width=30).place(relx=0.5, rely=0.34, anchor="center")

        ttk.Label(root, text="Password:", font=("Arial", 14)).place(relx=0.5, rely=0.43, anchor="center")
        password = tk.StringVar()
        ttk.Entry(root, textvariable=password, width=30, show="*").place(relx=0.5, rely=0.47, anchor="center")

        ttk.Button(
            root,
            text=buttonText,
            width=25,
            padding=5,
            command=func
            # command=lambda x=email.get(), y=password.get(): func(x, y)
        ).place(relx=0.5, rely=0.58, anchor="center")

        if buttonText == 'Sign Up':
            ttk.Button(self.content,text="Have an Account? Click to Login In", width=25, padding=5, command=lambda x='Login': self.userForm(x, self.loginfunc)).place(relx=0.5, rely=0.65, anchor="center")
        else:
            ttk.Button(self.content,text="No account? Click to Sign Up", width=25, padding=5, command=lambda x='Sign Up': self.userForm(x, self.signupfunc)).place(relx=0.5, rely=0.65, anchor="center")

    
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
        ttk.Label(root, text="Collections", font=("Helvetica", 22, "bold")).pack(pady=10)
        # .place(relx=0.5, rely=0.1, anchor="center")

        tframe = ttk.Frame(self.content)
        tframe.pack(pady=45)

        ttk.Label(tframe, text="Name").grid(column=0, row=0, padx=(0,15), pady=(0,7))
        ttk.Label(tframe, text="Actions").grid(column=1, row=0, pady=(0,7))
        for i, collection in enumerate(collections):
            print(collection)
            ttk.Label(tframe, text=collection['name']).grid(column=0, row=i+1, padx=(0,15))
            actions = ttk.Frame(tframe)
            actions.grid(column=1, row=i+1)
            ttk.Button(actions, text="View", command= lambda x=collection['id']: self.taskScreen(x)).grid(column=0, row=0)
            ttk.Button(actions, text="Delete").grid(column=1, row=0)
            
    
    def taskScreen(self, collectionId):
        response = requests.get(f'{BASE_URL}/collection/task/{collectionId}',
                                 headers={"Authorization":self.token})
        
        tasks = response.json()
    def createScreen():
        pass
            
app(root)
sv_ttk.use_light_theme()

root.mainloop()