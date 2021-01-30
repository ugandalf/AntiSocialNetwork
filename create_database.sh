#!/usr/bin/env zsh

# make sure to run "sudo pip3 install -r requirements.txt" before!!!

# Creates:
# - database "antisocialnetwork"
# - user "antisocial_admin"
# - extension "plpython3u" and makes it trusted for the sake of letting "antisocial_admin" add functions
psql -f ./database_creation/database_setup.sql
# Connects to database as antisocial_admin and creates all the tables and views
psql -f ./database_creation/table_creation.sql
psql -f ./database_creation/table_views.sql
# Creates functions that populate the database with sample data
psql -f ./database_creation/table_population.sql
# Handles all kinds of triggers: email, password, chronology, friend_request => friends transition
psql -f ./database_creation/table_triggers.sql
# Fill the database with sample data - it takes some time, mainly due to password security
psql -f ./database_creation/table_checks.sql
psql -f ./database_creation/table_fill.sql
# Adds primary and foreign keys
psql -f ./database_creation/table_pkeys.sql
psql -f ./database_creation/table_fkeys.sql
# Makes "plpython3u" untrusted again for added security
psql -f ./database_creation/database_cleanup.sql
