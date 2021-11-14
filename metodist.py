import sqlite3
import json
import sys
from mail_otpr import *

put = 'baza_for_sait.db'
put_mark = 'vse_mark.db'
put_json = 'static/'


def sost_student(predmet, prior, students, naprav, id):
    global put
    global put_mark
    con = sqlite3.connect(put)
    cur = con.cursor()

    mark_con = sqlite3.connect(put_mark)
    mark_cur = mark_con.cursor()

    if naprav == 8:
        poisk = f'((prioritet_{prior} = 3) or (prioritet_{prior} = 8))'
    else:
        poisk = f'(prioritet_{prior} = {naprav})'
    zapros = f'SELECT id, ФИО, klass FROM students WHERE {poisk}'
    result = cur.execute(zapros).fetchall()
    for man in result:
        student = dict()
        if man[0] in id:
            continue
        student['id'] = man[0]
        id.append(man[0])
        student['lesson'] = predmet
        student['fio'] = man[1]
        klass = cur.execute(f'SELECT klass_name FROM klass_bukva WHERE (id = {man[2]})').fetchall()
        student['klass'] = klass[0][0]
        mark = mark_cur.execute(f'SELECT {predmet} FROM mark WHERE (id = {man[0]})').fetchall()
        student['mark'] = mark[0][0]
        variant = mark_cur.execute(f'SELECT вар_{predmet} FROM mark WHERE (id = {man[0]})').fetchall()
        student['var'] = variant[0][0]
        students.append(student)
    return students



def poisk():
    golova = dict()
    students = list()
    id = list()
    naprav, predmet = 3, 'биология'
    students = sost_student(predmet, 'one', students, naprav, id)
    students = sost_student(predmet, 'two', students, naprav, id)
    students = sost_student(predmet, 'tree', students, naprav, id)
    golova[predmet] = students

    id = list()
    students = list()
    naprav, predmet = 4, 'информатика'
    students = sost_student(predmet, 'one', students, naprav, id)
    students = sost_student(predmet, 'two', students, naprav, id)
    students = sost_student(predmet, 'tree', students, naprav, id)
    golova[predmet] = students

    id = list()
    students = list()
    naprav, predmet = 8, 'химия'
    students = sost_student(predmet, 'one', students, naprav, id)
    students = sost_student(predmet, 'two', students, naprav, id)
    students = sost_student(predmet, 'tree', students, naprav, id)
    golova[predmet] = students

    with open(f'{put_json}metodist.json', 'w', encoding = 'UTF-8') as file:
        json.dump(golova, file, ensure_ascii = False)


def vivod_prof(login):
    global put
    con = sqlite3.connect(put)
    cur = con.cursor()
    id_student = cur.execute(f'SELECT id FROM students WHERE (почта = \'{login}\')').fetchall()[0][0]
    print(id_student)
    flag = dict()
    students = list()
    id = list()
    naprav, predmet = 3, 'биология'
    students = sost_student(predmet, 'one', students, naprav, id)
    students = sost_student(predmet, 'two', students, naprav, id)
    students = sost_student(predmet, 'tree', students, naprav, id)
    for element in students:
        if element['id'] == id_student:
            flag[predmet] = element['var']
            break

    id = list()
    students = list()
    naprav, predmet = 4, 'информатика'
    students = sost_student(predmet, 'one', students, naprav, id)
    students = sost_student(predmet, 'two', students, naprav, id)
    students = sost_student(predmet, 'tree', students, naprav, id)
    for element in students:
        if element['id'] == id_student:
            flag[predmet] = element['var']
            break

    id = list()
    students = list()
    naprav, predmet = 8, 'химия'
    students = sost_student(predmet, 'one', students, naprav, id)
    students = sost_student(predmet, 'two', students, naprav, id)
    students = sost_student(predmet, 'tree', students, naprav, id)
    for element in students:
        if element['id'] == id_student:
            flag[predmet] = element['var']
            break

    return flag



def uved_otp():
    global put
    con = sqlite3.connect(put)
    cur = con.cursor()
    golova = dict()
    students = list()
    id = list()
    naprav, predmet = 8, 'химия'
    students = sost_student(predmet, 'one', students, naprav, id)
    students = sost_student(predmet, 'two', students, naprav, id)
    students = sost_student(predmet, 'tree', students, naprav, id)
    for element in students:
        zapros = f'select почта from students where id = {element["id"]}'
        poluchatel = cur.execute(zapros).fetchall()[0][0]
        text = f'''
        <p>&nbsp;<img src="https://1502энергия.рф/static/imgs/LOGO_HOME.png" alt="" style="display: block; margin-left: auto; margin-right: auto;" /></p>
<p style="text-align: center;"><strong>Доброго времени суток, {element['fio']}!</strong></p>
<p style="text-align: center;"></p>
<p style="text-align: center;"><strong></strong></p>
<p style="text-align: center;"><strong>В личном кабинете на ресурсе <a href="1502энергия.рф">1502энергия.рф</a>&nbsp; появилась информация о проведении олимпиады по химии.</strong></p>
<p style="text-align: center;"><strong>Внимательно ознакомтесь со всеми уловиями проведения.&nbsp;</strong></p>
<p style="text-align: center;"><strong>В конференцию ZOOM нужно заходить под своей фамилией и именем, в противном случае Вы будете дисквалифицированы с олимпиады.</strong></p>

            '''
        tema_msg = 'Олимпиада по химии'
        otpravka(poluchatel, tema_msg, text)


def variant():
    global put_mark
    mark_con = sqlite3.connect(put_mark)
    mark_cur = mark_con.cursor()
    id = list()
    students = list()
    naprav, predmet = 3, 'биология'
    students = sost_student(predmet, 'one', students, naprav, id)
    students = sost_student(predmet, 'two', students, naprav, id)
    students = sost_student(predmet, 'tree', students, naprav, id)
    i = 1
    j = 1
    for element in students:
        var = str(i) + str(j)
        zapros = f'UPDATE mark SET вар_биология = {int(var)} WHERE (id = {element["id"]})'
        poluchatel = mark_cur.execute(zapros)
        i += 1
        if i > 4:
            i = 1
        if i == 1:
            j += 1
        if j > 3:
            j = 1
    mark_con.commit()
    mark_con.close()


def form_var():
    global put_mark
    mark_con = sqlite3.connect(put_mark)
    mark_cur = mark_con.cursor()

    global put
    con = sqlite3.connect(put)
    cur = con.cursor()
    g = 1
    teacher = {
    1 : 'Шабалин В.Г.',
    2 : 'Блинков Е.А.',
    3 : 'Чернышова Ю. Н.',
    4 : 'Платонычева О.В',
    5 : 'Кравченко О.В.',
    6 : 'Руднева М.Н.'
    }
    print('Химия')

    for i in range(1, 7):
        kol = 1
        zapros = f'select id from mark where вар_химия = {i}'
        spisok_id = mark_cur.execute(zapros).fetchall()
        for id in spisok_id:
            zapros = f'select ФИО from students where id = {id[0]}'
            fio = cur.execute(zapros).fetchall()
            print(f'{g}\t{teacher[i]}\t{kol}. {fio[0][0]}')
            kol += 1
            g += 1

    print('\n\nБиология\n\n')
    teacher = {
    1 : 'Чернышова Ю.Н.',
    2 : 'Блинков Е.А.',
    3 : 'Кравченко О.В.',
    4 : 'Скалепова Л.В.'
    }
    kol = 1
    for i in range(1, 5):
        g = 1
        for j in range(1, 4):
            var = str(i) + str(j)
            zapros = f'select id from mark where вар_биология = {var}'
            spisok_id = mark_cur.execute(zapros).fetchall()
            for id in spisok_id:
                zapros = f'select ФИО from students where id = {id[0]}'
                fio = cur.execute(zapros).fetchall()
                print(f'{kol}\tвариант №{j}\t{teacher[i]}\t{g}. {fio[0][0]}')
                g += 1
                kol += 1
