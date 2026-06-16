import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:secretpassword@localhost:5432/sentrynode")

def run_migrations():
    print(f"Connecting to database at: {DATABASE_URL.split('@')[-1]}...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Read schema file
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        with open(schema_path, "r") as f:
            schema_sql = f.read()
            
        print("Executing schema migrations...")
        cur.execute(schema_sql)
        conn.commit()
        
        print("Database migrations applied successfully.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Migration error: {e}")

if __name__ == "__main__":
    run_migrations()
