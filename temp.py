import sqlite3

def insert(name, info):
    try:
        sqlite_connection = sqlite3.connect('test.db')
        cursor = sqlite_connection.cursor()

        sqlite_insert_with_param = """INSERT INTO test
                            (name, info)
                            VALUES (?, ?);"""
        data_tuple = (name, info)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def update(name, id):
    try:
        sqlite_connection = sqlite3.connect('test.db')
        cursor = sqlite_connection.cursor()
        sql_update_query = """Update test set name = 'XXX' where id = ?"""
        data_tuple = (name, id)
        cursor.execute(sql_update_query, data_tuple)
        
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
        
    finally:
        if sqlite_connection:
            sqlite_connection.close()

insert('pavel', 'levykin')