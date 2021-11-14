from hash_update import generate_select
import os
import sqlite3
from random import shuffle


put = 'baza_for_sait.db'


needs_a = [4, 5, 6, 7, 9, 10, 11, 19]
con = sqlite3.connect(put)
cur = con.cursor()
"""for i in needs_a:
    sel_zap = generate_select('students', ['почта', 'klass'], 'klass', i)
    res = cur.execute(sel_zap).fetchall()
    print(f'{i}: {len(res)}')"""
sel_zap = generate_select('students', ['id', 'klass'])
res = cur.execute(sel_zap).fetchall()
res = [i[0] for i in res if i[1] in needs_a]
#for i in res:
#    print(i)
kol = len(res)
aud = round(kol / 15) + 1
shuffle(res)
rass = []
for i in range(aud):
    rass.append([].copy())
for i in range(aud):
    a = i * 15
    b = (i + 1) * 15
    rass[i] = res[a:b]
for i in range(len(rass)):
    print(i + 1, rass[i])
con.commit()
con.close()
