import sqlite3
import os
import datetime

put = 'baza_for_sait.db'

def isClassBossOrTeacher(login, pw):
# [кл_рук, teacher_ppv]
    #[0, 1]
    global put
    all = []
    con = sqlite3.connect(put)

    # Создание курсора
    cur = con.cursor()
    #находим по логину пользователя
    result = cur.execute('''SELECT фио FROM klas_ruk_11 WHERE login = \'''' + login + '\' AND pw = \'''' + pw + '\'''').fetchall()
    result_2 = cur.execute('''SELECT фио FROM teacher_ppv WHERE login = \'''' + login + '\' AND pw = \'''' + pw + '\'''').fetchall()
    print(len(result_2))
    if len(result) >= 1:
        all.append(1)
    else:
        all.append(0)
    if len(result_2) >= 1:
        all.append(1)
    else:
        all.append(0)
    return all


def studentsInfoForTeachers(login):
    global put
    con = sqlite3.connect(put)
    cur = con.cursor()
    idTeacher = cur.execute(f'''SELECT id FROM teacher_ppv WHERE login = \'{login}\'''').fetchall()[0][0]
    dayNumber = 4
    fullPpv = str(idTeacher)+','+str(dayNumber)
    studentInfo = cur.execute(f'''SELECT * FROM student_11 WHERE ппв_1 = \'{fullPpv}\' OR ппв_2 = \'{fullPpv}\' OR ппв_3 = \'{fullPpv}\' OR ппв_4 = \'{fullPpv}\' OR ппв_5 = \'{fullPpv}\' OR ппв_6 = \'{fullPpv}\' ''').fetchall()
    return studentInfo


def nach_uchenika(login):
    con = sqlite3.connect(put)
    # Создание курсора
    cur = con.cursor()
    klass = cur.execute(f'SELECT класс FROM klas_ruk_11 WHERE login = \'{login}\'').fetchall()[0][0]
    ucheniki = cur.execute(f'SELECT фио, присутствие FROM student_11 WHERE класс = \'{klass}\'').fetchall()
    return ucheniki

def classBossName(login):
    con = sqlite3.connect(put)
    # Создание курсора
    cur = con.cursor()
    name = cur.execute(f'SELECT фио FROM klas_ruk_11 WHERE login = \'{login}\'').fetchall()
    return name

def teacherName(login):
    con = sqlite3.connect(put)
    # Создание курсора
    cur = con.cursor()
    name = cur.execute(f'SELECT фио FROM teacher_ppv WHERE login = \'{login}\'').fetchall()
    return name
