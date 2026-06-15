import pymysql
from dotenv import load_dotenv
import os

env_path='./.env'
load_dotenv(dotenv_path=env_path)

HOST=os.getenv('DB_HOST')
PORT=os.getenv('DB_PORT')
USER=os.getenv('DB_USER')
PASS=os.getenv('DB_PASS')
NAME=os.getenv('DB_NAME')

def get_connection():
    conn = pymysql.connect(
        host=HOST,
        user=USER,
        password=PASS,
        database=NAME,
        charset="utf8"
    )

    cursor = conn.cursor()    
    return cursor