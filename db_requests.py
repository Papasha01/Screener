import sqlite3

def select_get_quantity(namecoin, price):
    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()

        sql_select_query = """select * from data where coinname = ? and price = ?"""
        cursor.execute(sql_select_query, (namecoin, price, ))
        records = cursor.fetchall()
        cursor.close()

        if len(records) > 0:
            #print(f'SelectYES {namecoin, price}')
            return(records[0])
        else:
            #print(f'SelectNO {namecoin, price}')
            return(False)

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            
def select_get_an_approved_entry(datetime_):
    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()
        # print(str(datetime_))
        sql_select_query = """SELECT * from data where datetime < ?"""
        cursor.execute(sql_select_query, (str(datetime_),))
        records = cursor.fetchall()
        cursor.close()

        if len(records) > 0:
            return(records)
        else:
            return(False)

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def select_user_id(user_id):
    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()
        # print(str(datetime_))
        sql_select_query = """SELECT * from user_ids where id == ?"""
        cursor.execute(sql_select_query, (user_id,))
        records = cursor.fetchall()
        cursor.close()

        if len(records) > 0:
            return(records)
        else:
            return(False)

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def select_all_user_id():
    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()
        # print(str(datetime_))
        sql_select_query = """SELECT * from user_ids"""
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        cursor.close()

        if len(records) > 0:
            return(records)
        else:
            return(False)

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def insert_into_table(coinname, price, count, time):

    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()


        sqlite_insert_with_param = """INSERT INTO data
                            (coinname, price, count, datetime)
                            VALUES (?, ?, ?, ?);"""
        data_tuple = (coinname, price, count, time)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()
        # print(f"Insert: {coinname, price, count, time}")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def insert_user_id(user_id):

    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()

        sqlite_insert_with_param = """INSERT INTO user_ids VALUES (?);"""
        cursor.execute(sqlite_insert_with_param, (user_id, ))
        sqlite_connection.commit()
        # print(f"Insert: {user_id}")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            
def update_sqlite_table(coinname, price, count, time):
    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()

        sql_update_query = """Update data set count = ?, datetime= ? where coinname = ? and price = ?"""
        data_tuple = (count, time, coinname, price)
        cursor.execute(sql_update_query, data_tuple)
        sqlite_connection.commit()
        #print(f"Update: {coinname, price, count, time}")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            
def delete_sqlite_record(coinname, price):
    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()

        sql_update_query = """DELETE from data where coinname = ? and price = ?"""
        cursor.execute(sql_update_query, (coinname, price, ))
        sqlite_connection.commit()
        # print(f"Delete: {coinname, price}")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

# update_sqlite_table('ADAUSDT', 1.195, 229787.7, str(datetime.now()))
#insert_into_table('btcusdt', 43000.56546545, 100.65465, str(datetime.now()))
# print(f"Объем заявки: {select_info('btcusdt', 43000.56546545)}")
# delete_sqlite_record(5)
# select_get_an_approved_entry(datetime(2023,1,1))
