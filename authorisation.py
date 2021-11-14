import sqlite3
from hashing import check_password
from hash_update import generate_select
import os



put = 'baza_for_sait.db'



def check(table, email, user_password):
    global cur
    has_zap = generate_select(table, ['код'], 'почта', email)
    if cur.execute(has_zap).fetchall():
        hashed_password = cur.execute(has_zap).fetchall()[0][0]
        return check_password(hashed_password, user_password)
    else:
        return False


def wdb_check(table, email, password, db=put):
    global cur
    con = sqlite3.connect(f"{db}")
    cur = con.cursor()
    res = check(table, email, password)
    con.commit()
    con.close()
    return res
