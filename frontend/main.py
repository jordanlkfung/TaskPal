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
        # self.taskScreen(1,'Collection')
        self.initScreen()

    def loginfunc(self, email = "test21@com.com", password = 'testfield1'):
        print("request to login")
        response = requests.post(f'{BASE_URL}/user/login', json={"email":email, 'password':password})
        print("Login response")
        if response.status_code == 200:
            self.token = response.headers['Authorization']
            self.collectionsScreen()
        else:
            print(f"Login response code: {response.status_code}")

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

        
        ttk.Label(self.content, text="Welcome To TaskPal", font=title_font).place(relx=0.5, rely=0.3, anchor="center")
        ttk.Button(self.content, text="Login", command=toLoginForm, padding=5, width=25).place(relx=0.5, rely=0.45, anchor="center")
        ttk.Button(self.content, text="Sign Up", padding=5, width=25, command=lambda x="Sign Up": self.userForm(x, self.signupfunc)).place(relx=0.5, rely=0.55, anchor="center")

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
        collections = response.json()

        loading.destroy()
        ttk.Label(self.content, text="My Collections", font=("Helvetica", 22, "bold")).grid(row=0, column=1, pady=15)


        self.content.grid_columnconfigure(0, weight=1, uniform="equal")
        self.content.grid_columnconfigure(1, weight=1, uniform="equal")
        self.content.grid_columnconfigure(2, weight=1, uniform="equal")

        ttk.Label(self.content, text="Name").grid(column=0, row=1, padx=(5, 20), pady=(0, 7), sticky="ew", columnspan=1)
        ttk.Label(self.content, text="Number of Tasks").grid(column=1, row=1, pady=(0, 7), sticky="ew", columnspan=1)
        tempframe = ttk.Frame(self.content)
        tempframe.grid(column=2, row=1, pady=(0, 7), sticky="ew", columnspan=1)
        ttk.Label(tempframe, text="Actions").grid()

        for i, collection in enumerate(collections):
            ttk.Label(self.content, text=collection['name']).grid(column=0, row=i+2, padx=(5, 20), sticky="ew", columnspan=1)
            ttk.Label(self.content, text=collection['Number of Tasks']).grid(column=1, row=i+2, sticky="ew", columnspan=1)
            
            actions = ttk.Frame(self.content)
            actions.grid(column=2, row=i+2, sticky="ew", columnspan=1)
            
            ttk.Button(actions, text="View", command=lambda x=collection['id'], y=collection['name']: self.taskScreen(x, y)).grid(column=0, row=0, padx=(0, 5))
            
            ttk.Button(actions, text="Delete", command=lambda x=collection['id']: x).grid(column=1, row=0, padx=(5, 0))
            
        ttk.Button(self.content, text="Create New Collection", command=self.createCollectionScreen).place(relx=.5, rely=.9, anchor='center')

    def taskScreen(self, collectionId, collection_name):
        response = requests.get(f'{BASE_URL}/collection/task/{collectionId}',
                                 headers={"Authorization":self.token})
        
        tasks = [{
            "id":1,
            "name":"task1",
            "priority":"NONE",
            "creation_date":"03/23/11",
            'completed': False
        }]
        ttk.Label(self.content, text=collection_name, font=("Helvetica", 22, "bold")).grid(row=0, column=2, pady=15)


        self.content.grid_columnconfigure(0, weight=1, uniform="equal")
        self.content.grid_columnconfigure(1, weight=1, uniform="equal")
        self.content.grid_columnconfigure(2, weight=1, uniform="equal")
        self.content.grid_columnconfigure(3, weight=1, uniform="equal")
        self.content.grid_columnconfigure(4, weight=1, uniform="equal")

        ttk.Label(self.content, text="Task Name").grid(column=0, row=1, padx=(5, 20), pady=(0, 7), sticky="ew", columnspan=1)
        ttk.Label(self.content, text="Priority").grid(column=1, row=1, pady=(0, 7), sticky="ew", columnspan=1)
        ttk.Label(self.content, text="Creation date").grid(column=2, row=1, pady=(0, 7), sticky="ew", columnspan=1)
        ttk.Label(self.content, text="Status").grid(column=3, row=1, pady=(0, 7), sticky="ew", columnspan=1)
        
        # tempframe = ttk.Frame(self.content)
        # tempframe.grid(column=3, row=1, pady=(0, 7), sticky="ew", columnspan=1)
        # ttk.Label(tempframe, text="Actions").grid()
        def markComplete():
            response = requests.post()

        for i, task in enumerate(tasks):
            ttk.Label(self.content, text=task['name']).grid(column=0, row=i+2, padx=(5, 20), sticky="ew", columnspan=1)
            ttk.Label(self.content, text=task['priority']).grid(column=1, row=i+2, sticky="ew", columnspan=1)
            ttk.Label(self.content, text=task['creation_date']).grid(column=2, row=i+2, sticky="ew", columnspan=1)
            text = "Mark Completed"
            command = markComplete
            if task['completed']:
                command = lambda x: x
                text = 'Completed'
            ttk.Button(self.content, text=text, command=lambda x= task['id']: command(x)).grid(column=3, row=i+2, sticky="ew", columnspan=1)
            
            
            ttk.Button(self.content, text="Delete", command=lambda x=task['id']: x).grid(column=4, row=i+2, columnspan=1)
            
        ttk.Button(self.content, text="Create New Collection", command=self.createCollectionScreen).place(relx=.5, rely=.9, anchor='center')

        

    def createCollectionScreen(self):
        def createCollection():
            if collection_name.get():
                response = requests.post(f'{BASE_URL}/collection/add', json={"name":collection_name.get()})

                new_collection = response.json()

                if response.status_code == 201:
                    self.taskScreen(self, new_collection['collection_id'], collection_name.get())
        for i in self.content.winfo_children():
            i.destroy()

        ttk.Label(self.content, text="Create Collection", font=("Helvetica", 22, "bold")).place(relx=.5, rely=.25, anchor='center')

        ttk.Label(self.content, text="Enter Collection Name", font=("Helvetica", 14)).place(relx=.5, rely=.41, anchor='center')
        collection_name = tk.StringVar()

        ttk.Entry(self.content, textvariable=collection_name).place(relx=.5, rely=.47, relheight=.07, anchor='center')

        ttk.Button(self.content, text="Create", width=15, command=createCollection).place(relx=.5, rely=.6, anchor='center')
    

    def createTaskScreen(self, collection_id):
        for i in self.content.winfo_children():
            i.destroy()
        
        def createTaskReq():
            response = requests.post(f'{BASE_URL}/task/add',
                                     headers={"Authorization":self.token},
                                     json={"collection_id":collection_id,
                                           "name":name,
                                           "priority":priority})
            
        name = tk.StringVar()
        priority = tk.StringVar()
        ttk.Label(self.content, text='Task name').pack()
        ttk.Entry(self.content, textvariable=name).pack()
        ttk.Combobox(self.content, textvariable=priority, state='readonly', values=['NONE', 'LOW', 'MEDIUM','HIGH']).pack()
        ttk.Button(self.content, text="Add Task").pack()
app(root)
sv_ttk.use_light_theme()

root.mainloop()