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
        conn = sqlite3.connect(db_file)
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
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_in_db(conn, name, nick, status):  # добавляем username в базу
    try:
        cursor = conn.cursor()
        sql_update_query = """INSERT INTO users(name, nick, status, username) VALUES(?, ?, ?, ?)"""
        count = cursor.execute(sql_update_query, (name, nick, status, None))
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
                                    status_id TEXT NOT NULL,
                                    data_vist DATA,
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
    else:
        print("Error! cannot create the database connection.")
    return conn
def search_nick_in_db(conn, nick):
    result = 0
    try:
        cursor = conn.cursor()
        print("Подключен к SQLite")
        sqlite_select_query = "SELECT * from users WHERE nick=?"
        cursor.execute(sqlite_select_query, (nick,))
        records = cursor.fetchall()
        result = records[0][1] != ''
        for i in records():
            print(i)
    except Error as error:
        print("Ошибка при работе с SQLite", error)
    return result

def search_nick_by_usrname(conn, username):
    result = None
    try:
        cursor = conn.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = "SELECT * from users WHERE username=?"
        cursor.execute(sqlite_select_query, (username,))
        records = cursor.fetchall()
        result = records
    except Error as error:
        print("Ошибка при работе с SQLite", error)
    return result
def main():
    conn = create_data_base("db.db")
    insert_in_db(conn, "Daniil Suvorov", "reynardk", 1)
    insert_in_db(conn, "Veronica F", "rosyvelm", 1)

if __name__ == '__main__':
    main()