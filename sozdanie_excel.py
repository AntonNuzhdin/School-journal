import sqlite3
from openpyxl import *




def sozdanie():
    title = ['№', 'ФИО', 'Класс', 'Приоритет 1', 'Приоритет 2', 'Приоритет 3', 'алгебра', 'геометрия',
    'русский', 'физика', 'информатика', 'химия', 'иностранный', 'биология',  'Рекомендации']
    put = 'baza_for_sait.db'
    put_mark = 'vse_mark.db'
    con = sqlite3.connect(put)
    cur = con.cursor()

    mark_con = sqlite3.connect(put_mark)
    mark_cur = mark_con.cursor()

    wb = Workbook()
    ws = wb.active
    zapros = 'select ФИО, klass, prioritet_one, prioritet_two, prioritet_tree, id FROM students'
    result = cur.execute(zapros).fetchall()
    ws.append(title)
    number = 1
    for element in result:
        #print(element)
        stroka = list()
        stroka.append(number)
        number += 1
        stroka.append(element[0])
        zapros = f'select klass_name FROM klass_bukva where id = {element[1]}'
        result = cur.execute(zapros).fetchall()
        stroka.append(result[0][0])
        if element[2]:
            zapros = f'select name_naprav FROM napravlenie where id = {element[2]}'
            result = cur.execute(zapros).fetchall()
            stroka.append(result[0][0])
            zapros = f'select name_naprav FROM napravlenie where id = {element[3]}'
            result = cur.execute(zapros).fetchall()
            stroka.append(result[0][0])
            zapros = f'select name_naprav FROM napravlenie where id = {element[4]}'
            result = cur.execute(zapros).fetchall()
            stroka.append(result[0][0])
        else:
            prior = 'не выбрано'
            stroka.append(prior)
            stroka.append(prior)
            stroka.append(prior)


        zapros  = f'SELECT алгебра FROM mark WHERE id = {element[5]}'
        stroka.append(mark_cur.execute(zapros).fetchall()[0][0])
        zapros  = f'SELECT геометрия FROM mark WHERE id = {element[5]}'
        stroka.append(mark_cur.execute(zapros).fetchall()[0][0])
        zapros  = f'SELECT русский FROM mark WHERE id = {element[5]}'
        stroka.append(mark_cur.execute(zapros).fetchall()[0][0])
        zapros  = f'SELECT физика FROM mark WHERE id = {element[5]}'
        stroka.append(mark_cur.execute(zapros).fetchall()[0][0])
        zapros  = f'SELECT информатика FROM mark WHERE id = {element[5]}'
        stroka.append(mark_cur.execute(zapros).fetchall()[0][0])
        zapros  = f'SELECT химия FROM mark WHERE id = {element[5]}'
        stroka.append(mark_cur.execute(zapros).fetchall()[0][0])
        zapros  = f'SELECT иностранный FROM mark WHERE id = {element[5]}'
        stroka.append(mark_cur.execute(zapros).fetchall()[0][0])
        zapros  = f'SELECT биология FROM mark WHERE id = {element[5]}'
        stroka.append(mark_cur.execute(zapros).fetchall()[0][0])





        comment = 'physics_comment, informatic_comment, biology_comment, draftsmanship_comment, russian_comment, maths_comment, chemistry,foreign_lang, obsh_comment'
        zapros = f'SELECT {comment} FROM teacher_notes WHERE fio = \'{element[0]}\''
        spisok_com = cur.execute(zapros).fetchall()
        com = str()
        for element_com in spisok_com:
            com += f'информатика: {element_com[1]};\n'
            com += f'математика: {element_com[5]};\n'
            com += f'физика: {element_com[0]};\n'
            com += f'химия: {element_com[6]};\n'
            com += f'биология: {element_com[2]};\n'
            com += f'русский язык: {element_com[4]};\n'
            com += f'иностранный язык: {element_com[7]};\n'
            com += f'обществознание: {element_com[8]};\n'
            com += f'черчение: {element_com[3]};\n'
        stroka.append(com)



        print(stroka)
        ws.append(stroka)
    wb.save("static/viborka.xlsx")


#sozdanie()
