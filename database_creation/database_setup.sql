-- Remove existing user and database
DROP DATABASE IF EXISTS antisocialnetwork;
DROP USER IF EXISTS antisocial_admin;

-- Create user responsible for the database
CREATE USER antisocial_admin WITH PASSWORD NULL;
CREATE DATABASE antisocialnetwork;
ALTER DATABASE antisocialnetwork OWNER TO antisocial_admin;

-- Connect to database to finish setup
\c antisocialnetwork

-- Load python language and allow it to be executed (Warning: Potentially dangerous!)
CREATE EXTENSION IF NOT EXISTS plpython3u;
UPDATE pg_language SET lanpltrusted = TRUE WHERE lanname = 'plpython3u';
