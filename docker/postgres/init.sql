-- Connect to the default postgres database
\c postgres;

-- Create the application database if it doesn't exist
CREATE DATABASE bowlsacedb;

-- Connect to the application database
\c bowlsacedb;

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant privileges to the postgres user
GRANT ALL PRIVILEGES ON DATABASE bowlsacedb TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;
