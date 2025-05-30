"""
Script to test database connectivity using both psycopg2 and asyncpg
"""
import asyncio
import os
import sys
import asyncpg
import psycopg2

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.core.config import settings

async def test_asyncpg():
    """Test connection with asyncpg (async driver)"""
    print("\nTesting connection to PostgreSQL using asyncpg...")
    try:
        # Parse connection info from DATABASE_URL
        connection_string = settings.DATABASE_URL
        if 'postgresql+psycopg2://' in connection_string:
            connection_string = connection_string.replace('postgresql+psycopg2://', 'postgresql://')
        
        # Try to connect
        conn = await asyncpg.connect(connection_string)
        print("Connection successful!")
        
        # Test a query
        version = await conn.fetchval('SELECT version()')
        print(f"PostgreSQL version: {version}")
        
        # Check if users table exists
        exists = await conn.fetchval("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')")
        if exists:
            print("Users table exists")
            
            # Check if any users exist
            count = await conn.fetchval("SELECT COUNT(*) FROM users")
            print(f"Number of users: {count}")
            
            # Check table structure
            columns = await conn.fetch(
                "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users'"
            )
            print("\nUsers table structure:")
            for col in columns:
                print(f"- {col['column_name']}: {col['data_type']}")
        else:
            print("Users table does not exist")
        
        # Close the connection
        await conn.close()
        print("Connection closed")
        
    except Exception as e:
        print(f"Connection failed: {e}")

def test_psycopg2():
    """Test connection with psycopg2 (sync driver)"""
    print("\nTesting connection to PostgreSQL using psycopg2...")
    try:
        # Parse connection info from DATABASE_URL
        connection_string = settings.DATABASE_URL
        if 'postgresql+psycopg2://' in connection_string:
            # Extract parts from connection string
            parts = connection_string.replace('postgresql+psycopg2://', '').split('/')
            credentials = parts[0].split('@')
            user_pass = credentials[0].split(':')
            host_port = credentials[1].split(':')
            
            user = user_pass[0]
            password = user_pass[1]
            host = host_port[0]
            port = int(host_port[1]) if len(host_port) > 1 else 5432
            database = parts[1]
        else:
            # Default values
            user = 'postgres'
            password = 'postgres'
            host = 'db'
            port = 5432
            database = 'bowlsacedb'
        
        # Try to connect
        conn = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )
        print("Connection successful!")
        
        # Test a query
        cur = conn.cursor()
        cur.execute('SELECT version()')
        version = cur.fetchone()
        print(f"PostgreSQL version: {version[0]}")
        
        # Check if users table exists
        cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')")
        exists = cur.fetchone()[0]
        if exists:
            print("Users table exists")
            
            # Check if any users exist
            cur.execute("SELECT COUNT(*) FROM users")
            count = cur.fetchone()[0]
            print(f"Number of users: {count}")
            
            # Check table structure
            cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users'")
            print("\nUsers table structure:")
            for col in cur.fetchall():
                print(f"- {col[0]}: {col[1]}")
        else:
            print("Users table does not exist")
        
        # Close the connection
        cur.close()
        conn.close()
        print("Connection closed")
        
    except Exception as e:
        print(f"Connection failed: {e}")

async def main():
    """Run both connection tests"""
    print(f"Testing database connection with URL: {settings.DATABASE_URL}")
    
    # Test with psycopg2
    test_psycopg2()
    
    # Test with asyncpg
    await test_asyncpg()

def test_local_connection():
    """Test local connection with localhost instead of db container name"""
    print("\nTesting direct connection to localhost...")
    try:
        # Try to connect
        conn = psycopg2.connect(
            user="postgres",
            password="postgres",
            host="localhost",
            port=5432,
            database="bowlsacedb"
        )
        print("Local connection successful!")
        
        # Test a query
        cur = conn.cursor()
        cur.execute('SELECT version()')
        version = cur.fetchone()
        print(f"PostgreSQL version: {version[0]}")
        
        # Close the connection
        cur.close()
        conn.close()
        print("Connection closed")
        
    except Exception as e:
        print(f"Local connection failed: {e}")

if __name__ == "__main__":
    # Test local connection directly
    test_local_connection()
    
    # Test with config settings
    asyncio.run(main())
