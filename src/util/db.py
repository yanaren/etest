
import MySQLdb as mdb
from src.deploy import DNS

def execute(sql):
    con = None
    try:
        con = mdb.connect(host=DNS['DB_HOST'],
                          user=DNS['DB_USER'],
                          passwd=DNS['DB_PASS'],
                          db=DNS['DB_DATABASE'],
                          port=DNS['DB_PORT']);

        cur = con.cursor()
        cur.execute(sql)
        if sql.split(' ')[0] == 'insert' or sql.split(' ')[0] == 'update':
            con.commit()
        data = cur.fetchall()
        cur.close()
        return data
    finally:
        if con:
            con.close()

def callproc(callname, args):
    con = None
    try:
        con = mdb.connect(host=DNS['DB_HOST'],
                          user=DNS['DB_USER'],
                          passwd=DNS['DB_PASS'],
                          db=DNS['DB_DATABASE'],
                          port=DNS['DB_PORT']);

        cur = con.cursor()
        cur.callproc(callname, args)
        con.commit()
        data = cur.fetchall()
        cur.close()
        return data
    finally:
        if con:
            con.close()

