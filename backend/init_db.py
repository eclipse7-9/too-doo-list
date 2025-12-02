import pathlib
import sys
from backend.database import get_conn


def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    schema_file = root / 'server' / 'schema.sql'
    if not schema_file.exists():
        print(f"schema file not found: {schema_file}")
        sys.exit(1)

    sql = schema_file.read_text(encoding='utf-8')

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # naive split by ';' to run each statement
            parts = [p.strip() for p in sql.split(';') if p.strip()]
            for p in parts:
                cur.execute(p)
        conn.commit()
        print('Schema executed successfully')
    finally:
        conn.close()


if __name__ == '__main__':
    main()
