import glob
import os
import sqlite3

from config import Config

SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "../schemas/")


def get_db_connection():
    conn = sqlite3.connect(Config.DB_FILE_PATH)
    conn.row_factory = sqlite3.Row
    # Initialize all schemas in the schemas directory
    schema_files = sorted(glob.glob(os.path.join(SCHEMA_DIR, "*.sql")))
    for schema_file in schema_files:
        with open(schema_file) as f:
            conn.executescript(f.read())
    return conn
