import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "job_tracker.db")
SECRET_KEY = "814k0a2b8c4h6a0q3ji910o20f6k1la7"
ACCESS_TOKEN_EXPIRE_MINUTES = 15