import pymysql
import json
import middleware.context as context


def _get_db_connection():

    db_connect_info = context.get_db_info()

    print("Connection info = \n", json.dumps(db_connect_info, indent=2, default=str))

    db_connection = pymysql.connect(**db_connect_info)
    return db_connection


def create_or_update_stock_in_portfolio(db_schema, table_name, stock_ticker, stock_quantity):
    conn = _get_db_connection()
    cur = conn.cursor()
    sql = "CREATE TABLE IF NOT EXISTS " + db_schema + ".`" + table_name + \
          "` (ticker VARCHAR(10) PRIMARY KEY, quantity INT NOT NULL) "
    print("SQL Statement = " + cur.mogrify(sql, None))
    res = cur.execute(sql)
    res = conn.commit()

    sql = "INSERT INTO " + db_schema + "." + table_name + " (ticker, quantity) " \
          + "VALUES ('%s', %s)" % (stock_ticker, stock_quantity) + " ON DUPLICATE KEY UPDATE " + \
          "quantity=quantity+'%s'" % stock_quantity
    print("SQL Statement = " + cur.mogrify(sql, None))
    res = cur.execute(sql)
    res = conn.commit()

    conn.close()

    return res


def sell_stock_in_portfolio(db_schema, table_name, stock_ticker, stock_quantity):
    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "UPDATE " + db_schema + "." + table_name + " SET " + \
          "quantity=quantity-'%s'" % stock_quantity + " where " + \
          "ticker" + " like " + "'" + stock_ticker + "%'"
    print("SQL Statement = " + cur.mogrify(sql, None))
    res = cur.execute(sql)
    res = conn.commit()

    conn.close()

    return res


def get_table(db_schema, table_name):

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()

    conn.close()

    return res


def get_by_prefix(db_schema, table_name, column_name, value_prefix):

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name + " where " + \
        column_name + " like " + "'" + value_prefix + "%'"
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()

    conn.close()

    return res


def delete_by_prefix(db_schema, table_name, column_name, value_prefix):

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "delete from " + db_schema + "." + table_name + " where " + \
        column_name + "=" + "'" + value_prefix + "'"
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = conn.commit()

    conn.close()

    return res


def clear_table(db_schema, table_name):
    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "delete from " + db_schema + "." + table_name
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = conn.commit()

    conn.close()

    return res
