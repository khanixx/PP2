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

def search_pattern(pattern):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM phonebook
                WHERE first_name ILIKE %s OR last_name ILIKE %s OR phone ILIKE %s
            """, (f'%{pattern}%', f'%{pattern}%', f'%{pattern}%'))
            return cur.fetchall()



def insert_or_update_user(first_name, last_name, phone):
    with connect() as conn:
        with conn.cursor() as cur:
            if phone.isdigit() and 10 <= len(phone) <= 15:
                cur.execute("""
                    SELECT * FROM phonebook 
                    WHERE first_name ILIKE %s AND last_name ILIKE %s
                """, (first_name, last_name))
                if cur.fetchone():
                    cur.execute("""
                        UPDATE phonebook 
                        SET phone = %s 
                        WHERE first_name ILIKE %s AND last_name ILIKE %s
                    """, (phone, first_name, last_name))
                else:
                    cur.execute("""
                        INSERT INTO phonebook (first_name, last_name, phone)
                        VALUES (%s, %s, %s)
                    """, (first_name, last_name, phone))
                conn.commit()
            else:
                print(f"Invalid phone: {phone}")


def insert_many_users(data):
    invalid_data = []
    with connect() as conn:
        with conn.cursor() as cur:
            for first_name, last_name, phone in data:
                if phone.isdigit() and 10 <= len(phone) <= 15:
                    cur.execute("""
                        SELECT * FROM phonebook 
                        WHERE first_name ILIKE %s AND last_name ILIKE %s
                    """, (first_name, last_name))
                    if cur.fetchone():
                        cur.execute("""
                            UPDATE phonebook 
                            SET phone = %s 
                            WHERE first_name ILIKE %s AND last_name ILIKE %s
                        """, (phone, first_name, last_name))
                    else:
                        cur.execute("""
                            INSERT INTO phonebook (first_name, last_name, phone)
                            VALUES (%s, %s, %s)
                        """, (first_name, last_name, phone))
                else:
                    invalid_data.append(f"{first_name} {last_name} - {phone}")
        conn.commit()
    return invalid_data




def get_paginated_data(limit, offset):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook ORDER BY id LIMIT %s OFFSET %s", (limit, offset))
            return cur.fetchall()

def delete_by_name_or_phone(value):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM phonebook WHERE first_name = %s OR phone = %s", (value, value))
        conn.commit()

