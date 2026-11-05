CREATE TABLE IF NOT EXISTS sessions (id bigint PRIMARY KEY, token text, file_name text);
CREATE TABLE players (id bigint, display_name text, PRIMARY KEY (id));
ALTER TABLE sessions ADD COLUMN email text, ADD COLUMN created_at timestamptz;
