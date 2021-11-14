import sqlite3


put = 'baza_for_sait.db'

def pois_uch(login, one, two, tree):
    global put
    con = sqlite3.connect(put)
    cur = con.cursor()
    zapros = f'UPDATE students SET prioritet_one = {one} WHERE (почта = \'{login}\')'
    admin = cur.execute(zapros)
    zapros = f'UPDATE students SET prioritet_two = {two} WHERE (почта = \'{login}\')'
    admin = cur.execute(zapros)
    zapros = f'UPDATE students SET prioritet_tree = {tree} WHERE (почта = \'{login}\')'
    admin = cur.execute(zapros)
    con.commit()
    con.close()


login, one, two, tree = input(), int(input()), int(input()), int(input())
pois_uch(login, one, two, tree)
