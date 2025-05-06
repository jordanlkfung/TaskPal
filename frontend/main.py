TK_SILENCE_DEPRECATION=1
import tkinter as tk
from tkinter import ttk, font
import os
from dotenv import load_dotenv
import requests
from typing import List
import sv_ttk
from utils import get_priority_str, get_priority_val, datetime_to_mdy, str_to_val, valid_email
from datetime import datetime

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
        else:
            print(f"Login response code: {response.status_code}")
        return response.status_code

    def signupfunc(self, email, password):
        response = requests.post(f'{BASE_URL}/user/signup', json={"email":email, 'password':password})
        self.token = response.headers['Authorization']
        if response.status_code == 201:
            self.token = response.headers['Authorization']
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

            res = func(user_email, user_password)
            # res = func()
            if res == 200 or res == 201:
                self.collectionsScreen()
            elif res >=400 and res <500:
                setErrorMsg("Invalid Email or Password")
            else:
                setErrorMsg("Server Error, please try again")

        # def checkEmail(event):
        #     print(event.char)
        #     if valid_email(event):
        #         removeErrorMsg()
        #     else:
        #         setErrorMsg("Invalid Email")

        ttk.Label(root, text=buttonText, font=("Arial", 20, "bold")).place(relx=0.5, rely=0.1, anchor="center")

        ttk.Label(root, text="Email Address:", font=("Arial", 14)).place(relx=0.5, rely=0.28, anchor="center")
        email = tk.StringVar()
        email_entry = ttk.Entry(root, textvariable=email, width=30)
        email_entry.place(relx=0.5, rely=0.34, anchor="center")
        # email_entry.bind('<Key>', checkEmail)

        ttk.Label(root, text="Password:", font=("Arial", 14)).place(relx=0.5, rely=0.43, anchor="center")
        password = tk.StringVar()
        ttk.Entry(root, textvariable=password, width=30, show="*").place(relx=0.5, rely=0.49, anchor="center")

        ttk.Button(root, text=buttonText, width=25, padding=5, command=sumbit).place(relx=0.5, rely=0.58, anchor="center")

        if buttonText == 'Sign Up':
            ttk.Button(self.content,text="Have an Account? Click to Login In", width=25, padding=5, command=lambda x='Login': self.userForm(x, self.loginfunc)).place(relx=0.5, rely=0.67, anchor="center")
        else:
            ttk.Button(self.content,text="No account? Click to Sign Up", width=25, padding=5, command=lambda x='Sign Up': self.userForm(x, self.signupfunc)).place(relx=0.5, rely=0.67, anchor="center")

    

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

        def markComplete(task, index):
            print("request to complete")
            response = requests.patch(f"{BASE_URL}/task/",headers={"Authorization": self.token}, 
                                      json={"name":task['name'], 
                                            "id":task['id'], 
                                            'completed':not task['completed'], 
                                            'priority':task['priority']})
            print(f"{response.status_code} code received")
            if response.status_code == 204:
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
            text = "Pending"
            if task['completed']:
                text = 'Completed'
            ttk.Button(self.content, text=text, command=lambda x= task: markComplete(x, i)).grid(column=4, row=i+2, columnspan=1, sticky='nsew', padx=5)
            
            ttk.Button(self.content, text="Edit", command= lambda x = task: self.updateTaskScreen(x, (collectionId, collection_name))).grid(column=5, row=i+2, sticky='nsew', padx=5)
            ttk.Button(self.content, text="Delete", command=lambda x=task['id']: deleteTask(x)).grid(column=6, row=i+2, padx=(5,10), sticky='nsew')
            
        ttk.Button(self.content, text="Add Task", command=lambda x=collectionId, y=collection_name: self.createTaskScreen(x, y)).place(relx=.5, rely=.9, anchor='center')
        ttk.Button(self.content, text="Back", command=self.collectionsScreen).place(relx=.5, rely=.95, anchor='center')

    def createCollectionScreen(self):
        def createCollection():
            if collection_name.get():
                print("request to add collection")
                response = requests.post(f'{BASE_URL}/collection/add', json={"name": collection_name.get()},
                                         headers={"Authorization": self.token})
                new_collection = response.json()
                print(f'{response.status_code} received')
                if response.status_code == 201:
                    self.taskScreen(new_collection['collection_id'], collection_name.get())

        for i in self.content.winfo_children():
            i.destroy()

        ttk.Label(self.content, text="Create Collection", font=("Helvetica", 22, "bold")).place(relx=.5, rely=.25,
                                                                                                anchor='center')

        ttk.Label(self.content, text="Enter Collection Name", font=("Helvetica", 14)).place(relx=.5, rely=.41,
                                                                                            anchor='center')
        collection_name = tk.StringVar()

        ttk.Entry(self.content, textvariable=collection_name).place(relx=.5, rely=.47, relheight=.07, anchor='center')

        ttk.Button(self.content, text="Create", width=15, command=createCollection).place(relx=.5, rely=.6,
                                                                                          anchor='center')
        ttk.Button(self.content, text="Back", width=15, command=self.collectionsScreen).place(relx=.5, rely=.7,
                                                                                              anchor='center')

    def collectionsScreen(self):
        def logout_func():
            self.token = None
            self.initScreen()

        def delete_collection(collection_id):
            response = requests.delete(f'{BASE_URL}/collection/{collection_id}',
                                       headers={"Authorization": self.token})
            if response.status_code == 204:
                self.collectionsScreen()
            else:
                print("Failed to delete collection")

        for i in self.content.winfo_children():
            i.destroy()
        loading = ttk.Label(self.content, text="Loading..", font=("Helvetica", 22, "bold"))
        loading.place(relx=.5, rely=.5, anchor="center")

        response = requests.get(f'{BASE_URL}/collection/get',
                                headers={"Authorization": self.token})
        collections = response.json()
        loading.destroy()
        for i in range(3):
            self.content.grid_columnconfigure(i, weight=1)
        title = ttk.Label(self.content, text="My Collections", font=("Helvetica", 22, "bold"))
        title.grid(row=0, column=0, pady=15, columnspan=3, sticky='nsew')
        title.configure(anchor='center')

        ttk.Button(self.content, text="Logout", command=logout_func).place(relx=.99, rely=.01, anchor='ne')
        ttk.Label(self.content, text="Name", font=("Helvetica", 18, "bold")).grid(column=0, row=1, padx=(5, 20),
                                                                                  pady=(0, 7))
        ttk.Label(self.content, text="Number of Tasks", font=("Helvetica", 18, "bold")).grid(column=1, row=1,
                                                                                             pady=(0, 7))
        ttk.Label(self.content, text="Actions", font=("Helvetica", 18, "bold")).grid(row=1, column=2)

        for i, collection in enumerate(collections):
            ttk.Label(self.content, text=collection['name']).grid(column=0, row=i + 2, padx=(5, 20))
            ttk.Label(self.content, text=collection['Number of Tasks']).grid(column=1, row=i + 2)

            actions = ttk.Frame(self.content)
            actions.grid(column=2, row=i + 2, columnspan=1)
            actions.grid_columnconfigure(0, weight=1)
            actions.grid_columnconfigure(1, weight=1)
            actions.grid_columnconfigure(2, weight=1)
            ttk.Button(actions, text="View",
                       command=lambda x=collection['id'], y=collection['name']: self.taskScreen(x, y)).grid(column=0, row=0, padx=(0, 5), sticky='nsew')
            ttk.Button(actions, text="Edit", command=lambda x=collection['id']: self.updateCollectionScreen(x)).grid(column=1, row=0, padx=5, sticky='nsew')
            ttk.Button(actions, text="Delete", command=lambda x=collection['id']: delete_collection(x)).grid(column=2, row=0, padx=(5, 0), sticky='nsew')

        # Bottom button row (Add, View, Sort)
        bottom_frame = ttk.Frame(self.content)
        bottom_frame.grid(row=len(collections) + 3, column=0, columnspan=3, pady=10)

        ttk.Button(bottom_frame, text="Create New Collection", command=self.createCollectionScreen).grid(row=0, column=0, padx=10)
        ttk.Button(bottom_frame, text="View By Priority", command=self.viewByPriorityScreen).grid(row=0, column=1, padx=10)
        ttk.Button(bottom_frame, text="Sort By Priority", command=self.sortByPriorityScreen).grid(row=0, column=2, padx=10)


        # Back button row
        ttk.Button(self.content, text="Back", command=lambda: self.userForm("Login", self.loginfunc)).grid(
            row=len(collections) + 4, column=0, columnspan=3, pady=10)


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
        ttk.Button(self.content, text="Back", command=return_to_tasks, width=28).place(relx=0.5, rely=0.75,
                                                                                       anchor='center')
    def updateCollectionScreen(self, collection_id):
        for i in self.content.winfo_children():
            i.destroy()  # ✅ Only do this ONCE

        error_msg = None

        def remove_error_msg():
            nonlocal error_msg
            if error_msg:
                error_msg.destroy()
                error_msg = None

        def set_error_msg(message):
            nonlocal error_msg
            error_msg = ttk.Label(self.content, text=message, foreground='red')
            error_msg.place(relx=.5, rely=.55, anchor='center')

        def update():
            remove_error_msg()
            new_name = collection_name.get()
            if new_name:
                response = requests.patch(
                    f'{BASE_URL}/collection/',
                    json={"name": new_name, "id": collection_id},
                    headers={"Authorization": self.token}
                )
                print("Status Code:", response.status_code)
                print("Response:", response.text)

                if response.status_code in [200, 201, 204]:
                    self.collectionsScreen()
                elif response.status_code < 500:
                    set_error_msg("Invalid Name")
                else:
                    set_error_msg("Server Error, Please try again")
            else:set_error_msg("Collection has to have a name")

        ttk.Label(self.content, text="Modify Collection", font=("Helvetica", 22, "bold")).place(relx=.5, rely=.25,
                                                                                                anchor='center')
        ttk.Label(self.content, text="New Name", font=("Helvetica", 14)).place(relx=.5, rely=.41, anchor='center')

        #collection_name = tk.StringVar()
        original_name = self.get_collection_name_by_id(collection_id)
        collection_name = tk.StringVar(value=original_name)

        name_entry = ttk.Entry(self.content, textvariable=collection_name)
        name_entry.place(relx=.5, rely=.47, relheight=.07, anchor='center')
        name_entry.bind('<Key>', lambda x: remove_error_msg())

        # Correctly spaced buttons
        #ttk.Button(self.content, text="Cancel", width=15, command=self.collectionsScreen).place(relx=.3, rely=.65,anchor='center')
        ttk.Button(self.content, text="Cancel", width=15, command=lambda: [remove_error_msg(), collection_name.set(original_name)]
        ).place(relx=.3, rely=.65, anchor='center')

        ttk.Button(self.content, text="Update", width=15, command=update).place(relx=.7, rely=.65, anchor='center')
        ttk.Button(self.content, text="Back", width=15, command=self.collectionsScreen).place(relx=.5, rely=.75, anchor='center')

    def get_collection_name_by_id(self, collection_id):
        response = requests.get(f'{BASE_URL}/collection/get', headers={"Authorization": self.token})
        collections = response.json()
        for col in collections:
            if col['id'] == collection_id:
                return col['name']
        return ""


    def updateTaskScreen(self, task, task_screen_parameters):
        for i in self.content.winfo_children():
            i.destroy()

        error_msg = None
        def navigate_to_task_screen():
            self.taskScreen(task_screen_parameters[0], task_screen_parameters[1])
        def remove_error():
            nonlocal error_msg
            if error_msg:
                error_msg.destroy()
                error_msg = None
        def set_error_msg_name(message):
            nonlocal error_msg
            error_msg = ttk.Label(self.content, foreground='red', text=message)
            error_msg.place(relx=.5, rely=.62, anchor='center')
        

        def updateTask():
            new_name = collection_name.get()
            new_priority = combobox.get()
            if not new_name or not new_priority:
                set_error_msg_name("Missing name")
                return
            
            updated_task = task
            updated_task['name'] = new_name
            updated_task['priority'] = get_priority_val(new_priority)
            response = requests.patch(f'{BASE_URL}/task/',
                                      headers={"Authorization":self.token},
                                      json=updated_task)
            
            if response.status_code == 204:
                navigate_to_task_screen()
            elif response.status_code >=400 and response.status_code < 500:
                set_error_msg_name("Invalid name or priority")
            else:
                set_error_msg_name("Server error, please try again")
        
        ttk.Label(self.content, text="Edit Task", font=("Helvetica", 22, "bold")).place(relx=.5, rely=.25, anchor='center')
        ttk.Label(self.content, text="Task Name", font=("Helvetica", 14)).place(relx=.5, rely=.34, anchor='center')
        collection_name = tk.StringVar(master=self.content, value=task['name'])
        original_name = task['name']
        original_priority = get_priority_str(task['priority']).upper()

        name_entry = tk.Entry(self.content, textvariable=collection_name, width=25)
        name_entry.place(relx=.5, rely=.4, relheight=.07, anchor='center')
        name_entry.update() # this is needed so that the name will load instantly
        name_entry.bind('<Key>', lambda x: remove_error())

        ttk.Label(self.content, text='Priority').place(relx=0.5, rely=0.48, anchor='center')

        combobox = ttk.Combobox(self.content, state='readonly', values=list(str_to_val.keys()), width=20, validate='focus', validatecommand=remove_error)
        combobox.set(get_priority_str(task['priority']).upper())
        combobox.place(relx=0.5, rely=0.54, anchor='center')
        # combobox.bind('<<ComboboxSelected>>', func=lambda x: remove_error())
        
        #ttk.Button(self.content, text="Cancel", width=15, command=navigate_to_task_screen).place(relx=.5, rely=.7, anchor='center')
        ttk.Button(self.content, text="Cancel", width=15, command=lambda: [remove_error(), collection_name.set(original_name), combobox.set(original_priority)]
        ).place(relx=.5, rely=.7, anchor='center')

        ttk.Button(self.content, text="Update", width=15, command=updateTask).place(relx=.5, rely=.75, anchor='center')
        ttk.Button(self.content, text="Back", width=15, command=navigate_to_task_screen).place(relx=.5, rely=.8, anchor='center')

    def viewByPriorityScreen(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        selected_priority = tk.StringVar()

        # Top control panel
        control_frame = ttk.Frame(self.content)
        control_frame.pack(pady=20)

        ttk.Label(control_frame, text="Choose Priority", font=("Helvetica", 16)).grid(row=0, column=0, padx=10)
        priorities = list(str_to_val.keys())
        ttk.Combobox(control_frame, textvariable=selected_priority, values=priorities, state='readonly').grid(row=0,
                                                                                                              column=1,
                                                                                                              padx=10)
        ttk.Button(control_frame, text="Show Tasks", command=lambda: fetch_all_tasks_by_priority()).grid(row=0,
                                                                                                         column=2,
                                                                                                         padx=10)

        task_view_frame = ttk.Frame(self.content)
        task_view_frame.pack(fill='both', expand=True, pady=(10, 30))

        def fetch_all_tasks_by_priority():
            for widget in task_view_frame.winfo_children():
                widget.destroy()

            priority_val = get_priority_val(selected_priority.get())
            response = requests.get(f"{BASE_URL}/collection/get", headers={"Authorization": self.token})
            if response.status_code != 200:
                print("Failed to fetch collections")
                return

            all_tasks = []
            collections = response.json()

            for col in collections:
                cid = col['id']
                cname = col['name']
                res = requests.get(f"{BASE_URL}/task/{cid}", headers={"Authorization": self.token})
                if res.status_code == 200:
                    tasks = res.json()
                    matching = [t for t in tasks if t['priority'] == priority_val]
                    for t in matching:
                        t['collection_name'] = cname
                    all_tasks.extend(matching)

            show_filtered_tasks(all_tasks)

        def show_filtered_tasks(task_list):
            # Headers
            headers = ["Task", "Priority", "Creation Date", "Status"]
            for col, header in enumerate(headers):
                ttk.Label(task_view_frame, text=header, font=("Arial", 12, "bold")).grid(row=0, column=col, padx=10,
                                                                                         pady=5)

            # Rows
            for i, task in enumerate(task_list):
                ttk.Label(task_view_frame, text=task['name']).grid(row=i + 1, column=0, padx=10, pady=3)
                ttk.Label(task_view_frame, text=get_priority_str(task['priority'])).grid(row=i + 1, column=1, padx=10)
                creation_date = task.get('creation_date')
                date_str = datetime_to_mdy(creation_date) if creation_date else "N/A"
                ttk.Label(task_view_frame, text=date_str).grid(row=i + 1, column=2, padx=10)
                ttk.Label(task_view_frame, text="Completed" if task.get('completed') else "Pending").grid(row=i + 1,
                                                                                                          column=3,
                                                                                                          padx=10)

        ttk.Button(self.content, text="Back", command=self.collectionsScreen).place(relx=0.5, rely=0.95,
                                                                                    anchor='center')

    def sortByPriorityScreen(self):
        from datetime import datetime

        for widget in self.content.winfo_children():
            widget.destroy()

        ttk.Label(self.content, text="All Tasks Sorted By Priority", font=("Helvetica", 18, "bold")).pack(pady=10)

        # Scrollable frame setup
        canvas = tk.Canvas(self.content)
        scrollbar = ttk.Scrollbar(self.content, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Table headers
        headers = ["Task", "Priority", "Creation Date", "Status"]
        for col, h in enumerate(headers):
            ttk.Label(scroll_frame, text=h, font=("Helvetica", 12, "bold")).grid(row=0, column=col, padx=10, pady=5)

        all_tasks = []
        collections = []

        res = requests.get(f"{BASE_URL}/collection/get", headers={"Authorization": self.token})
        if res.status_code == 200:
            collections = res.json()

        for collection in collections:
            cid = collection['id']
            cname = collection['name']
            task_res = requests.get(f"{BASE_URL}/task/{cid}", headers={"Authorization": self.token})
            if task_res.status_code == 200:
                tasks = task_res.json()
                for task_obj in tasks:
                    task_obj['collection_id'] = cid
                    task_obj['collection_name'] = cname
                    all_tasks.append(task_obj)

        # Safer datetime parser (avoid .timestamp() on bad dates)
        def safe_date(task_obj):
            dt_str = task_obj.get('creation_date')
            formats = ['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ']
            for fmt in formats:
                try:
                    return datetime.strptime(dt_str, fmt)
                except Exception:
                    continue
            return datetime.min  # Fallback

        # Sort by priority (lower = higher) and date (newest first)
        all_tasks.sort(key=lambda task_obj: (task_obj['priority'], safe_date(task_obj)), reverse=True)

        for i, task_obj in enumerate(all_tasks):
            ttk.Label(scroll_frame, text=task_obj['name']).grid(row=i + 1, column=0, padx=10, pady=3)
            ttk.Label(scroll_frame, text=get_priority_str(task_obj['priority'])).grid(row=i + 1, column=1, padx=10)
            ttk.Label(
                scroll_frame,
                #text=task_obj.get('created_at', 'N/A').split("T")[0] if 'created_at' in task_obj else "N/A"
                text = datetime_to_mdy(task_obj.get('creation_date')) if task_obj.get('creation_date') else 'N/A'

            ).grid(row=i + 1, column=2, padx=10)
            ttk.Label(scroll_frame, text="Completed" if task_obj.get('completed') else "Pending").grid(row=i + 1,
                                                                                                       column=3,
                                                                                                       padx=10)

            # Actions (optional – currently no buttons provided)
            action_frame = ttk.Frame(scroll_frame)
            action_frame.grid(row=i + 1, column=4)

        # Back button
        ttk.Button(self.content, text="Back", command=self.collectionsScreen).pack(pady=15)


app(root)
sv_ttk.use_light_theme()

root.mainloop()