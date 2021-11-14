import sqlite3
import os

put = 'baza_for_sait.db'

def pois_uch(email_teacher):
    global put
    con = sqlite3.connect(put)
    cur = con.cursor()
    #так как будет находить по email педагогу нужно сделать следующее везде fio_teacher заменить!!!!!
    #Ветка, которая проверяет ведет ли учитель в данном классе
    id_teacher = f'SELECT id FROM teachers WHERE  почта = \'{email_teacher}\''
    name_predmet = f'SELECT name_predmeti FROM stud_predmeti WHERE id = \
                    (SELECT stud_predmet FROM teachers WHERE почта = \'{email_teacher}\')'
    result = cur.execute(name_predmet).fetchall()
    id_class = f'SELECT id FROM klass_bukva WHERE {result[0][0]} = ({id_teacher})'

    #Ветка которая проверяет по выбранности направления ученика
    id_predmet = f'SELECT stud_predmet FROM teachers WHERE почта = \'{email_teacher}\''
    id_napravlenie = f'SELECT id FROM napravlenie WHERE (predmet_1 = ({id_predmet}) or predmet_2 = ({id_predmet}))'

    #собираем всё
    ucheniki = f'SELECT ФИО, id FROM students WHERE ( klass IN ({id_class}) and \
                (prioritet_one = ({id_napravlenie}) or prioritet_two = ({id_napravlenie}) \
                or prioritet_tree = ({id_napravlenie})))'
    result = cur.execute(ucheniki).fetchall()
    return result


def uch_info(name):
    global put
    info = []
    con = sqlite3.connect(put)
    cur = con.cursor()
    grade = f'SELECT klass FROM students WHERE ФИО = \'{name}\''
    grade_rez = cur.execute(grade).fetchall()
    grade_letter = cur.execute(f'''SELECT klass_name FROM klass_bukva WHERE id = \'{grade_rez[0][0]}\'''').fetchall()
    info.append(grade_letter[0][0])
    comments = f'''SELECT physics_comment, informatic_comment,
	               biology_comment,
	               draftsmanship_comment,
	               russian_comment,
	               maths_comment,
	               chemistry,
	               foreign_lang, obsh_comment FROM teacher_notes WHERE fio = \'{name}\''''
    comments_rez = cur.execute(comments).fetchall()
    info.append(comments_rez[0])
    prof = f'''SELECT prioritet_one, prioritet_two, prioritet_tree FROM students WHERE ФИО = \'{name}\''''
    prof_rez = cur.execute(prof).fetchall()
    prof_tmp = []
    for i in prof_rez[0]:
        if i == 1:
            prof_tmp.append('Физико-математическое направление')
        elif i == 2:
            prof_tmp.append('Направление с углубленным изучением иностранного языка')
        elif i == 5:
            prof_tmp.append('Инженерное направление')
        elif i == 4:
            prof_tmp.append('Информационно-технологическое направление')
        elif i == 3:
            prof_tmp.append('Естественнонаучное направление: химико-биологическое')
        elif i == 6:
            prof_tmp.append('Экономико-математическое направление')
        elif i == 7:
            prof_tmp.append('Универсальное направление')
        elif i == 8:
            prof_tmp.append('Естественнонаучное направление: физико-химическое')
    profiles = []
    for i in prof_tmp:
        profiles.append(i)
    info.append(profiles)

    return info
