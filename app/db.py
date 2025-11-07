#app/db.py
# Lightweight PostgreSQL helper using psycopg (v3).
# Reads connection info from environment variables or a .env file.

import os
from contextlib import contextmanager
from typing import Optional, Any, List, Dict
from dotenv import load_dotenv
import psycopg
import psycopg.rows

# Loag .env if present
load_dotenv()

def _conn_kwargs() -> dict:
    return {
        "host": os.getenv("PGHOST", "localhost"),
        "port": int(os.getenv("PGPORT", "5432")),
        "dbname": os.getenv("PGDATABASE", "school_db"),
        "user": os.getenv("PGUSER", "postgres"),
        "password": os.getenv("PGPASSWORD", ""),
    }

@contextmanager
def get_conn():
    """Context manager that yields a psycopg Connection and closes it afterwards."""
    conn = psycopg.connect(**_conn_kwargs())
    try:
        yield conn
    finally:
        conn.close()

def get_all_students() -> List[Dict[str, Any]]:
    """Return all rows from students ordered by student_id."""
    with get_conn() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute("SELECT student_id, first_name, last_name, email, enrollment_date FROM students ORDER BY student_id;")
            return cur.fetchall()

def add_student(first_name: str, last_name: str, email: str, enrollment_date: Optional[str]) -> int:
    """
    Insert a new student. Returns the new student_id.
    enrollment_date should be an ISO date string (YYYY-MM-DD) or None.
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO students (first_name, last_name, email, enrollment_date)
                VALUES (%s, %s, %s, %s)
                RETURNING student_id;
                """,
                (first_name, last_name, email, enrollment_date),
            )
            new_id = cur.fetchone()[0]
            conn.commit()
            return new_id

def update_student_email(student_id: int, new_email: str) -> int:
    """Update email for a given student_id. Returns number of rows updated (0 or 1)."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE students SET email = %s WHERE student_id = %s;",
                (new_email, student_id),
            )
            updated = cur.rowcount
            conn.commit()
            return updated

def delete_student(student_id: int) -> int:
    """Delete a student by id. Returns number of rows deleted (0 or 1)."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM students WHERE student_id = %s;", (student_id,))
            deleted = cur.rowcount
            conn.commit()
            return deleted
       
