import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from google.cloud.sql.connector import Connector, IPTypes
from dotenv import load_dotenv

load_dotenv()

# We will initialize the Cloud SQL Python Connector
def getconn():
    connector = Connector()
    conn = connector.connect(
        os.getenv("CLOUD_SQL_CONNECTION_NAME", "your-project:us-central1:your-instance"),
        "pg8000",
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASS", "password"),
        db=os.getenv("DB_NAME", "praxiom"),
        ip_type=IPTypes.PUBLIC,
    )
    return conn

# For local development without actual cloud sql credentials, we will just use SQLite to avoid crashing
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./praxiom_local.db")

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session
