import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

db = pymysql.connect(host = os.getenv("DB_host"), user = os.getenv("DB_user"), password = os.getenv("DB_password"), database = os.getenv("DB_database"), port = int(os.getenv("DB_port")))
cursor = db.cursor()
