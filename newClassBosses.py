import sqlite3
import os
from hashing import check_password


put = 'baza_for_sait.db'

con = sqlite3.connect(put)

# Создание курсора
cur = con.cursor()

classes = cur.execute(f'SELECT * FROM boss_klass').fetchall()
print(classes)
