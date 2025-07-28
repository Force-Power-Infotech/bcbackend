"""
Script to run the FastAPI application locally with a sync database URL
"""
import uvicorn
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path so we can import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# Override DATABASE_URL to use psycopg2 (sync driver) and connect to the Docker container
# Docker exposes port 5432 so we can connect to it from the host
os.environ["DATABASE_URL"] = "postgresql+psycopg2://postgres:postgres@localhost:5432/bowlsacedb"
os.environ["USE_SYNC_DB"] = "true"

if __name__ == "__main__":
    # Using port 8000
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
