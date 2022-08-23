import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread = False)
        return conn
    except Error as e:
        print(e)

    return conn
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
    except Error as e:
        print(e)
def insert_in_db(conn, name, nick, status = 0, username = None):  # добавляем username в базу
    try:
        cursor = conn.cursor()
        sql_update_query = """INSERT INTO users(name, nick, status, username) VALUES(?, ?, ?, ?)"""
        cursor.execute(sql_update_query, (name, nick, status, username))
        conn.commit()
    except Error as e:
        print(e) 
def create_data_base(database):
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id INTEGER PRIMARY KEY,
                                        name TEXT NOT NULL,
                                        nick TEXT NOT NULL,
                                        status INTEGER,
                                        username TEXT
                                    ); """

    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS orders (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    visitant TEXT NOT NULL,
                                    status TEXT NOT NULL,
                                    data_visit DATA,
                                    time_visit TIME
                                    );"""

    # create a database connection
    conn = create_connection(database)
    # create tables
    if conn is not None:
        # create user table
        create_table(conn, sql_create_projects_table)
        # create orders table
        create_table(conn, sql_create_tasks_table)
        # add first admin
        insert_in_db(conn, "Daniil Suvorov", "reynardk", 1)
    else:
        print("Error! cannot create the database connection.")
    return conn
def search_nick_in_db(conn, nick):
    result = 0
    try:
        cursor = conn.cursor()
        sqlite_select_query = "SELECT * from users WHERE nick = ?"
        cursor.execute(sqlite_select_query, (nick,))
        records = cursor.fetchall()
        result = len(records)
    except Error as error:
        print("Ошибка при работе с SQLite", error)
    return result
def search_nick_by_usrname(conn, username):
    result = ()
    try:
        cursor = conn.cursor()
        sqlite_select_query = "SELECT * from users WHERE username=?"
        cursor.execute(sqlite_select_query, (username,))
        records = cursor.fetchall()
        result = records
        return result
    except Error as error:
        print("Ошибка при работе с SQLite", error)
        return result
def ubdate_username(conn, nick, username):
    try:
        cursor = conn.cursor()
        sqlite_ubdate_query = "UPDATE users SET username = ? WHERE nick = ?"
        cursor.execute(sqlite_ubdate_query, (username, nick))
        conn.commit()
    except Error as error:
        print("Ошибка при работе с SQLite", error)
def insert_pass(conn, guest_fio, user_fio, data_visit = None, time_visit = None, status = "create"):
    try:
        cursor = conn.cursor()
        sql_update_query = "INSERT INTO orders (name, visitant, status, data_visit, time_visit) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(sql_update_query, (user_fio, guest_fio, status, data_visit, time_visit))
        conn.commit()
    except Error as error:
        print("Ошибка при работе с SQLite", error)
def main():
    conn = create_data_base("db.db")
    insert_in_db(conn, "Veronica Nazamova", "rosyvelm", 1)
    insert_in_db(conn, "Pavel Lovah", "princess", 1)
    conn.close()

if __name__ == '__main__':
    main()