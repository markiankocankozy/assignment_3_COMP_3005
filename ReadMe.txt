Install instructions:
pip3 install -r requirements.txt

Database Setup:
#open psql 
psql -d postgres
#Create school_db
CREATE DATABASE school_db;
#quit psql for now
\q
#populate database
psql -d school_db -f db/database.sql;
#make sure the database was populated successfully
psql -d postgres
\c school_db
SELECT * FROM students;

Examples of how to use functions:
#make sure your not in PostgreSQL
\q
# List students
python3 app/main.py list

# Add a student
python3 app/main.py add "Alice" "Wonder" "alice@example.com" 2023-09-03

# Update a student's email
python3 app/main.py update-email 1 "john.new@example.com"

# Delete a student
python3 app/main.py delete 3