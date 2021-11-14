import sqlite3
from datetime import *
import os
import json



put = 'baza_for_sait.db'
put_json = '/help_json/'
put_json_stud = 'static/'
put_mark = 'vse_mark.db'







def zapis(cur, con, tabl, summa, today, ter): #вспомогательная функция для vnesenie_kol_otst
        zapros = f'''SELECT дата FROM {tabl} WHERE дата = \'{today}\''''
        result = cur.execute(zapros).fetchall()
        zapros_id = f'''SELECT id FROM {tabl} WHERE дата = \'{today}\''''
        if result:
            cur.execute(f'''UPDATE {tabl} SET \'{ter}\' = {summa} WHERE id = ({zapros_id})''')
        else:
            cur.execute(f'''INSERT INTO {tabl}(дата, \'{ter}\') VALUES(\'{today}\', {summa})''')


def vnesenie_kol_otst():     #вставить при переходе на страницу выбора территории и даты сделать сохранение словаря в json
    global put
    con = sqlite3.connect(put)
    cur = con.cursor()
    today = str(date.today())#[:9] + '7'
    statistic = dict()
    adress = ['Улица Молостовых, дом 10А',
            'Улица Девятая Рота, дом 14 А',
            '2-я улица Бухвостова, дом 6',
            'Саянская улица, дом 3А',
            'Шоссе Энтузиастов, дом 96Г',
            'Шоссе Энтузиастов, дом 94А',
            'Шоссе Энтузиастов, дом 94Б',
            'Шоссе Энтузиастов, дом 96А',
            'Шоссе Энтузиастов, дом 96Б']
    obsch_summa_resh = 0
    obsch_summa_ORVI = 0
    obsch_summa_grip = 0
    obsch_summa_dr_zab = 0
    obsch_summa_tr_v_school = 0
    obsch_summa_tr_vne_school = 0
    obsch_summa_pr_ne_izv = 0
    obsch_summa_dist = 0
    obsch_summa_itog = 0
    obsch_summa_kol_stud = 0
    for ter in adress:
        zapros = f'''SELECT класс FROM class_terr WHERE (территория = \'{ter}\')'''
        result = cur.execute(zapros).fetchall()
        klass = list()
        for elem in result:
            if 'МШФ' != elem[0] and 'Другое' != elem[0]:
                klass.append(elem[0])
        result = cur.execute(f'SELECT * FROM klass_ruk WHERE дата_время like \'{today}%\' AND класс IN ({zapros})').fetchall()
        copy_result = result.copy()
        for i in range(len(copy_result)):
            for j in range(len(copy_result)):
                if copy_result[i][2] == copy_result[j][2]:
                    if copy_result[i][1] < copy_result[j][1]:

                        result.remove(copy_result[i])
                        break
        prov = list()
        for kl in klass:
            for element in result:
                if kl == element[2]:
                    prov.append(element)
                    break

        result = cur.execute(f'SELECT численность FROM class_terr WHERE класс IN (SELECT класс FROM class_terr WHERE (территория = \'{ter}\'))').fetchall()
        summa_kol_stud = 0
        for element in result:
            summa_kol_stud += int(element[0])
        summa_resh = 0
        summa_ORVI = 0
        summa_grip = 0
        summa_dr_zab = 0
        summa_tr_v_school = 0
        summa_tr_vne_school = 0
        summa_pr_ne_izv = 0
        summa_dist = 0
        summa_itog = 0
        statistik_ter = dict()
        for klass in prov:
            summa_resh += klass[3]
            summa_ORVI += klass[4]
            summa_grip += klass[5]
            summa_dr_zab += klass[6]
            summa_tr_v_school += klass[7]
            summa_tr_vne_school += klass[8]
            summa_pr_ne_izv += klass[9]
            summa_dist += klass[10]
        summa_itog += (summa_resh + summa_ORVI + summa_grip + summa_dr_zab +
                    summa_tr_v_school + summa_tr_vne_school + summa_pr_ne_izv +
                    summa_dist)
        obsch_summa_resh += summa_resh
        obsch_summa_ORVI += summa_ORVI
        obsch_summa_grip += summa_grip
        obsch_summa_dr_zab += summa_dr_zab
        obsch_summa_tr_v_school += summa_tr_v_school
        obsch_summa_tr_vne_school += summa_tr_vne_school
        obsch_summa_pr_ne_izv += summa_pr_ne_izv
        obsch_summa_dist += summa_dist
        obsch_summa_itog += summa_itog
        obsch_summa_kol_stud += summa_kol_stud
        statistik_ter['решение родителей'] = summa_resh
        statistik_ter['ОРВИ'] = summa_ORVI
        statistik_ter['грипп'] = summa_grip
        statistik_ter['другое заболевание'] = summa_dr_zab
        statistik_ter['травма в школе'] = summa_tr_v_school
        statistik_ter['травма вне школы'] = summa_tr_vne_school
        statistik_ter['причина неизвестна'] = summa_pr_ne_izv
        statistik_ter['дистанционно'] = summa_dist
        statistik_ter['итог по зданию'] = summa_itog
        statistik_ter['всего учеников'] = summa_kol_stud
        statistik_ter['присутствующие'] = statistik_ter['всего учеников'] - statistik_ter['итог по зданию']
        statistik_ter['процент отсутствия'] = str(round(statistik_ter['итог по зданию']/statistik_ter['всего учеников'] * 100, 2)) + '%'
        statistic[ter] = statistik_ter

        zapis(cur, con, 'statistik_resh', summa_resh, today, ter)
        zapis(cur, con, 'statistik_ORVI', summa_ORVI, today, ter)
        zapis(cur, con, 'statistik_grip', summa_grip, today, ter)
        zapis(cur, con, 'statistik_dr_zab', summa_dr_zab, today, ter)
        zapis(cur, con, 'statistik_tr_v_school', summa_tr_v_school, today, ter)
        zapis(cur, con, 'statistik_tr_vne_school', summa_tr_vne_school, today, ter)
        zapis(cur, con, 'statistik_pr_ne_izv', summa_pr_ne_izv, today, ter)
        zapis(cur, con, 'statistik_dist', summa_dist, today, ter)
        zapis(cur, con, 'statistik_itog', summa_itog, today, ter)
    statistik_ter = dict()
    statistik_ter['решение родителей'] = obsch_summa_resh
    zapis(cur, con, 'statistik_resh', obsch_summa_resh, today, 'все')
    statistik_ter['ОРВИ'] = obsch_summa_ORVI
    zapis(cur, con, 'statistik_ORVI', obsch_summa_ORVI, today, 'все')
    statistik_ter['грипп'] = obsch_summa_grip
    zapis(cur, con, 'statistik_grip', obsch_summa_grip, today, 'все')
    statistik_ter['другое заболевание'] = obsch_summa_dr_zab
    zapis(cur, con, 'statistik_dr_zab', obsch_summa_dr_zab, today, 'все')
    statistik_ter['травма в школе'] = obsch_summa_tr_v_school
    zapis(cur, con, 'statistik_tr_v_school', obsch_summa_tr_v_school, today, 'все')
    statistik_ter['травма вне школы'] = obsch_summa_tr_vne_school
    zapis(cur, con, 'statistik_tr_vne_school', obsch_summa_tr_vne_school, today, 'все')
    statistik_ter['причина неизвестна'] = obsch_summa_pr_ne_izv
    zapis(cur, con, 'statistik_pr_ne_izv', obsch_summa_pr_ne_izv, today, 'все')
    statistik_ter['дистанционно'] = obsch_summa_dist
    zapis(cur, con, 'statistik_dist', obsch_summa_dist, today, 'все')
    statistik_ter['итог по зданию'] = obsch_summa_itog
    zapis(cur, con, 'statistik_itog', obsch_summa_itog, today, 'все')
    statistik_ter['всего учеников'] = obsch_summa_kol_stud
    statistik_ter['присутствующие'] = obsch_summa_kol_stud - obsch_summa_itog
    statistik_ter['процент отсутствия'] = str(round(statistik_ter['итог по зданию']/statistik_ter['всего учеников'] * 100, 2)) + '%'





    statistic['все'] = statistik_ter
    con.commit()
    con.close()
    return statistic

def help_vivod_grafik(cur, con, ter, tabl):
    zapros = f'''SELECT дата, {ter} FROM {tabl}'''
    result = cur.execute(zapros).fetchall()
    return  result

def vivod_grafik(ter):
    global put
    global put_json
    con = sqlite3.connect(put)
    cur = con.cursor()
    grafik = dict()
    grafik['решение родителей'] = help_vivod_grafik(cur, con, ter, 'statistik_resh')
    grafik['ОРВИ'] = help_vivod_grafik(cur, con, ter, 'statistik_ORVI')
    grafik['грипп'] = help_vivod_grafik(cur, con, ter, 'statistik_grip')
    grafik['другое заболевание'] = help_vivod_grafik(cur, con, ter, 'statistik_dr_zab')
    grafik['травма в школе'] = help_vivod_grafik(cur, con, ter, 'statistik_tr_v_school')
    grafik['травма вне школы'] = help_vivod_grafik(cur, con, ter, 'statistik_tr_vne_school')
    grafik['причина неизвестна'] = help_vivod_grafik(cur, con, ter, 'statistik_pr_ne_izv')
    grafik['дистанционно'] = help_vivod_grafik(cur, con, ter, 'statistik_dist')
    grafik['итог по зданию'] = help_vivod_grafik(cur, con, ter, 'statistik_itog')

    with open(f'{put_json}{ter}_for_grafik.json', 'w', encoding = 'UTF-8') as file:
        json.dump(grafik, file, ensure_ascii = False)
    return(grafik)



def ryzanceva(): #формирует файл json для гуревича страницы фильтр по приоритетам
    global put
    global put_mark

    con = sqlite3.connect(put)
    cur = con.cursor()

    mark_con = sqlite3.connect(put_mark)
    mark_cur = mark_con.cursor()

    for_json = list()
    zapros = 'SELECT id, ФИО, klass, prioritet_one, prioritet_two, prioritet_tree FROM students'
    result = cur.execute(zapros).fetchall()
    i = 1
    for element in result:

        student = dict()
        student['ФИО'] = element[1]

        zapros = f'SELECT klass_name FROM klass_bukva WHERE id = {element[2]}'
        klass = cur.execute(zapros).fetchall()
        student['класс'] = klass[0][0]

        zapros = f'SELECT korpus FROM klass_bukva WHERE id = {element[2]}'
        zapros_2 = f'SELECT name_korpus FROM territory WHERE id = ({zapros})'
        territory = cur.execute(zapros_2).fetchall()
        student['территория'] = territory[0][0]


        if element[3]:
            zapros = f'SELECT name_naprav FROM napravlenie WHERE id = {element[3]}'
            naprav = cur.execute(zapros).fetchall()
            student['приоритет1'] = naprav[0][0]
        else:
            student['приоритет1'] = 'не выбран'

        if element[4]:
            zapros = f'SELECT name_naprav FROM napravlenie WHERE id = {element[4]}'
            naprav = cur.execute(zapros).fetchall()
            student['приоритет2'] = naprav[0][0]
        else:
            student['приоритет2'] = 'не выбран'

        if element[5]:
            zapros = f'SELECT name_naprav FROM napravlenie WHERE id = {element[5]}'
            naprav = cur.execute(zapros).fetchall()
            student['приоритет3'] = naprav[0][0]
        else:
            student['приоритет3'] = 'не выбран'


        comment = 'physics_comment, informatic_comment, biology_comment, draftsmanship_comment, russian_comment, maths_comment, chemistry,foreign_lang, obsh_comment'
        zapros = f'SELECT {comment} FROM teacher_notes WHERE fio = \'{element[1]}\''
        spisok_com = cur.execute(zapros).fetchall()
        com = dict()
        for element_com in spisok_com:
            com['информатика'] = element_com[1]
            com['математика'] = element_com[5]
            com['физика'] = element_com[0]
            com['химия'] = element_com[6]
            com['биология'] = element_com[2]
            com['русский язык'] = element_com[4]
            com['иностранный язык'] = element_com[7]
            com['обществознание'] = element_com[8]
            com['черчение'] = element_com[3]
        student['рекомендации'] = com

        mark = dict()
        zapros  = f'SELECT алгебра FROM mark WHERE id = {element[0]}'
        mark['алгебра'] = mark_cur.execute(zapros).fetchall()[0][0]
        zapros  = f'SELECT геометрия FROM mark WHERE id = {element[0]}'
        mark['геометрия'] = mark_cur.execute(zapros).fetchall()[0][0]
        zapros  = f'SELECT русский FROM mark WHERE id = {element[0]}'
        mark['русский'] = mark_cur.execute(zapros).fetchall()[0][0]
        zapros  = f'SELECT физика FROM mark WHERE id = {element[0]}'
        mark['физика'] = mark_cur.execute(zapros).fetchall()[0][0]
        zapros  = f'SELECT информатика FROM mark WHERE id = {element[0]}'
        mark['информатика'] = mark_cur.execute(zapros).fetchall()[0][0]
        zapros  = f'SELECT иностранный FROM mark WHERE id = {element[0]}'
        mark['иностранный'] = mark_cur.execute(zapros).fetchall()[0][0]
        zapros  = f'SELECT биология FROM mark WHERE id = {element[0]}'
        mark['биология'] = mark_cur.execute(zapros).fetchall()[0][0]
        zapros  = f'SELECT химия FROM mark WHERE id = {element[0]}'
        mark['химия'] = mark_cur.execute(zapros).fetchall()[0][0]
        student['оценки'] = mark

        for_json.append(student)
    with open(f'{put_json_stud}otchet_students.json', 'w', encoding = 'UTF-8') as file:
        json.dump(for_json, file, ensure_ascii = False)


# def statistica():
#     global put_mark
#     mark_con = sqlite3.connect(put_mark)
#     mark_cur = mark_con.cursor()
#     zapros = 'SELECT id, алгебра FROM mark WHERE алгебра IN (9, 10)'
#     result = cur.execute(zapros).fetchall()
#     for i in result:
#         print(i)
