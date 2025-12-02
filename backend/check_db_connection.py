"""
Small utility to test TCP connectivity and PyMySQL authentication to the DB configured
via environment variables. Useful to run inside the Render service shell to diagnose
network/credential issues.

Usage:
  python backend/check_db_connection.py

It prints diagnostic lines and exits with code 0 on success, 1 on failure.
"""
from dotenv import load_dotenv
import os
import pathlib
import socket
import sys
import traceback

try:
    import pymysql
except Exception:
    print("PyMySQL not installed in this environment. Install via requirements.txt.")
    sys.exit(1)

root = pathlib.Path(__file__).parent
env_path = root / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=str(env_path))

DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = int(os.getenv('DB_PORT', '3306'))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'todo_db')
DB_CONNECT_TIMEOUT = int(os.getenv('DB_CONNECT_TIMEOUT', '5'))


def test_tcp_connect(host, port, timeout):
    print(f"Testing TCP to {host}:{port} with timeout={timeout}s...")
    try:
        with socket.create_connection((host, port), timeout):
            print("TCP connection: SUCCESS")
            return True
    except Exception as e:
        print("TCP connection: FAILED")
        traceback.print_exc()
        return False


def test_pymysql_connect(host, port, user, password, db, timeout):
    print(f"Testing PyMySQL connect to {host}:{port} database='{db}' user='{user}' timeout={timeout}s...")
    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db,
            connect_timeout=timeout,
            cursorclass=pymysql.cursors.DictCursor,
            charset='utf8mb4'
        )
        conn.close()
        print("PyMySQL connect: SUCCESS")
        return True
    except Exception as e:
        print("PyMySQL connect: FAILED")
        traceback.print_exc()
        return False


def main():
    tcp_ok = test_tcp_connect(DB_HOST, DB_PORT, DB_CONNECT_TIMEOUT)
    if not tcp_ok:
        print("TCP check failed — likely a network/DNS/firewall issue. Stop here.")
        sys.exit(1)

    sql_ok = test_pymysql_connect(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, DB_CONNECT_TIMEOUT)
    if not sql_ok:
        print("Authentication or database issue — credentials or DB name may be wrong.")
        sys.exit(1)

    print("All checks passed — service should be able to reach the DB.")
    sys.exit(0)


if __name__ == '__main__':
    main()
