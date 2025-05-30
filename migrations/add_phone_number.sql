-- Migration SQL script to add phone number and verification columns
-- This is a direct SQL version of our Alembic migration

-- Add phone_number column
ALTER TABLE users ADD COLUMN IF NOT EXISTS phone_number VARCHAR(20);

-- Create index on phone_number
CREATE UNIQUE INDEX IF NOT EXISTS ix_users_phone_number ON users(phone_number);

-- Update existing users with temporary phone numbers
UPDATE users 
SET phone_number = CONCAT('temp_', id, '_', FLOOR(RANDOM() * 1000000000)::TEXT)
WHERE phone_number IS NULL;

-- Make phone_number not null after populating data
ALTER TABLE users ALTER COLUMN phone_number SET NOT NULL;

-- Add verification columns
ALTER TABLE users ADD COLUMN IF NOT EXISTS phone_verified BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS email_verified BOOLEAN NOT NULL DEFAULT FALSE;
