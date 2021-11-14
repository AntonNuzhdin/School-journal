import sqlite3

import os


put = 'baza_for_sait.db'


def admin_proverka(login):
    fio = ''
    login = login.lower()
    con = sqlite3.connect(put)
    cur = con.cursor()
    admin = cur.execute(f'''SELECT ФИО FROM admin WHERE (почта = \'{login}\')''').fetchall()
    teacher = cur.execute(f'''SELECT ФИО FROM teachers WHERE (почта = \'{login}\')''').fetchall()
    helper_admin = cur.execute(f'''SELECT ФИО FROM help_admin WHERE (почта = \'{login}\')''').fetchall()
    ter = '  '
    try:
        if admin:
            fio = admin[0][0]
        elif teacher and helper_admin:
            fio = helper_admin[0][0]
            ter = cur.execute(f'''SELECT территория FROM help_admin WHERE (почта = \'{login}\')''').fetchall()
        elif helper_admin:
            fio = helper_admin[0][0]
            ter = cur.execute(f'''SELECT территория FROM help_admin WHERE (почта = \'{login}\')''').fetchall()
        else:
            fio = teacher[0][0]
        return bool(admin), bool(teacher), bool(helper_admin), fio, ter
    except Exception:
        return (0, 0, 0)
    #1 администратор - полный доступ
    # 2 есть в списках учителей
    # 3 помощник администратор - только его территория



#
#a = input()
#print(admin_proverka(login= 'dumina-ms@1502.moscow'))
