from datetime import datetime
import sqlite3

def select_info(namecoin, price):
    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sql_select_query = """select * from Data where coinname = ? and price = ?"""
        cursor.execute(sql_select_query, (namecoin, price))
        records = cursor.fetchall()
        ls = []
        if len(records) > 0:
            for row in records:
                return(row[3])
                
        else:
            print('\nno records\n')

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

def insert_into_table(coinname, price, count, time):

    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_insert_with_param = """INSERT INTO Data
                            (coinname, price, count, time)
                            VALUES (?, ?, ?, ?);"""
        data_tuple = (coinname, price, count, time)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()
        print("Запись успешно вставлена ​​в таблицу sqlitedb_developers ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

def update_sqlite_table(coinname, price, count, time):
    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sql_update_query = """Update Data set count = ?, time= ? where coinname = ? and price = ?"""
        data = (count, time, coinname, price)
        cursor.execute(sql_update_query, data)
        sqlite_connection.commit()
        print("Запись успешно обновлена")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def delete_sqlite_record(dev_id):
    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sql_update_query = """DELETE from Data where id = ?"""
        cursor.execute(sql_update_query, (dev_id, ))
        sqlite_connection.commit()
        print("Запись успешно удалена")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")



# update_sqlite_table('ADAUSDT', 1.195, 229787.7, str(datetime.now()))
# insert_into_table('btcusdt', 43000.56546545, 100.65465, str(datetime.now()))
# print(f"Объем заявки: {select_info('btcusdt', 43000.56546545)}")
# delete_sqlite_record(5)
