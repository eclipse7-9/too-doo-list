from dotenv import load_dotenv
import os
import pathlib
import pymysql

root = pathlib.Path(__file__).parent
env_path = root / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=str(env_path))

DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = int(os.getenv('DB_PORT', '3306'))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'todo_db')
DB_CONNECT_TIMEOUT = int(os.getenv('DB_CONNECT_TIMEOUT', '10'))
DB_SSL = os.getenv('DB_SSL', 'false').lower() in ('1', 'true', 'yes')

# Quick validation to catch a common misconfiguration: pasting the port into DB_NAME.
# If DB_NAME is numeric or exactly equals the DB_PORT, raise a clear error so the
# deployment logs show a helpful message instead of a vague authentication error.
if isinstance(DB_NAME, str) and (DB_NAME.isdigit() or DB_NAME == str(DB_PORT)):
    raise RuntimeError(
        f"Invalid DB_NAME environment variable: '{DB_NAME}'.\n"
        "It looks like you pasted the database port into DB_NAME.\n"
        "Please set `DB_PORT` to the numeric port (e.g. 29949) and `DB_NAME` to the actual database name\n"
        "(for Railway the DB name is usually 'railway' or the name shown in the connection details)."
    )

def get_conn():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        connect_timeout=DB_CONNECT_TIMEOUT,
        ssl={'ssl': {}} if DB_SSL else None,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
        charset='utf8mb4'
    )
