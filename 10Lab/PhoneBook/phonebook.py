import csv
from connect import connect

def create_table():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phonebook (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50),
                    phone VARCHAR(15)
                );
            """)
            conn.commit()

def insert_from_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        with connect() as conn:
            with conn.cursor() as cur:
                for row in reader:
                    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (row[0], row[1]))
            conn.commit()

def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
        conn.commit()

def update_phone(name, new_phone):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE phonebook SET phone = %s WHERE name = %s", (new_phone, name))
        conn.commit()

def update_name(phone, new_name):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE phonebook SET name = %s WHERE phone = %s", (new_name, phone))
        conn.commit()

def query_by_name(name):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook WHERE name ILIKE %s", (f'%{name}%',))
            return cur.fetchall()

def query_by_phone(phone):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (f'%{phone}%',))
            return cur.fetchall()

def delete_by_name(name):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
        conn.commit()

def delete_by_phone(phone):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
        conn.commit()
