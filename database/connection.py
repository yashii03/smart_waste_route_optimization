import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load variables from .env
load_dotenv()

# Read database settings
DB_HOST = os.getenv("localhost")
DB_PORT = os.getenv("3360")
DB_NAME = os.getenv("smart_waste_db")
DB_USER = os.getenv("root")
DB_PASSWORD = os.getenv("123456")

# Create MySQL connection URL
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

print("Database engine created successfully!")