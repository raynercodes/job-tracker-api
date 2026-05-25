import sqlite3
from config import Config


def get_db():
    return sqlite3.connect(Config.DB_PATH)