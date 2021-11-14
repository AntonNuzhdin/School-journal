from hashing import hash_password
import sqlite3


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


def obrabotka(table, pas_name):
    global cur
    users = cur.execute(f"SELECT id FROM {table}").fetchall()
    for user_id in users:
        user_id = user_id[0]
        pas_zap = generate_select(table, [pas_name], 'id', str(user_id))
        password = cur.execute(pas_zap).fetchall()[0][0]
        passwords = open('passwords.txt', 'a', encoding='utf-8')
        if (":" not in password) or 1:
            hashed = hash_password(password)
            if table == 'students':
                fio_zap = generate_select(table, ['fio'], 'id', str(user_id))
            if table == 'teachers':
                fio_zap = generate_select(table, ['fio_teacher'], 'id', str(user_id))
            fio = cur.execute(fio_zap).fetchall()[0][0]
            passwords.write(f'\n{fio}: {password}')
            upl_zap = generate_update(table, pas_name, hashed, 'id', str(user_id))
            cur.execute(upl_zap)
        passwords.close()

def fin(db_name):
    global cur
    con = sqlite3.connect(f"{db_name}")
    cur = con.cursor()
    obrabotka('students', 'password')
    obrabotka('teachers', 'password_teacher')
    con.commit()
    con.close()


msg = """!!!WARNING!!!
1) Database name without .db
2) Programm work with teachers table(password_teacher field) and students table(password field)
INSERT YOUR DATABASE NAME FOR ENCODING:
>"""
#db_name = input(msg)
#fin(db_name)
