import sqlite3
import os
from hashing import check_password


put = 'baza_for_sait.db'

def check_log_pas(login, password): #проверяет логин и пароль на верность ввода
    # Подключение к БД
    global put
    con = sqlite3.connect(put)

    # Создание курсора
    cur = con.cursor()
    #находим по логину пользователя
    result = cur.execute('''SELECT * FROM students WHERE почта = \'''' + login + '\'').fetchall()
    con.close()
    otchet_log = False
    otchet_pas = False
    if result: #если что то нашлось то отчет логин даем 1
        otchet_log = True
        #идет проверка пароля
        if check_password(result[0][3], password): #если пароль введен верно меняем пароль на 1
            otchet_pas = True
            return otchet_log, otchet_pas, result[0]
        else:
            result = list()
            return otchet_log, otchet_pas, result
    else:
        result = list()
        return otchet_log, otchet_pas, result


def zapis_v_bazu(predmet, login, prioritet):
    global put
    con = sqlite3.connect(put)
    # Создание курсора
    cur = con.cursor()
    #находим по логину пользователя
    if prioritet == 1:
        if predmet == "Физико-математическое направление":
            predmet = "1"
        elif predmet == "Направление с углубленным изучением иностранного языка":
            predmet = "2"
        elif predmet == "Инженерное направление":
            predmet = "5"
        elif predmet == "Информационно-технологическое направление":
            predmet = "4"
        elif predmet == "Естественнонаучное направление: химико-биологическое":
            predmet = "3"
        elif predmet == "Экономико-математическое направление":
            predmet = "6"
        elif predmet == "Универсальное направление":
            predmet = "7"
        elif predmet == "Естественнонаучное направление: физико-химическое":
            predmet = "8"
        result = cur.execute('''UPDATE students set prioritet_one = \'''' + predmet
                             + '\' WHERE  почта = \'' + login + '\'').fetchall()
    elif prioritet == 2:
        if predmet == "Физико-математическое направление":
            predmet = "1"
        elif predmet == "Направление с углубленным изучением иностранного языка":
            predmet = "2"
        elif predmet == "Инженерное направление":
            predmet = "5"
        elif predmet == "Информационно-технологическое направление":
            predmet = "4"
        elif predmet == "Естественнонаучное направление: химико-биологическое":
            predmet = "3"
        elif predmet == "Экономико-математическое направление":
            predmet = "6"
        elif predmet == "Универсальное направление":
            predmet = "7"
        elif predmet == "Естественнонаучное направление: физико-химическое":
            predmet = "8"
        result = cur.execute('''UPDATE students set prioritet_two = \'''' + predmet
                             + '\' WHERE  почта = \'' + login + '\'').fetchall()
    elif prioritet == 3:
        if predmet == "Физико-математическое направление":
            predmet = "1"
        elif predmet == "Направление с углубленным изучением иностранного языка":
            predmet = "2"
        elif predmet == "Инженерное направление":
            predmet = "5"
        elif predmet == "Информационно-технологическое направление":
            predmet = "4"
        elif predmet == "Естественнонаучное направление: химико-биологическое":
            predmet = "3"
        elif predmet == "Экономико-математическое направление":
            predmet = "6"
        elif predmet == "Универсальное направление":
            predmet = "7"
        elif predmet == "Естественнонаучное направление: физико-химическое":
            predmet = "8"
        result = cur.execute('''UPDATE students set prioritet_tree = \'''' + predmet
                            + '\' WHERE  почта = \'' + login + '\'').fetchall()
    con.commit()
    con.close()


def check_teacher(login, password):
    global put
    con = sqlite3.connect(put)

    # Создание курсора
    cur = con.cursor()
    #находим по логину пользователя
    result = cur.execute('''SELECT * FROM teachers WHERE  почта = \'''' + login + '\'').fetchall()
    #print(result)
    con.close()
    #print(result)
    otchet_log = False
    otchet_pas = False
    if result: #если что то нашлось то отчет логин даем 1
        otchet_log = True
        #идет проверка пароля
        if check_password(result[0][4], password): #если пароль введен верно меняем пароль на 1
            otchet_pas = True
            return otchet_log, otchet_pas, result[0]
        else:
            result = list()
            return otchet_log, otchet_pas, result
    else:
        result = list()
        return otchet_log, otchet_pas, result

def classes_list():
    global put
    classes = []
    con = sqlite3.connect(put)

    # Создание курсора
    cur = con.cursor()
    #находим по логину пользователя
    result = cur.execute('''SELECT klass_name FROM klass_bukva''').fetchall()
    con.close()
    #print(result)
    for i in result:
        classes.append(i)
    return classes


def zapis_comments(name, comment, rek, predmet):
    global put
    con = sqlite3.connect(put)
    # Создание курсора
    cur = con.cursor()
    if predmet == 1:
        result = cur.execute('''UPDATE teacher_notes set physics_comment = \'''' + comment
                         + '\' WHERE fio = \'' + name + '\'').fetchall()
        result = cur.execute('''UPDATE teacher_notes set phys_rek = \'''' + rek
                         + '\' WHERE fio = \'' + name + '\'').fetchall()

    elif predmet == 2:
        result = cur.execute('''UPDATE teacher_notes set foreign_lang = \'''' + comment
                         + '\' WHERE fio = \'' + name + '\'').fetchall()
        result = cur.execute('''UPDATE teacher_notes set foreign_rek = \'''' + rek
                         + '\' WHERE fio = \'' + name + '\'').fetchall()
    elif predmet == 3:
        result = cur.execute('''UPDATE teacher_notes set draftsmanship_comment = \'''' + comment
                         + '\' WHERE fio = \'' + name + '\'').fetchall()
        result = cur.execute('''UPDATE teacher_notes set cherch_rek = \'''' + rek
                         + '\' WHERE fio = \'' + name + '\'').fetchall()
    elif predmet == 4:
        result = cur.execute('''UPDATE teacher_notes set biology_comment = \'''' + comment
                         + '\' WHERE fio = \'' + name + '\'').fetchall()
        result = cur.execute('''UPDATE teacher_notes set bio_rek = \'''' + rek
                         + '\' WHERE fio = \'' + name + '\'').fetchall()
    elif predmet == 5:
        result = cur.execute('''UPDATE teacher_notes set informatic_comment = \'''' + comment
                         + '\' WHERE fio = \'' + name + '\'').fetchall()
        result = cur.execute('''UPDATE teacher_notes set info_rek = \'''' + rek
                         + '\' WHERE fio = \'' + name + '\'').fetchall()
    elif predmet == 6:
        result = cur.execute('''UPDATE teacher_notes set maths_comment = \'''' + comment
                         + '\' WHERE fio = \'' + name + '\'').fetchall()
        result = cur.execute('''UPDATE teacher_notes set math_rek = \'''' + rek
                         + '\' WHERE fio = \'' + name + '\'').fetchall()
    elif predmet == 7:
        result = cur.execute('''UPDATE teacher_notes set russian_comment = \'''' + comment
                         + '\' WHERE fio = \'' + name + '\'').fetchall()
        result = cur.execute('''UPDATE teacher_notes set rus_rek = \'''' + rek
                         + '\' WHERE fio = \'' + name + '\'').fetchall()
    elif predmet == 8:
        result = cur.execute('''UPDATE teacher_notes set chemistry = \'''' + comment
                         + '\' WHERE fio = \'' + name + '\'').fetchall()
        result = cur.execute('''UPDATE teacher_notes set chem_rek = \'''' + rek
                         + '\' WHERE fio = \'' + name + '\'').fetchall()
    elif predmet == 9:
        result = cur.execute('''UPDATE teacher_notes set obsh_comment = \'''' + comment
                         + '\' WHERE fio = \'' + name + '\'').fetchall()
        result = cur.execute('''UPDATE teacher_notes set obsh_rek = \'''' + rek
                         + '\' WHERE fio = \'' + name + '\'').fetchall()

    con.commit()
    con.close()


def pois_predmeta(login):
    global put
    con = sqlite3.connect(put)
    # Создание курсора
    cur = con.cursor()
    id_predmet = cur.execute(f'''SELECT stud_predmet FROM teachers WHERE  почта = \'{login}\'''').fetchall()
    return id_predmet[0][0]


def opred_ter(login):
    global put
    con = sqlite3.connect(put)
    cur = con.cursor()
    zapros = f'''SELECT name_korpus FROM territory WHERE id = (SELECT korpus FROM klass_bukva
                WHERE id = (SELECT klass FROM students WHERE почта = \'{login}\'))'''
    ter = cur.execute(zapros).fetchall()
    return ter[0][0]

def marks(login):
    global put
    test = dict()
    put_mark = '/Users/antonnuzhdin/Yandex.Disk.localized/new_abulance/https/vse_mark.db'
    con = sqlite3.connect(put)
    cur = con.cursor()
    mark_con = sqlite3.connect(put_mark)
    mark_cur = mark_con.cursor()
    zap_id = f'''SELECT id from students WHERE почта = \'{login}\''''
    id = cur.execute(zap_id).fetchall()[0][0]
    all = mark_cur.execute(f'''SELECT * FROM mark WHERE id = {id}''').fetchall()
    marks = [i for i in all[0][1::]]
    test['биология'] = mark_cur.execute(f'''SELECT биология FROM mark WHERE id = {id}''').fetchall()[0][0]
    test['химия'] = mark_cur.execute(f'''SELECT химия FROM mark WHERE id = {id}''').fetchall()[0][0]
    test['информатика'] = mark_cur.execute(f'''SELECT информатика FROM mark WHERE id = {id}''').fetchall()[0][0]
    return marks, test


#print(marks('nuzhdin-ao@stu.1502.moscow'))
def var_him(login):
    global put
    put_mark = '/Users/antonnuzhdin/Yandex.Disk.localized/new_abulance/https/vse_mark.db'
    con = sqlite3.connect(put)
    cur = con.cursor()
    info = [] * 2
    mark_con = sqlite3.connect(put_mark)
    mark_cur = mark_con.cursor()
    zap_id = f'''SELECT id from students WHERE почта = \'{login}\''''
    id = cur.execute(zap_id).fetchall()[0][0]
    all = mark_cur.execute(f'''SELECT вар_химия FROM mark WHERE id = {id}''').fetchall()
    return all[0][0]
def var_stepik(id_stepik, login):
    with open("var_login.txt", 'a') as f:
        f.write(f'''Логин: {login}, id: {id_stepik} \n''' )


def to_class(login):
    global put
    # put = '/Users/antonnuzhdin/Yandex.Disk.localized/new_abulance/baza_for_sait.db'

    con = sqlite3.connect(put)
    cur = con.cursor()
    req_fio = f'''SELECT ФИО from students WHERE почта = \'{login}\''''
    fio = cur.execute(req_fio).fetchall()[0][0]
    req_to_class = f'''SELECT to_class FROM admission WHERE fio=\'{fio}\''''
    to_class = cur.execute(req_to_class).fetchall()[0][0]
    return to_class
