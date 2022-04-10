from datetime import datetime

from loguru import logger
from mysql.connector import MySQLConnection, Error

def select_record(coin_name, price):
    query = """select * from data where coin_name = %s and price like %s"""
    try:
        conn = MySQLConnection(host="localhost", user="root", db="screener")
        cursor = conn.cursor()
        cursor.execute(query, (coin_name, price))
        result = cursor.fetchall()
        if len(result) > 0:
            return(result[0])
        else:
            return(False)
    except Error as error:
        logger.error(error)
    finally:
        conn.close()



def select_records_by_coin_name(coin_name):
    query = """select * from data where coin_name = %s"""
    try:
        conn = MySQLConnection(host="localhost", user="root", db="screener")
        cursor = conn.cursor()
        cursor.execute(query, (coin_name, ))
        result = cursor.fetchall()
        if len(result) > 0:
            return(result)
        else:
            return(False)
    except Error as error:
        logger.error(error)
    finally:
        conn.close()

def select_all_records():
    query = """select * from data"""
    try:
        conn = MySQLConnection(host="localhost", user="root", db="screener")
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) > 0:
            return(result)
        else:
            return(False)
    except Error as error:
        logger.error(error)
    finally:
        conn.close()

def select_get_an_accepted_records(dt):
    query = """SELECT * from data where dt < %s"""
    try:
        conn = MySQLConnection(host="localhost", user="root", db="screener")
        cursor = conn.cursor()
        cursor.execute(query, (dt,))
        result = cursor.fetchall()
        if len(result) > 0:
            return(result)
        else:
            return(False)
    except Error as error:
        logger.error(error)
    finally:
        conn.close()

def select_get_an_verified_record():
    query = """SELECT * from data where in_range = 1"""
    try:
        conn = MySQLConnection(host="localhost", user="root", db="screener")
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) > 0:
            return(result)
        else:
            return(False)
    except Error as error:
        logger.error(error)
    finally:
        conn.close()

def select_user_id(user_id):
    query = """SELECT * from user_id where user_id = %s"""
    try:
        conn = MySQLConnection(host="localhost", user="root", db="screener")
        cursor = conn.cursor()
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        if len(result) > 0:
            return(result[0])
        else:
            return(False)
    except Error as error:
        logger.error(error)
    finally:
        conn.close()

def select_all_user_id():
    query = """SELECT user_id from user_id """
    try:
        conn = MySQLConnection(host="localhost", user="root", db="screener")
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) > 0:
            return(result)
        else:
            return(False)
    except Error as error:
        logger.error(error)
    finally:
        conn.close()

def select_coin_current_price(coin_name):
    query = """SELECT * from current_price where coin_name = %s"""
    try:
        conn = MySQLConnection(host="localhost", user="root", db="screener")
        cursor = conn.cursor()
        cursor.execute(query, (coin_name,))
        result = cursor.fetchall()
        if len(result) > 0:
            return(result[0][2])
        else:
            return(False)
    except Error as error:
        logger.error(error)
    finally:
        conn.close()

def insert_depth(coin_name, price, count, dt):
    query = """INSERT INTO data
        (coin_name, price, count, dt, in_range)
        VALUES (%s, %s, %s, %s, 0);"""
    try:
        conn = MySQLConnection(host="localhost", user="root", db="screener")
        cursor = conn.cursor()
        cursor.execute(query, (coin_name, price, count, dt))
        conn.commit()
    except Error as error:
        logger.error(error)
    finally:
        conn.close()

def insert_price(coin_name, price):
    query = """INSERT INTO current_price
        (coin_name, price)
        VALUES (%s, %s);"""
    try:
        conn = MySQLConnection(host="localhost", user="root", db="screener")
        cursor = conn.cursor()
        cursor.execute(query, (coin_name, price))
        conn.commit()
    except Error as error:
        logger.error(error)
    finally:
        conn.close()

def insert_user_id(user_id):
    query = """INSERT INTO user_id
        (user_id)
        VALUES (%s);"""
    try:
        conn = MySQLConnection(host="localhost", user="root", db="screener")
        cursor = conn.cursor()
        cursor.execute(query, (user_id,))
        conn.commit()
    except Error as error:
        logger.error(error)
    finally:
        conn.close()    

def update_currnet_price(coin_name, price):
    query = """Update current_price set price = %s where coin_name = %s"""
    try:
        conn = MySQLConnection(host="localhost", user="root", db="screener")
        cursor = conn.cursor()
        cursor.execute(query, (price, coin_name))
        conn.commit()
    except Error as error:
        logger.error(error)
    finally:
        conn.close()

def update_record(coin_name, price, count, dt):
    query = """Update data set count = %s, dt= %s where coin_name = %s and price like %s"""
    try:
        conn = MySQLConnection(host="localhost", user="root", db="screener")
        cursor = conn.cursor()
        cursor.execute(query, (count, dt, coin_name, price))
        conn.commit()
    except Error as error:
        logger.error(error)
    finally:
        conn.close()

def update_out_from_range (coin_name, price):
    query = """Update data set in_range = 0 where coin_name = %s and price like '%s%'"""
    try:
        conn = MySQLConnection(host="localhost", user="root", db="screener")
        cursor = conn.cursor()
        cursor.execute(query, (coin_name, price))
        conn.commit()
    except Error as error:
        logger.error(error)
    finally:
        conn.close()

def update_enter_range (coin_name, price, dt):
    query = """Update data set in_range = 1, timer = %s where coin_name = %s and price like '%s%'"""
    try:
        conn = MySQLConnection(host="localhost", user="root", db="screener")
        cursor = conn.cursor()
        cursor.execute(query, (dt, coin_name, price))
        conn.commit()
    except Error as error:
        logger.error(error)
    finally:
        conn.close() 

def delete_record(coin_name, price):
    query = "DELETE from data where coin_name = %s and price like %s"
    try:
        conn = MySQLConnection(host="localhost", user="root", db="screener")
        cursor = conn.cursor()
        cursor.execute(query, (coin_name, price))
        conn.commit()
    except Error as error:
        logger.error(error)
    finally:
        conn.close()

def delete_all_data():
    query1 = "DELETE FROM data"
    query2 = "DELETE FROM current_price"
    try:
        conn = MySQLConnection(host="localhost", user="root", db="screener")
        cursor = conn.cursor()
        cursor.execute(query1)
        cursor.execute(query2)
        conn.commit()
    except Error as error:
        logger.error(error)
    finally:
        conn.close()