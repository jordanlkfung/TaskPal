from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from .database import sessionmanager
import os
load_dotenv()
version = os.getenv("API_VERSION")

def init_app(init_db=True):
    lifespan = None

    if init_db:
        sessionmanager.init(os.getenv("DB_URL"))

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            print("Server is starting")
            yield
            if sessionmanager._engine is not None:
                await sessionmanager.close()
            print("Server is shutting down")

    server = FastAPI(title="FastAPI server", lifespan=lifespan)

    from app.users.routes import user_router
    from app.task.routes import task_router
    from app.collection.routes import collection_router

    server.include_router(user_router, prefix="/api/v1/user", tags=["user"])
    server.include_router(task_router, prefix=f'/api/{version}/task', tags=['task'])
    server.include_router(collection_router, prefix=f'/api/{version}/collection', tags=['collection'])
    
    @server.get('/healthcheck')
    async def healthCheck():
        return {"Health": "Good"}

    return server
