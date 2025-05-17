import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev")
    ALLOWED_EXTENSIONS = {"pdf"}
    DB_FILE_PATH = os.environ.get("DB_FILE_PATH", "mydb.db")
