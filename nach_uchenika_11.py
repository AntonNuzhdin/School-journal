import sqlite3
import os


put = 'baza_for_sait.db'

def nach_uchenika(login):
    con = sqlite3.connect(put)
    # Создание курсора
    cur = con.cursor()
    klass = cur.execute(f'SELECT класс FROM klas_ruk_11 WHERE login = \'{login}\'').fetchall()[0][0]
    ucheniki = cur.execute(f'SELECT фио, присутствие FROM student_11 WHERE класс = \'{klass}\'').fetchall()
    return ucheniki
