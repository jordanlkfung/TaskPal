from fastapi import FastAPI
from app.users.routes import user_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Server is starting")
    yield
    print("Server is shutting down")

version = 'v1'

app = FastAPI(
    title="TaskPal",
    version=version,
    lifespan=lifespan
)

app.include_router(user_router, prefix=f'/api/{version}/user', tags=['user'])

@app.get("/")
async def root():
    return {"message":"hello"}


@app.post("/login")
async def login():
    pass

@app.post("/signup")
async def signUp():
    pass

@app.get("/tasks")
async def getTasks():
    pass

@app.post("/tasks/add")
async def addTask():
    pass

@app.patch("/tasks/update/{_id}")
async def updateTask(_id:str):
    pass

@app.delete("/tasks/{_id}")
async def deleteTask(_id:str):
    pass

@app.get("/collections/{collectionId}")
async def getColllection(collectionId: str):
    pass