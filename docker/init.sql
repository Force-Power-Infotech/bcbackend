-- Connect to the database (it should already exist from POSTGRES_DB env var)
\c bowlsacedb;

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE bowlsacedb TO bowlsace;
