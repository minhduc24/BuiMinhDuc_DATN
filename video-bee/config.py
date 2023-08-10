import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

"""
Database config
"""
DB_DEFAULT_HOST = os.getenv("DB_DEFAULT_HOST")
DB_DEFAULT_PORT = os.getenv("DB_DEFAULT_PORT")
DB_DEFAULT_DBNAME = os.getenv("DB_DEFAULT_DBNAME")
DB_DEFAULT_USERNAME = os.getenv("DB_DEFAULT_USERNAME")
DB_DEFAULT_PASSWORD = os.getenv("DB_DEFAULT_PASSWORD")

"""
S3 Credential
"""
S3_ACCESS_KEY_ID = os.getenv("S3_ACCESS_KEY_ID")
S3_SECRET_ACCESS_KEY = os.getenv("S3_SECRET_ACCESS_KEY")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_RESULT_BUCKET = os.getenv("S3_RESULT_BUCKET")

"""
Shotstack config
"""
SHOTSTACK_API_KEY= os.getenv("SHOTSTACK_API_KEY")
SHOTSTACK_ASSETS_URL=os.getenv("SHOTSTACK_ASSETS_URL")
SHOTSTACK_HOST=os.getenv("SHOTSTACK_HOST")
PEXELS_API_KEY=os.getenv("PEXELS_API_KEY")