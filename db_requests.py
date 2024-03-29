import sqlite3
from loguru import logger

def select_record(coin_name, price):
    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()
        sql_select_query = """select * from data where coin_name = ? and price = ?"""
        cursor.execute(sql_select_query, (coin_name, price, ))
        records = cursor.fetchall()
        cursor.close()
        if len(records) > 0:
            return(records[0])
        else:
            return(False)
    except sqlite3.Error as error:
        logger.error(f"Ошибка при работе с SQLite {error}")
        
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def select_records_by_coin_name(coin_name):
    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()
        sql_select_query = """select * from data where coin_name = ?"""
        cursor.execute(sql_select_query, (coin_name,))
        records = cursor.fetchall()
        cursor.close()

        if len(records) > 0:
            return(records)
        else:
            return(False)

    except sqlite3.Error as error:
        logger.error(f"Ошибка при работе с SQLite {error}")
        
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def select_all_records():
    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()
        sql_select_query = """select * from data"""
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        cursor.close()

        if len(records) > 0:
            return(records)
        else:
            return(False)

    except sqlite3.Error as error:
        logger.error(f"Ошибка при работе с SQLite {error}")
        
    finally:
        if sqlite_connection:
            sqlite_connection.close()
     
def select_get_an_accepted_records(dt):
    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()
        sql_select_query = """SELECT * from data where dt < ?"""
        cursor.execute(sql_select_query, (dt,))
        records = cursor.fetchall()
        cursor.close()

        if len(records) > 0:
            return(records)
        else:
            return(False)

    except sqlite3.Error as error:
        logger.error(f"Ошибка при работе с SQLite {error}")
        
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def select_get_an_verified_record():
    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()
        sql_select_query = """SELECT * from data where in_range = 1"""
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        cursor.close()

        if len(records) > 0:
            return(records)
        else:
            return(False)

    except sqlite3.Error as error:
        logger.error(f"Ошибка при работе с SQLite {error}")
        
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def select_user_id(user_id):
    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()
        sql_select_query = """SELECT * from user_ids where id == ?"""
        cursor.execute(sql_select_query, (user_id,))
        records = cursor.fetchall()
        cursor.close()

        if len(records) > 0:
            return(records)
        else:
            return(False)

    except sqlite3.Error as error:
        logger.error(f"Ошибка при работе с SQLite {error}")
        
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def select_all_user_id():
    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()
        sql_select_query = """SELECT * from user_ids"""
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        cursor.close()
        if len(records) > 0:
            return(records)
        else:
            return(False)

    except sqlite3.Error as error:
        logger.error(f"Ошибка при работе с SQLite {error}")
        
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def select_coin_current_price(coin_name):
    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()
        sql_select_query = """SELECT * from current_price where coin_name = ?"""
        cursor.execute(sql_select_query, (coin_name, ))
        records = cursor.fetchall()
        cursor.close()
        if len(records) > 0:
            return(records[0][2])
        else:
            return(False)

    except sqlite3.Error as error:
        logger.error(f"Ошибка при работе с SQLite {error}")
        
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def insert_depth(coin_name, price, count, dt):
    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()
        sqlite_insert_with_param = """INSERT INTO data
                            (coin_name, price, count, dt, in_range)
                            VALUES (?, ?, ?, ?, 0);"""
        data_tuple = (coin_name, price, count, dt)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        logger.error(f"Ошибка при работе с SQLite {error}")
        
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def insert_price(coin_name, price):
    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()
        sqlite_insert_with_param = """INSERT INTO current_price
                            (coin_name, price)
                            VALUES (?, ?);"""
        data_tuple = (coin_name, price)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        logger.error(f"Ошибка при работе с SQLite {error}")
        
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
        cursor.close()

    except sqlite3.Error as error:
        logger.error(f"Ошибка при работе с SQLite {error}")
        
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            
def update_currnet_price(coin_name, price):
    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()
        sql_update_query = """Update current_price set price = ? where coin_name = ?"""
        data_tuple = (price, coin_name)
        cursor.execute(sql_update_query, data_tuple)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        logger.error(f"Ошибка при работе с SQLite {error}")
        
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def update_record(coin_name, price, count, dt):
    try:
        
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()
        sql_update_query = """Update data set count = ?, dt= ? where coin_name = ? and price = ?"""
        data_tuple = (count, dt, coin_name, price)
        cursor.execute(sql_update_query, data_tuple)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        logger.error(f"Ошибка при работе с SQLite {error}")
        
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def update_out_from_range (coin_name, price):
    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()

        sql_update_query = """Update data set in_range = 0 where coin_name = ? and price = ?"""
        data_tuple = (coin_name, price)
        cursor.execute(sql_update_query, data_tuple)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        logger.error(f"Ошибка при работе с SQLite {error}")
        
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def update_enter_range (coin_name, price, dt):
    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()

        sql_update_query = """Update data set in_range = 1, timer = ? where coin_name = ? and price = ?"""
        data_tuple = (dt, coin_name, price)
        cursor.execute(sql_update_query, data_tuple)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        logger.error(f"Ошибка при работе с SQLite {error}")
        
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            
def delete_sqlite_record(coin_name, price):
    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()
        sql_update_query = """DELETE from data where coin_name = ? and price = ?"""
        cursor.execute(sql_update_query, (coin_name, price, ))
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        logger.error(f"Ошибка при работе с SQLite {error}")
        
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def delete_all_data():
    try:
        sqlite_connection = sqlite3.connect('screener.db')
        cursor = sqlite_connection.cursor()

        sql_update_query1 = """DELETE from data"""
        sql_update_query2 = """DELETE from current_price"""
        sql_update_query3 = """DELETE from sqlite_sequence"""
        cursor.execute(sql_update_query1)
        cursor.execute(sql_update_query2)
        cursor.execute(sql_update_query3)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        logger.error(f"Ошибка при работе с SQLite {error}")
        
    finally:
        if sqlite_connection:
            sqlite_connection.close()
