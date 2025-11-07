# app/main.py
#Simple CLI to demonstrate CRUD functions required by the assignment
#
#Usage examples:
#   python3 app/main.py list
#   python3 app/main.py add "Alice" "Wonder" "alice@example.com" 2023-09-03
#   python3 app/main.py update-email 1 "john.new@example.com"
#   python3 app/main.py delete 3
#
# (First create the DB + table and load schema.sql; see README.)

import sys
from tabulate import tabulate
from db import get_all_students, add_student, update_student_email, delete_student

def print_students():
    rows = get_all_students()
    if rows:
        print(tabulate(rows, headers="keys", tablefmt="github"))
    else:
        print("No students found.")

def usage():
    print(
        "Usage:\n"
        "   python3 app/main.py list\n"
        "   python3 app/main.py add <first_name> <last_name> <email> <enrollment_date|None>\n"
        "   python3 app/main.py update-email <student_id> <new_email>\n"
        "   python3 app/main.py delete <student_id>\n"
    )
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    cmd = sys.argv[1]
    try:
        if cmd == "list":
            print_students()
        elif cmd == "add":
            if len(sys.argv) != 6:
                usage()
                sys.exit(1)
            first_name, last_name, email, date_str = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
            enrollment_date = None if date_str.lower() == "none" else date_str
            new_id = add_student(first_name, last_name, email, enrollment_date)
            print(f"Inserted student_id={new_id}")
            print_students()
        elif cmd == "update-email":
            if len(sys.argv) != 4:
                usage()
                sys.exit(1)
            student_id = int(sys.argv[2])
            new_email = sys.argv[3]
            updated = update_student_email(student_id, new_email)
            print(f"Rows updated: {updated}")
            print_students()
        elif cmd == "delete":
            if len(sys.argv) != 3:
                usage()
                sys.exit(1)
            student_id = int(sys.argv[2])
            deleted = delete_student(student_id)
            print(f"Rows deleted: {deleted}")
            print_students()
        else:
            usage()
            sys.exit(1)
    except Exception as e:
        # Basic error display for demo
        print(f"Error: {e}")
        sys.exit(2)
