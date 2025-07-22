import subprocess
import sys
import time
import psycopg2
from psycopg2 import Error

def check_postgres():
    """Check if PostgreSQL is accessible"""
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="bowlsace",
            password="supersecret",
            host="localhost",
            port="5432"
        )
        conn.close()
        return True
    except Error:
        return False

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to default postgres database
        conn = psycopg2.connect(
            dbname="postgres",
            user="bowlsace",
            password="supersecret",
            host="localhost",
            port="5432"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='bowlsacedb'")
        if not cursor.fetchone():
            cursor.execute("CREATE DATABASE bowlsacedb")
            print("Database created successfully!")
        else:
            print("Database already exists!")
            
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Error: {e}")
        sys.exit(1)

def run_migrations():
    """Run alembic migrations"""
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("Migrations completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error running migrations: {e}")
        sys.exit(1)

def main():
    print("Checking PostgreSQL connection...")
    retries = 5
    while retries > 0:
        if check_postgres():
            break
        print(f"Cannot connect to PostgreSQL. Retrying... ({retries} attempts left)")
        retries -= 1
        time.sleep(2)
    
    if retries == 0:
        print("Error: Could not connect to PostgreSQL. Please make sure PostgreSQL is running on localhost:5432")
        sys.exit(1)
    
    print("Creating database if it doesn't exist...")
    create_database()
    
    print("Running database migrations...")
    run_migrations()
    
    print("\nSetup completed successfully!")
    print("\nTo run the backend server, use:")
    print("uvicorn app.main:app --reload")

if __name__ == "__main__":
    main()
