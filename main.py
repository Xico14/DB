import psycopg2

def create_db(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            phones VARCHAR(100) []
        )
        """)
    conn.commit()

def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cursor:
        cursor.execute("""
        INSERT INTO clients (first_name, last_name, email, phones)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """, (first_name, last_name, email, phones))
        client_id = cursor.fetchone()[0]
    conn.commit()
    return client_id

def add_phone(conn, client_id, phone):
    with conn.cursor() as cursor:
        cursor.execute("""
        UPDATE clients
        SET phones = array_append(phones, %s)
        WHERE id = %s
        """, (phone, client_id))
    conn.commit()

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    update_fields = []
    if first_name:
        update_fields.append(f"first_name = '{first_name}'")
    if last_name:
        update_fields.append(f"last_name = '{last_name}'")
    if email:
        update_fields.append(f"email = '{email}'")
    if phones:
        update_fields.append(f"phones = '{phones}'")
    
    if update_fields:
        with conn.cursor() as cursor:
            cursor.execute("""
            UPDATE clients
            SET first_name = %s, last_name = %s, email = %s, phones = %s
            WHERE id = %s
            """, (first_name, last_name, email, phones, client_id))
        conn.commit()

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cursor:
        cursor.execute("""
        UPDATE clients
        SET phones = array_remove(phones, %s)
        WHERE id = %s
        """, (phone, client_id))
    conn.commit()

def delete_client(conn, client_id):
    with conn.cursor() as cursor:
        cursor.execute("""
        DELETE FROM clients
        WHERE id = %s
        """, (client_id,))
    conn.commit()

def find_client(conn, first_name, last_name, email, phones):
    with conn.cursor() as cursor:
        query = """
        SELECT * FROM clients
        WHERE first_name = %s AND last_name = %s AND email = %s AND %s = ANY(phones)
        """
        cursor.execute(query, (first_name, last_name, email, phones))
        clients = cursor.fetchall()
    return clients


# Example usage
with psycopg2.connect(database="client_db", user="postgres", password="1111") as conn:
    create_db(conn)

    client_id = add_client(conn, "John", "Doe", "john.doe@example.com", ["1234567890","8945123187"])
    phone = add_phone(conn, 1, "8678687896")
    update_client = change_client(conn, 1, "djiighkjfdgh", "dhfghjdgsf", "dsfsdfgsdg", ["8967769808"])
    delete_phones_cl = delete_phone(conn, 1, "8945123187")
    delete_client = delete_client(conn, 1)
    clients = find_client(conn, "John", "Doe", "john.doe@example.com", "1234567890" )


conn.close()

