import sqlite3
from config import DB_PATH


def get_db():
    return sqlite3.connect(DB_PATH)