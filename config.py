import os

from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')  # позволяет забрать из файлика .env данные

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')

settings = [DB_HOST, DB_USER, DB_PASS, DB_PORT, DB_NAME]

if not all([settings]):
    raise ValueError("One or more environment variables are not set")

SECRET = os.environ.get('SECRET')

api_id = os.environ.get('api_id')
api_hash = os.environ.get('api_hash')
phone = os.environ.get('phone')
