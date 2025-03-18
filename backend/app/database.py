from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import os
from dotenv import load_dotenv

load_dotenv(override=True)
url = os.getenv("DB_URL")
print(url)

engine = create_async_engine(url)
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def get_db():
    async with Session() as db: 
        try:
            yield db
        finally:
            await db.close()

