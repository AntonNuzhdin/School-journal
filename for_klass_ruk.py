import sqlite3
from datetime import *
import os



put = 'baza_for_sait.db'

def nuli():
    global put
    con = sqlite3.connect(put)
    cur = con.cursor()

    result = cur.execute(f'''UPDATE klass_ruk SET дистанционно=0''')
    con.commit()

def klass_ruk(terr):
    global put
    con = sqlite3.connect(put)
    cur = con.cursor()
    result = cur.execute(f'''SELECT класс FROM class_terr WHERE (территория = \'{terr}\')''').fetchall()
    klass = list()
    for elem in result:
        if 'МШФ' != elem[0] and 'Другое' != elem[0]:
            klass.append(elem[0])
    return(klass)

def prov(is_sait):
    if is_sait:
        return is_sait
    else:
        return 0

def opred_kinder(ur_class, reshenie, ORVI, grip, dr_zab,
                tr_v_school, tr_vne_school, neizvest, dist):
    global put
    con = sqlite3.connect(put)
    cur = con.cursor()
    znach = f'''\'{ur_class}\', {reshenie}, {ORVI}, {grip}, {dr_zab},
                    {tr_v_school}, {tr_vne_school}, {neizvest}, {dist}'''
    zapros = f'''INSERT INTO klass_ruk (класс, решение_род, ОРВИ, грипп,
                 другое_заболевание, травма_в_школе, травма_вне_школы,
                 причина_неизвестна, дистанционно) VALUES ({znach})'''
    result = cur.execute(zapros)
    con.commit()
    zapros = f'''SELECT почта FROM boss_klass WHERE (класс = \'{ur_class}\')'''
    result = cur.execute(zapros).fetchall()
    con.close()
    text = f'''<h1 style="text-align: center;"><img
                src="http://1502энергия.рф/static/imgs/LOGO_HOME.png"
                width="300" height="374" alt="" /></h1>
                <h1 style="text-align: center;"><strong>Добрый день!
                </strong></h1>
                <p><strong></strong></p>
                <p><strong></strong></p>
                <h2 style="text-align: center;"><strong> Ваш отчёт по классу
                </strong> <span style="color: #ff0000;"> <strong> {ur_class}
                </strong></span> <strong> получен и уже учтен в общей таблице
                 вашего корпуса. </strong></h2>
                '''

    return result[0][0], text


def otchet_admin_klass(terr, today=str(date.today())):
    global put
    con = sqlite3.connect(put)
    cur = con.cursor()
    #today = str(date.today())#[:9] + '1'
    #print(today)
    zapros = f'''SELECT класс FROM class_terr WHERE (территория = \'{terr}\')'''
    result = cur.execute(zapros).fetchall()
    klass = list()
    for elem in result:
        if 'МШФ' != elem[0] and 'Другое' != elem[0]:
            klass.append(elem[0])
    #print(klass)
    result = cur.execute(f'SELECT класс FROM klass_ruk WHERE дата_время like \'{today}%\'').fetchall()
    klass_est = list() #те классы которые прислали отчет
    for element in result:
        klass_est.append(element[0])
    ost_klass = list() #оставшееся классы которые не прислали отчет
    for element in klass:
        if element not in klass_est:
            ost_klass.append(element)
    result = cur.execute(f'SELECT id, дата_время, класс FROM klass_ruk WHERE дата_время like \'{today}%\' AND класс IN ({zapros})').fetchall()
    copy_result = result.copy()
    for i in range(len(copy_result)):
        for j in range(len(copy_result)):
            if copy_result[i][2] == copy_result[j][2]:
                if copy_result[i][1] < copy_result[j][1]:
                    result.remove(copy_result[i])
                    break
    otpr_klass_id = list()
    #print(result)
    for kl in klass:
        for element in result:
            if kl == element[2]:
                otpr_klass_id.append(element[0])
                break
    return ost_klass, otpr_klass_id




def otpr_info(list_id):
    global put
    con = sqlite3.connect(put)
    cur = con.cursor()
    lis = []
    for i in list_id:
        result = cur.execute(f'SELECT класс, решение_род, ОРВИ, грипп, другое_заболевание, травма_в_школе, травма_вне_школы, причина_неизвестна, дистанционно FROM klass_ruk WHERE id = {i}').fetchall()
        for j in result:
            j = list(j)
            j.append(sum(j[1:9]))
            result = cur.execute(f'SELECT численность FROM class_terr WHERE класс = (SELECT класс FROM klass_ruk WHERE id = {i})').fetchall()
            j.append(int(result[0][0]))
            j.append(j[-1] - j[-2])
            try:

                j.append(str(round((j[-3]/j[-2])*100, 2)) +'%')
            except ZeroDivisionError:
                j.append('0%')

            lis.append(j)
    return lis
# print(otpr_info([34,1,2,6]))
#выдает такой массив
#['1 А', 0, 10, 0, 3, 0, 0, 0, 7, 20, 29, 9, '68.97%'] что здесь что
#['класс', решение родителей, ОРВИ, грипп, Другое заболевание, Травма в школе, Травма вне школы, Причина неизвестна, Дистанционные, Всего отсутствует, Численность класса, кол-во присут, процент отсутствия]












def itog(otrp_info):
    all = []
    resh = 0
    orvi = 0
    grip = 0
    other = 0
    travma_v_sh = 0
    travma_vne_sh = 0
    prichina_neiz = 0
    dist = 0
    kol_otst = 0
    kol_obsh = 0
    kol_prisut = 0
    for i in otrp_info:
        resh += i[1]
        orvi += i[2]
        grip += i[3]
        other += i[4]
        travma_v_sh += i[5]
        travma_vne_sh += i[6]
        prichina_neiz += i[7]
        dist += i[8]
        kol_otst += i[9]
        kol_obsh += i[10]
        kol_prisut += i[11]

    all.append(resh)
    all.append(orvi)
    all.append(grip)
    all.append(other)
    all.append(travma_v_sh)
    all.append(travma_vne_sh)
    all.append(prichina_neiz)
    all.append(dist)
    all.append(kol_otst)
    all.append(kol_obsh)
    all.append(kol_prisut)
    try:

        all.append(str(round((all[-3]/all[-2])*100, 2)) +'%')
    except ZeroDivisionError:
        all.append('0%')

    return all


#def otchet_klass_ru():



# ost_klass, otpr_klass_id = otchet_admin_klass('Улица Девятая Рота, дом 14 А', today=str(date.today()))
# print(otpr_klass_id, '\n')
# a = otpr_info(otpr_klass_id)
# print(a, '\n')
# print(itog(a), '\n')
