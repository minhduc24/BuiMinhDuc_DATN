from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_DEFAULT_HOST, DB_DEFAULT_PORT, DB_DEFAULT_USERNAME,DB_DEFAULT_DBNAME,DB_DEFAULT_PASSWORD


SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_DEFAULT_USERNAME}:{DB_DEFAULT_PASSWORD}@{DB_DEFAULT_HOST}:{DB_DEFAULT_PORT}/{DB_DEFAULT_DBNAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
