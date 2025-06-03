-- Add new columns to drill_groups table
ALTER TABLE drill_groups ADD COLUMN IF NOT EXISTS is_public BOOLEAN DEFAULT true;
ALTER TABLE drill_groups ADD COLUMN IF NOT EXISTS difficulty INTEGER DEFAULT 1;
ALTER TABLE drill_groups ADD COLUMN IF NOT EXISTS tags JSONB DEFAULT '[]'::jsonb;
