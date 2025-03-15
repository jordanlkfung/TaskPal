from fastapi import FastAPI
from app.users.routes import user_router
from contextlib import asynccontextmanager
from .db_init import create_tables
from .task.routes import task_router
from .collection.routes import collection_router

# create_tables()
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
app.include_router(task_router, prefix=f'/api/{version}/task', tags=['task'])
app.include_router(collection_router, prefix=f'/api/{version}/collection', tags=['collection'])

@app.get("/")
async def root():
    return {"message":"hello"}
