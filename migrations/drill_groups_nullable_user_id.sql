-- Make drill_groups.user_id nullable
ALTER TABLE drill_groups ALTER COLUMN user_id DROP NOT NULL;
