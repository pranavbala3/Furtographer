import psycopg2

hostname = 'localhost'
database = 'furtographer'
username = 'admin'
pwd = 'password'
port_id = 5431
conn = None
curr = None
try:
    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id)

    # Note: when creating a cursor, make sure to close cursor when closing the connection
    curr = conn.cursor()

    # read from SQL script for Users table creation
    with open('V20231025_0823_create_table_users.sql', 'r') as file:
        user_tables_script = file.read()

    # execute the Users table creation script
    curr.execute(user_tables_script)

    # read the data SQL file for Users
    # execute the Users data SQL


except Exception as error:
    print(error)
finally:
    if curr is not None:
        cur.close()
    if conn is not None:
        conn.close()
