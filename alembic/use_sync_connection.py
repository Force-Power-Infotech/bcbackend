import os
import sys
from pathlib import Path

# Add the parent directory to sys.path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

# Force a synchronous database URL for the migration
os.environ["DATABASE_URL"] = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@db:5432/bowlsacedb").replace("+asyncpg", "")
