from hashing import hash_password
from random import choice
import sqlite3
import os

put = 'baza_for_sait.db'
pas = '/new_abulance/passwords.txt'


def generate_update(table, field1, data1, field2, data2):
    zap = f"""UPDATE {table}
SET {field1} = '{data1}'
WHERE {field2} = '{data2}'"""
    return zap


def generate_select(table, fields, usl_field=0, usl=0):
    zap = "SELECT "
    for i in range(len(fields) - 1):
        zap += f"{fields[i]}, "
    zap += f"{fields[-1]} FROM {table}"
    if usl:
        zap += "\n"
        zap += f"WHERE {usl_field} = '{usl}'"
    return zap


def obrabotka(table, pas_name, leng):
    global cur
    global pas
    users = cur.execute(f"SELECT почта FROM {table}").fetchall()
    passwords = open(pas, 'a', encoding='utf-8')
    for email in users:
        email = str(email[0]).strip()
        pas_zap = generate_select(table, [pas_name], 'почта', email)
        password = cur.execute(pas_zap).fetchall()[0][0]
        if (password == None):
            password = randomizer(leng)
#            print(f'{email}: {password}')
            passwords.write(f'\n{email}: {password}')
            hashed = hash_password(password)
            upl_zap = generate_update(table, pas_name, hashed, 'почта', email)
            cur.execute(upl_zap)
    passwords.close()

def fin(leng, tables, db_name=put):
    global cur
    global alet
    alet = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z']
    alet += ['x', 'c', 'v', 'b', 'n', 'm']
    alet += [i.upper() for i in alet]
    alet += ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    con = sqlite3.connect(f"{db_name}")
    cur = con.cursor()
    for i in tables:
        obrabotka(i, 'код', leng)
    con.commit()
    con.close()


def randomizer(leng):
    global alet
    ans = ''
    for i in range(leng):
        ans += choice(alet)
    return ans
#db_name = input(msg)
#fin(db_name)
