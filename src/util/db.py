# make sure DB info is right before use this tool
import MySQLdb as mdb
from src.deploy import DB, DNS

def execute(DB, sql=''):
    con = None
    try:
        con = mdb.connect(host=DB['DB_HOST'],
                          user=DB['DB_USER'],
                          passwd=DB['DB_PASS'],
                          db=DB['DB_DATABASE'],
                          port=DB['DB_PORT']);
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
        con = mdb.connect(host=DB['DB_HOST'],
                          user=DB['DB_USER'],
                          passwd=DB['DB_PASS'],
                          db=DB['DB_DATABASE'],
                          port=DB['DB_PORT']);

        cur = con.cursor()
        cur.callproc(callname, args)
        con.commit()
        data = cur.fetchall()
        cur.close()
        return data
    finally:
        if con:
            con.close()

