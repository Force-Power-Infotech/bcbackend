-- Migration: Add meta_drill_group_id column to drill_groups
ALTER TABLE drill_groups ADD COLUMN meta_drill_group_id INTEGER;
-- You may want to add a foreign key constraint if meta_drill_group_id references another table, e.g.:
-- ALTER TABLE drill_groups ADD CONSTRAINT fk_meta_drill_group FOREIGN KEY (meta_drill_group_id) REFERENCES meta_drill_groups(id);
