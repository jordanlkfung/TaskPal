TK_SILENCE_DEPRECATION=1
import tkinter as tk
from tkinter import ttk, font
import os
from dotenv import load_dotenv
import requests
from typing import List
import sv_ttk
from utils import get_priority_str, get_priority_val, datetime_to_mdy, str_to_val, valid_email

load_dotenv()
prod = True
api_version = "v1"
BASE_URL = os.getenv("BASE_URL") if prod else "http://127.0.0.1:8000/api/"+api_version
root = tk.Tk()


    
root.title("TaskPal")


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
        if response.status_code == 200:
            self.token = response.headers['Authorization']
            # self.collectionsScreen()
        else:
            print(f"Login response code: {response.status_code}")
            # error_func(response.status_code, response['detail'])
        return response.status_code

    def signupfunc(self, email, password):
        response = requests.post(f'{BASE_URL}/user/signup', json={"email":email, 'password':password})
        self.token = response.headers['Authorization']
        if response.status_code == 201:
            self.token = response.headers['Authorization']
            # self.collectionsScreen()
        return response.status_code

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

        error_msg = None
        def setErrorMsg(message):
            error_msg = ttk.Label(self.content, text=message, foreground='red')
            error_msg.place(relx=.5, rely=.73, anchor='center')
        
        def removeErrorMsg():
            if error_msg:
                error_msg.destroy()
        
        def sumbit():
            removeErrorMsg()
            user_email = email.get()
            user_password = password.get()
            
            # if not user_email or not user_password:
            #     setErrorMsg("Missing Email or Password")
            #     return

            # res = func(user_email, user_password)
            res = func()
            if res == 200 or res == 201:
                self.collectionsScreen()
            elif res >=400 and res <500:
                setErrorMsg("Invalid Email or Password")
            else:
                setErrorMsg("Server Error, please try again")

        def checkEmail(input):
            if valid_email(input):
                removeErrorMsg()
            else:
                setErrorMsg("Invalid Email Format")

        ttk.Label(root, text=buttonText, font=("Arial", 20, "bold")).place(relx=0.5, rely=0.1, anchor="center")

        ttk.Label(root, text="Email Address:", font=("Arial", 14)).place(relx=0.5, rely=0.28, anchor="center")
        email = tk.StringVar()
        ttk.Entry(root, textvariable=email, width=30).place(relx=0.5, rely=0.34, anchor="center")

        ttk.Label(root, text="Password:", font=("Arial", 14)).place(relx=0.5, rely=0.43, anchor="center")
        password = tk.StringVar()
        ttk.Entry(root, textvariable=password, width=30, show="*").place(relx=0.5, rely=0.49, anchor="center")

        ttk.Button(
            root,
            text=buttonText,
            width=25,
            padding=5,
            command=sumbit
        ).place(relx=0.5, rely=0.58, anchor="center")

        if buttonText == 'Sign Up':
            ttk.Button(self.content,text="Have an Account? Click to Login In", width=25, padding=5, command=lambda x='Login': self.userForm(x, self.loginfunc)).place(relx=0.5, rely=0.67, anchor="center")
        else:
            ttk.Button(self.content,text="No account? Click to Sign Up", width=25, padding=5, command=lambda x='Sign Up': self.userForm(x, self.signupfunc)).place(relx=0.5, rely=0.67, anchor="center")

    
    def collectionsScreen(self):
        def logout_func():
            self.token = None
            self.initScreen()
        for i in self.content.winfo_children():
            i.destroy()
        loading = ttk.Label(self.content, text="Loading..", font=("Helvetica", 22, "bold"))
        loading.place(relx=.5, rely=.5, anchor="center")

        response = requests.get(f'{BASE_URL}/collection/get',
                                   headers={"Authorization":self.token})
        collections = response.json()
        loading.destroy()
        for i in range(3):
            self.content.grid_columnconfigure(i, weight=1)
        title = ttk.Label(self.content, text="My Collections", font=("Helvetica", 22, "bold"))
        title.grid(row=0, column=0, pady=15, columnspan=3, sticky='nsew')
        title.configure(anchor='center')

        ttk.Button(self.content, text="Logout", command=logout_func).place(relx=.99, rely=.01, anchor='ne')


        ttk.Label(self.content, text="Name", font=("Helvetica", 18, "bold")).grid(column=0, row=1, padx=(5, 20), pady=(0, 7))
        ttk.Label(self.content, text="Number of Tasks", font=("Helvetica", 18, "bold")).grid(column=1, row=1, pady=(0, 7))
        # tempframe = ttk.Frame(self.content)
        # tempframe.grid(column=2, row=1, pady=(0, 7), sticky="ew", columnspan=1)
        ttk.Label(self.content, text="Actions", font=("Helvetica", 18, "bold")).grid(row=1, column=2)

        for i, collection in enumerate(collections):
            ttk.Label(self.content, text=collection['name']).grid(column=0, row=i+2, padx=(5, 20))
            ttk.Label(self.content, text=collection['Number of Tasks']).grid(column=1, row=i+2)
            
            actions = ttk.Frame(self.content)
            actions.grid(column=2, row=i+2, columnspan=1)
            actions.grid_columnconfigure(0, weight=1)
            actions.grid_columnconfigure(1, weight=1)
            actions.grid_columnconfigure(2, weight=1)
            ttk.Button(actions, text="View", command=lambda x=collection['id'], y=collection['name']: self.taskScreen(x, y)).grid(column=0, row=0, padx=(0, 5), sticky='nsew')
            ttk.Button(actions, text="Edit", command=lambda x=collection['id']: self.updateCollectionScreen(x)).grid(column=1, row=0, padx=5, sticky='nsew')
            
            ttk.Button(actions, text="Delete", command=lambda x=collection['id']: x).grid(column=2, row=0, padx=(5, 0), sticky='nsew')
            
        ttk.Button(self.content, text="Create New Collection", command=self.createCollectionScreen).place(relx=.5, rely=.9, anchor='center')

    def taskScreen(self, collectionId, collection_name):
        for i in self.content.winfo_children():
            i.destroy()
        response = requests.get(f'{BASE_URL}/task/{collectionId}',
                                 headers={"Authorization":self.token})
        
        tasks = response.json()
        title = ttk.Label(self.content, text=collection_name, font=("Helvetica", 22, "bold"))
        title.grid(row=0, column=0, pady=15, columnspan=6, sticky='nsew')
        title.configure(anchor='center')


        for i in range(5):
            self.content.grid_columnconfigure(i, weight=1)


        ttk.Label(self.content, text="Task Name").grid(column=0, row=1, padx=(5, 20), pady=(0, 7),  columnspan=2)
        ttk.Label(self.content, text="Priority").grid(column=2, row=1, pady=(0, 7),  columnspan=1)
        ttk.Label(self.content, text="Creation date").grid(column=3, row=1, pady=(0, 7))
        ttk.Label(self.content, text="Status").grid(column=4, row=1, pady=(0, 7), columnspan=1)
        # ttk.Label(self.content, text="Actions").grid(column=5, row=1, columnspan=2, pady=(0,7))
        def markComplete(task, index):
            print("request to complete")
            response = requests.patch(f"{BASE_URL}/task/",headers={"Authorization": self.token}, 
                                      json={"name":task['name'], 
                                            "id":task['id'], 
                                            'completed':not task['completed'], 
                                            'priority':task['priority']})
            print(f"{response.status_code} code received")
            if response.status_code == 204:
                # tasks[i]['completed'] = True
                # self.content.update()
                self.taskScreen(collectionId, collection_name)
            else:
                print("error")
                print(response.json())
        def deleteTask(id):
            response = requests.delete(f"{BASE_URL}/task/{id}",
                                       headers={"Authorization":self.token})
            if response.status_code == 204:
                self.taskScreen(collectionId, collection_name)
            else:
                print("error")
                print(response.json())
            
        for i, task in enumerate(tasks):
            ttk.Label(self.content, text=task['name']).grid(column=0, row=i+2, padx=(5, 20), columnspan=2)
            ttk.Label(self.content, text=get_priority_str(task['priority'])).grid(column=2, row=i+2)
            ttk.Label(self.content, text=datetime_to_mdy(task['creation_date'])).grid(column=3, row=i+2)
            text = "Complete"
            if task['completed']:
                text = 'Completed'
            ttk.Button(self.content, text=text, command=lambda x= task: markComplete(x, i)).grid(column=4, row=i+2, columnspan=1, sticky='nsew', padx=5)
            
            ttk.Button(self.content, text="Edit", command= lambda x = task: self.updateTaskScreen(task)).grid(column=5, row=i+2, sticky='nsew', padx=5)
            ttk.Button(self.content, text="Delete", command=lambda x=task['id']: deleteTask(x)).grid(column=6, row=i+2, padx=(5,10), sticky='nsew')
            
        ttk.Button(self.content, text="Add Task", command=lambda x=collectionId, y=collection_name: self.createTaskScreen(x, y)).place(relx=.5, rely=.9, anchor='center')

        

    def createCollectionScreen(self):
        def createCollection():
            if collection_name.get():
                print("request to add collection")
                response = requests.post(f'{BASE_URL}/collection/add', json={"name":collection_name.get()}, headers={"Authorization":self.token})

                new_collection = response.json()
                print(f'{response.status_code} received')
                if response.status_code == 201:
                    self.taskScreen(self, new_collection['collection_id'], collection_name.get())
        for i in self.content.winfo_children():
            i.destroy()

        ttk.Label(self.content, text="Create Collection", font=("Helvetica", 22, "bold")).place(relx=.5, rely=.25, anchor='center')

        ttk.Label(self.content, text="Enter Collection Name", font=("Helvetica", 14)).place(relx=.5, rely=.41, anchor='center')
        collection_name = tk.StringVar()

        ttk.Entry(self.content, textvariable=collection_name).place(relx=.5, rely=.47, relheight=.07, anchor='center')

        ttk.Button(self.content, text="Create", width=15, command=createCollection).place(relx=.5, rely=.6, anchor='center')
    

    def createTaskScreen(self, collection_id, collection_name):
        for i in self.content.winfo_children():
            i.destroy()
        
        def return_to_tasks():
            self.taskScreen(collection_id, collection_name)
        def createTaskReq():
            print("Create Task Request")
            response = requests.post(f'{BASE_URL}/task/add',
                                     headers={"Authorization":self.token},
                                     json={"collection_id":collection_id,
                                           "name":name.get(),
                                           "priority":get_priority_val(priority.get())})
            
            print(f"{response.status_code} code received")
            if response.status_code == 201:
                return_to_tasks()
            
        # ttk.Label(self.content, text=collection_name, font=("Helvetica", 22, "bold")).place(relx=0.5, rely=0.1, anchor='center')
        ttk.Label(self.content, text="Add Task", font=("Helvetica", 22, "bold")).place(relx=0.5, rely=0.18, anchor='center')

        name = tk.StringVar()
        priority = tk.StringVar()

        ttk.Label(self.content, text='Task name').place(relx=0.5, rely=0.3, anchor='center')
        ttk.Entry(self.content, textvariable=name, width=34).place(relx=0.5, rely=0.35, anchor='center')

        ttk.Label(self.content, text='Priority').place(relx=0.5, rely=0.45, anchor='center')

        ttk.Combobox(self.content, textvariable=priority, state='readonly', values=list(str_to_val.keys()), width=30).place(relx=0.5, rely=0.5, anchor='center')

        ttk.Button(self.content, text="Cancel", command=return_to_tasks, width=28).place(relx=0.5, rely=0.6, anchor='center')
        ttk.Button(self.content, text="Add Task", command=createTaskReq, width=28).place(relx=0.5, rely=0.67, anchor='center')

    def updateCollectionScreen(self,collection_id):
        for i in self.content.winfo_children():
            i.destroy()
        error_msg = None
        def remove_error_msg():
            nonlocal error_msg
            if error_msg:
                error_msg.destroy()
                error_msg = None
        def set_error_msg(message):
            nonlocal error_msg
            error_msg = ttk.Label(self.content, text= message, foreground='red')
            error_msg.place(relx=.5, rely=.55, anchor='center')

        def update():
            remove_error_msg()
            new_name = collection_name.get()
            if new_name:
                print("request to add collection")
                response = requests.patch(f'{BASE_URL}/collection/', json={"name":new_name, "id":collection_id}, headers={"Authorization":self.token})

                new_collection = response.json()
                print(f'{response.status_code} received')
                if response.status_code == 201:
                    self.collectionsScreen()
                if response.status_code <500:
                    set_error_msg("Invalid Name")
                else:
                    set_error_msg("Server Error, Please try again")
            else:
                set_error_msg("Collection Has to Have a Name")
                
        for i in self.content.winfo_children():
            i.destroy()

        ttk.Label(self.content, text="Modify Collection", font=("Helvetica", 22, "bold")).place(relx=.5, rely=.25, anchor='center')
        ttk.Label(self.content, text="New Name", font=("Helvetica", 14)).place(relx=.5, rely=.41, anchor='center')
        collection_name = tk.StringVar()

        name_entry = ttk.Entry(self.content, textvariable=collection_name)
        name_entry.place(relx=.5, rely=.47, relheight=.07, anchor='center')
        name_entry.bind('<Key>', lambda x: remove_error_msg())
    

        ttk.Button(self.content, text="Cancel", width=15, command=self.collectionsScreen).place(relx=.5, rely=.6, anchor='center')
        ttk.Button(self.content, text="Update", width=15, command=update).place(relx=.5, rely=.68, anchor='center')

    def updateTaskScreen(self, task):
        for i in self.content.winfo_children():
            i.destroy()

        error_msg = None
        def remove_error():
            if error_msg:
                error_msg.destroy()
                error_msg = None
        def set_error_msg_name(message):
            error_msg = ttk.Label(self.content, foreground='red', text=message)
            error_msg.place(relx=.5)
        
            
        def updateTask():
            response = requests.patch()
        print(task)
        ttk.Label(self.content, text="Edit Task", font=("Helvetica", 22, "bold")).place(relx=.5, rely=.25, anchor='center')
        ttk.Label(self.content, text="Task Name", font=("Helvetica", 14)).place(relx=.5, rely=.34, anchor='center')
        collection_name = tk.StringVar(master=self.content, value=task['name'])

        name_entry = tk.Entry(self.content, textvariable=collection_name, width=25)
        name_entry.place(relx=.5, rely=.4, relheight=.07, anchor='center')
        name_entry.update()
        name_entry.update_idletasks()
        name_entry.bind('<Key>', lambda x: remove_error())

        ttk.Label(self.content, text='Priority').place(relx=0.5, rely=0.48, anchor='center')

        combobox = ttk.Combobox(self.content, state='readonly', values=list(str_to_val.keys()), width=20)
        combobox.set(get_priority_str(task['priority']).upper())
        combobox.place(relx=0.5, rely=0.54, anchor='center')
        
        ttk.Button(self.content, text="Cancel", width=15, command=self.collectionsScreen).place(relx=.5, rely=.7, anchor='center')
        ttk.Button(self.content, text="Update", width=15, command=updateTask).place(relx=.5, rely=.75, anchor='center')

app(root)
sv_ttk.use_light_theme()

root.mainloop()