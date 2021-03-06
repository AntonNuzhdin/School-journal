#12

from flask import Flask, render_template, request, redirect, url_for, session, make_response
from flask import session
from data_mail import *
from jinja2 import *
from mail_otpr import *
from pois_uchenika_gotov import *
import os
from proverka_adminov import *
from authorisation import *
from for_klass_ruk import *
from datetime import *
from for_grafik import *
from sozdanie_excel import *
from metodist import *
from PPV_11_CLASS import *


app = Flask(__name__)

@app.route('/user/<username>/<int:value>')
def show_user_profile(username, value):
    # показать профиль данного пользователя
    db = sqlite3.connect("baza_for_sait.db")
    cursor = db.cursor()
    #test = cursor.execute("Select присутствие From student_11 Where фио='"+username+"' ")
    if(value==1):
        print('yes')
        cursor = db.cursor()
        test = cursor.execute("Update student_11 Set присутствие='Да' Where фио='" + username + "' ")
    else:
        print('No')
        cursor = db.cursor()
        test = cursor.execute("Update student_11 Set присутствие='Нет' Where фио='" + username + "' ")
    db.commit()
    return 'User %s' % username


@app.route('/', methods=['GET','POST'])
def index():
    session['flag_stu'] = 0
    session['flag_adm'] = 0
    session['flag_ryaz'] = 0
    session['flag_helper'] = 0
    session['flagPpv'] = 0
    session['flagClassBoss'] = 0

    try:
        if request.method == "GET": #если метод GET - просто показывает домашнюю страницу
            return render_template('home.html') #домешняя страница
        else:
            session['login'] = request.form['login']
            bossOrTeacher = isClassBossOrTeacher(request.form['login'], request.form['pw'])
            if bossOrTeacher[1] == 1 and bossOrTeacher[0] == 0:
                session['teacher'] = teacherName(session['login'])
                return render_template('teacher.html', studentsList = studentsInfoForTeachers(request.form['login']), teacher = session['teacher'][0][0])
            elif bossOrTeacher[1] == 0 and bossOrTeacher[0] == 1:
                session['teacher'] = classBossName(session['login'])
                return render_template('klass_ruk.html', studentsList = nach_uchenika(request.form['login']), teacher=session['teacher'][0][0])
            elif bossOrTeacher[1] == 1 and bossOrTeacher[0] == 1:
                session['teacher'] = classBossName(session['login'])
                return redirect(url_for('teacherOrBoss'))


            session['login'] = request.form['login']

            res_log, res_pas, data_student = check_log_pas(request.form['login'], request.form['pw'])
            res_log_teach, res_pas_teach, data_teacher = check_teacher(request.form['login'], request.form['pw'])

            session['admin_prov'] = admin_proverka(request.form['login'])
            if session['admin_prov'][0] and session['admin_prov'][1]:

                if wdb_check('admin',request.form['login'], request.form['pw']):
                    session['flag_adm'] = 1
                    session['teacher'] = data_teacher[1]

                    return redirect(url_for('adm_teach'))


            elif session['admin_prov'][0]:

                if wdb_check('admin', request.form['login'], request.form['pw']):
                    session['flag_adm'] = 1

                    return redirect(url_for('adm'))
            elif session['admin_prov'][2]:
                if wdb_check('help_admin', request.form['login'], request.form['pw']):
                    session['flag_adm'] = 1
                    return redirect(url_for('adm_help'))


            session['login'] = request.form['login']
            if res_log and res_pas: #проверям что логин совпадает с паролем
                session['flag_stu'] = 1
                session['stu_ter'] = opred_ter(request.form['login'])
                session['nickname'] = data_student[1] #выдергиваем имя пользователя чтобы отображалось на страничке
                #если ничего нет в предметах, то мы выдаем профили предметов, если есть что-то, то в личный кабинет
                if not (bool(data_student[4]) and bool(data_student[5] and bool(data_student[6]))):
                    return redirect(url_for('welcome'))
                else:
                    # сохраняем в сессичные переменные данные из бызы
                    session['naprav_1'] = data_student[4]
                    session['naprav_2'] = data_student[5]
                    session['naprav_3'] = data_student[6]
                    if session['naprav_1'] == 1:
                        session['naprav_1'] = "Физико-математическое направление"
                    elif session['naprav_1'] == 2:
                        session['naprav_1'] = "Направление с углубленным изучением иностранного языка"
                    elif session['naprav_1'] == 3:
                        session['naprav_1'] = "Естественнонаучное направление: химико-биологическое"
                    elif session['naprav_1'] == 4:
                        session['naprav_1'] = "Информационно-технологическое направление"
                    elif session['naprav_1'] == 5:
                        session['naprav_1'] = "Инженерное направление"
                    elif session['naprav_1'] == 6:
                        session['naprav_1'] = "Экономико-математическое направление"
                    elif session['naprav_1'] == 7:
                        session['naprav_1'] = "Универсальное направление"
                    elif session['naprav_1'] == 8:
                        session['naprav_1'] = "Естественнонаучное направление: физико-химическое"


                    if session['naprav_2'] == 1:
                        session['naprav_2'] = "Физико-математическое направление"
                    elif session['naprav_2'] == 2:
                        session['naprav_2'] = "Направление с углубленным изучением иностранного языка"
                    elif session['naprav_2'] == 3:
                        session['naprav_2'] = "Естественнонаучное направление: химико-биологическое"
                    elif session['naprav_2'] == 4:
                        session['naprav_2'] = "Информационно-технологическое направление"
                    elif session['naprav_2'] == 5:
                        session['naprav_2'] = "Инженерное направление"
                    elif session['naprav_2'] == 6:
                        session['naprav_2'] = "Экономико-математическое направление"
                    elif session['naprav_2'] == 7:
                        session['naprav_2'] = "Универсальное направление"
                    elif session['naprav_2'] == 8:
                        session['naprav_2'] = "Естественнонаучное направление: физико-химическое"


                    if session['naprav_3'] == 1:
                        session['naprav_3'] = "Физико-математическое направление"
                    elif session['naprav_3'] == 2:
                        session['naprav_3'] = "Направление с углубленным изучением иностранного языка"
                    elif session['naprav_3'] == 3:
                        session['naprav_3'] = "Естественнонаучное направление: химико-биологическое"
                    elif session['naprav_3'] == 4:
                        session['naprav_3'] = "Информационно-технологическое направление"
                    elif session['naprav_3'] == 5:
                        session['naprav_3'] = "Инженерное направление"
                    elif session['naprav_3'] == 6:
                        session['naprav_3'] = "Экономико-математическое направление"
                    elif session['naprav_3'] == 7:
                        session['naprav_3'] = "Универсальное направление"
                    elif session['naprav_3'] == 8:
                        session['naprav_3'] = "Естественнонаучное направление: физико-химическое"

                    session['marks'] = marks(session['login'])[0]

                    session['olimp_inf'] = marks(session['login'])[1]['информатика']
                    session['olimp_bio'] = marks(session['login'])[1]['биология']
                    session['olimp_him'] = marks(session['login'])[1]['химия']
                    if type(session['olimp_inf']) != int:
                        session['olimp_inf'] = 'null'
                        print('YES')
                    if type(session['olimp_bio']) != int:
                        session['olimp_bio'] = 'null'
                        print('YES')

                    if type(session['olimp_him']) != int:
                        session['olimp_him'] = 'null'
                        print('YES')

                    session['him'] = var_him(session['login'])
                    try:
                        session['admiss'] = 1
                        session['admission'] = to_class(session['login'])
                    except IndexError:
                        session['admiss'] = 0
                    return redirect(url_for('personal_page'))

            elif res_log_teach and res_pas_teach:
                session['flag_adm'] = 1

                session['teacher'] = data_teacher[1]
                session['all_students'] = pois_uch(session['login'])
                session['predmet_teach'] = pois_predmeta(session['login'])
                if session['login'] == 'blinkov-ea@1502.moscow' or session['login'] == 'pavluk-op@1502.moscow' or session['login'] == 'shabalin-vg@1502.moscow':
                    poisk()
                    return redirect(url_for('adm_teacher'))
                return redirect(url_for('teacher_choice_form'))
            else:
                return render_template('home.html', incorrect='Неверный логин или пароль') #если неверные - обратно домашнюю
    except KeyError:
        return render_template('home.html')

@app.route('/teacherOrBoss', methods=['GET', 'POST'])
def teacherOrBoss():
    return render_template('teacherOrBoss.html')

@app.route('/teacher', methods=['GET', 'POST'])
def teacher():
    return render_template('teacher.html', studentsList = studentsInfoForTeachers(session['login']), teacher = session['teacher'][0][0])

@app.route('/classBoss', methods=['GET', 'POST'])
def classBoss():
    return render_template('klass_ruk.html', studentsList = nach_uchenika(session['login']), teacher = session['teacher'][0][0])

# @app.route('/welcome', methods=['GET', 'POST'])
# def welcome():
#     try:
#         if session['flag_stu'] == 0:
#             return ">>>>>>>>"
#         else:
#             if session['stu_ter'] == 'Гамма':
#                 return render_template('welcome.html', stu_ter=session['stu_ter'], tmp=0)
#             else:
#                 return render_template('welcome.html', stu_ter=session['stu_ter'], tmp=1)
#
#     except KeyError:
#         return 'fghjkl'


@app.route('/personal_page', methods=['GET', 'POST'])
def personal_page():
    try:
        if session['flag_stu'] == 0:
            return ">>>>>>>>"
    except KeyError:
        return 'fghjkl'
    if request.method == 'POST':
        session['stepik_var'] = request.form['stepik_var']
        var_stepik(session['stepik_var'], session['login'])
        return redirect(url_for('personal_page'))
    else:
        try:
            zapis_v_bazu(session['naprav_1'], session['login'], 1)
            zapis_v_bazu(session['naprav_2'], session['login'], 2)
            zapis_v_bazu(session['naprav_3'], session['login'], 3)
            session['reg'] = vivod_prof(session['login'])
            if "информатика" in session['reg'] and "химия" in session['reg'] and "биология" in session['reg']:
                return render_template('personal_page.html',
                                       stu_ter=session['stu_ter'],
                                       nickname=session['nickname'],
                                       naprav_1=session['naprav_1'],
                                       naprav_2=session['naprav_2'],
                                        naprav_3=session['naprav_3'],
                                        inf=1, chem=1, bio=1,
                                        stu_marks=session['marks'],
                                        olimp_inf=session['olimp_inf'],
                                        olimp_him=session['olimp_him'],
                                        olimp_bio=session['olimp_bio'],
                                        him=session['him'],
                                        to_class=session['admission'],
                                        admiss = session['admiss'])

            elif "информатика" in session['reg'] and "химия" in session['reg']:
                return render_template('personal_page.html',
                                       stu_ter=session['stu_ter'],
                                        nickname=session['nickname'],
                                         naprav_1=session['naprav_1'],
                                         naprav_2=session['naprav_2'],
                                         naprav_3=session['naprav_3'],
                                         inf=1, chem=1,
                                         stu_marks=session['marks'],
                                         olimp_inf=session['olimp_inf'],
                                         olimp_him=session['olimp_him'],
                                         olimp_bio=session['olimp_bio'],
                                         him=session['him'],
                                         to_class=session['admission'],
                                         admiss = session['admiss'])

            elif "информатика" in session['reg'] and "биология" in session['reg']:
                return render_template('personal_page.html',
                                       stu_ter=session['stu_ter'],
                                       nickname=session['nickname'],
                                       naprav_1=session['naprav_1'],
                                       naprav_2=session['naprav_2'],
                                       naprav_3=session['naprav_3'],
                                       inf=1, bio=1,
                                       stu_marks=session['marks'],
                                       olimp_inf=session['olimp_inf'],
                                       olimp_him=session['olimp_him'],
                                       olimp_bio=session['olimp_bio'],
                                       to_class=session['admission'],
                                       admiss = session['admiss'])

            elif "химия" in session['reg'] and "биология" in session['reg']:
                return render_template('personal_page.html',
                                       stu_ter=session['stu_ter'],
                                       nickname=session['nickname'],
                                       naprav_1=session['naprav_1'],
                                       naprav_2=session['naprav_2'],
                                       naprav_3=session['naprav_3'],
                                       chem=1, bio=1,
                                       stu_marks=session['marks'],
                                       olimp_inf=session['olimp_inf'],
                                       olimp_him=session['olimp_him'],
                                       olimp_bio=session['olimp_bio'],
                                       him=session['him'],
                                       to_class=session['admission'],
                                       admiss = session['admiss'])

            elif "информатика" in session['reg']:
                return render_template('personal_page.html',
                                       stu_ter=session['stu_ter'],
                                       nickname=session['nickname'],
                                       naprav_1=session['naprav_1'],
                                       naprav_2=session['naprav_2'],
                                       naprav_3=session['naprav_3'],
                                       inf=1,
                                       stu_marks=session['marks'],
                                       olimp_inf=session['olimp_inf'],
                                       olimp_him=session['olimp_him'],
                                       olimp_bio=session['olimp_bio'],
                                       to_class=session['admission'],
                                       admiss = session['admiss'])

            elif "химия" in session['reg']:
                return render_template('personal_page.html', stu_ter=session['stu_ter'], nickname=session['nickname'], naprav_1=session['naprav_1'], naprav_2=session['naprav_2'], naprav_3=session['naprav_3'], chem=1, stu_marks=session['marks'],
                olimp_inf=session['olimp_inf'],
                olimp_him=session['olimp_him'],
                olimp_bio=session['olimp_bio'],
                him=session['him'],
                to_class=session['admission'],
                admiss = session['admiss'])
            elif "биология" in session['reg']:
                return render_template('personal_page.html', stu_ter=session['stu_ter'], nickname=session['nickname'], naprav_1=session['naprav_1'], naprav_2=session['naprav_2'], naprav_3=session['naprav_3'], bio=1, stu_marks=session['marks'],
                olimp_inf=session['olimp_inf'],
                olimp_him=session['olimp_him'],
                olimp_bio=session['olimp_bio'],
                to_class=session['admission'],
                admiss = session['admiss'])
            else:
                return render_template('personal_page.html', stu_ter=session['stu_ter'], nickname=session['nickname'], naprav_1=session['naprav_1'], naprav_2=session['naprav_2'], naprav_3=session['naprav_3'], stu_marks=session['marks'],
                olimp_inf=session['olimp_inf'],
                olimp_him=session['olimp_him'],
                olimp_bio=session['olimp_bio'],
                to_class=session['admission'],
                admiss = session['admiss'])

        except KeyError:
            return render_template('personal_page_error.html',stu_ter=session['stu_ter'], nickname=session['nickname'])

#
#
# @app.route('/choice', methods=['GET','POST'])#путь для второй страницы с формой
# def choice():
#     try:
#
#         if session['flag_stu'] == 0:
#             return ">>>>>>>>"
#         elif request.method == "GET" and session['stu_ter'] == 'Гамма':
#             return render_template('choice_gamma.html', stu_ter=session['stu_ter'], nickname=session['nickname'])
#         elif request.method == "GET" and session['stu_ter'] == 'Альфа':
#             return render_template('choice.html', stu_ter=session['stu_ter'], nickname=session['nickname'])
#         else:
#
#             session['naprav_1'] = request.form['pref'] # записываем первый приоритет в переменную
#             zapis_v_bazu(session['naprav_1'], session['login'], 1)
#             session['naprav_2'] = request.form['pref_2'] # второй приоритет
#             zapis_v_bazu(session['naprav_2'], session['login'], 2)
#             session['naprav_3'] = request.form['pref_3']# третий
#             zapis_v_bazu(session['naprav_3'], session['login'], 3)
#             text_otp = text_prof(session['naprav_1'], session['naprav_2'], session['naprav_3'], session['nickname'])
#             otpravka(session['login'], 'Направления классов', text_otp)
#
#             return render_template('thanks.html')
#     except KeyError:
#         return 'fghjkl'
#


@app.route('/adm_teach', methods=['GET', 'POST'])
def adm_teach():
    if session['flag_adm'] == 0:
        return "<<<<<<<"

    return redirect(url_for('adm_teacher'))


@app.route('/adm', methods=['GET', 'POST'])
def adm():
    if session['flag_adm'] == 0:
        return "<<<<<<<"
    if session['login'] == "ryazantseva-em@1502.moscow" or session['login'] == "britov-dr@1502.moscow" or session['login'] == 'chudov-vl@1502.moscow':
        session['flag_ryaz'] = 1
        sozdanie()
        ryzanceva()

        return render_template("adm_teacher.html", view=1)
    else:
        return redirect(url_for('table_before'))


@app.route('/adm_help', methods=['GET', 'POST'])
def adm_help():
    if session['flag_adm'] == 0:
        return "<<<<<<<"

    return redirect(url_for('adm_helper'))


@app.route('/adm_teacher', methods=['GET', 'POST'])
def adm_teacher():
    if session['flag_adm'] == 0:
        return "<<<<<<<"

    if session['login'] == "tumanov-nv@1502.moscow":
        session['flag_ryaz'] = 1

        poisk()

        ryzanceva()
        sozdanie()

        return render_template('adm_teacher.html', view=2)
    elif session['login'] == 'blinkov-ea@1502.moscow' or session['login'] == 'pavluk-op@1502.moscow' or session['login'] == 'shabalin-vg@1502.moscow':
        return render_template('adm_teacher.html', view=3)

    else:
        return render_template('adm_teacher.html')




@app.route('/adm_helper', methods=['GET', 'POST'])
def adm_helper():
    if session['flag_adm'] == 0:
        return "<<<<<<<"

    session['flag_helper'] = 1
    session['ter'] = admin_proverka(session['login'])[-1]

    return redirect(url_for('table'))

@app.route('/methdist', methods=['GET', 'POST'])
def methodist():
    if session['flag_adm'] == 0:
        return '<<<<<'
    else:
        return render_template('metodist.html')


@app.route('/prof_table', methods=['GET', 'POST'])
def prof_table():
    if session['flag_ryaz'] == 1:
        session['excel'] = 'https://xn--1502-o4dlw1b2a1k1a.xn--p1ai/static/viborka.xlsx'
        return render_template('a.html', file=session['excel'])
    else:
        return ">>>>>>"




@app.route('/teacher_choice_form', methods=['GET','POST'])#путь для второй страницы с формой
def teacher_choice_form():
    if session['flag_adm'] == 0:
        return '<<<<<<<'
    if request.method == "GET":
        session['all_students'] = pois_uch(session['login'])
        session['complex_info'] = []
        session['box'] = 0
        for i in session['all_students']:
            session['complex_info'].append(uch_info(i[0]))
        session['len_classes'] = len(session['all_students'])
        return render_template('teacher_choice_form.html', teacher = session['teacher'], classes = session['all_students'], len_classes=session['len_classes'],
                               complex=session['complex_info'], box=session['box'])
    else:
        for i in session['all_students']:
            try:
                session['predmet_teach'] = pois_predmeta(session['login'])

                session['stu'] = request.form[i[0]]
                session['test'] = request.form[i[0]+'ch']
                if session['test'] == '1':
                    session['test'] = "Рекомендую"
                if session['test'] == '2':
                    session['test'] = "Не рекомендую"
                if session['test'] == '3':
                    session['test'] = "Нейтрально"
                if len(session['stu']) > 2 and session['test'] != "Выберите один из вариантов":
                    zapis_comments(i[0], session['stu']+"("+session['test']+")", session['test'], session['predmet_teach'])
                elif len(session['stu']) > 2 and session['test'] == "Выберите один из вариантов":
                    zapis_comments(i[0], session['stu']+"(Нейтрально)", "Нейтрально", session['predmet_teach'])
                elif len(session['stu']) < 2 and session['test'] == "Выберите один из вариантов":
                    continue
                else:
                    zapis_comments(i[0], session['test'], session['test'], session['predmet_teach'])
            except KeyError:
                continue

        return render_template('thanks_teachers.html')



@app.route('/table_before', methods=['GET', 'POST'])
def table_before():
    if session['flag_adm'] == 0:
        return "<<<<<<<"
    else:
        if request.method == "GET" and session['flag_helper'] == 0:
            session['stat'] = vnesenie_kol_otst()

            return render_template('table_before.html', stat=session['stat'])
        else:
            return redirect(url_for('table'))


@app.route('/table', methods=['GET', 'POST'])
def table():
    if session['flag_adm'] == 0:
        return "<<<<<<"
    if request.method == "GET" and session['flag_helper'] == 0:
            session['stat'] = vnesenie_kol_otst()

            return render_template('table_before.html', stat=session['stat'])
    elif request.method == "GET" and session['flag_helper'] == 1:

        if session['flag_helper'] == 1:
            session['ne_otpr'] = otchet_admin_klass(session['ter'][0][0])[0]

            session['range_ne'] = len(session['ne_otpr'])
            session['otpr'] = otchet_admin_klass(session['ter'][0][0])[1]
        else:
            session['ne_otpr'] = otchet_admin_klass(session['ter'][0][0], session['calender'])[0]

            session['range_ne'] = len(session['ne_otpr'])
            session['otpr'] = otchet_admin_klass(session['ter'][0][0], session['calender'])[1]
        session['range_otpr'] = len(session['otpr'])
        session['otpr_info'] = otpr_info(session['otpr'])
        session['range3'] = len(session['otpr_info'])
        session['itog'] = itog(session['otpr_info'])

        return render_template('Table.html',  name=session['admin_prov'][3], terri=session['ter'][0][0], ne_otpr=session['ne_otpr'], range1=session['range_ne'], otpr_info=session['otpr_info'], range3=session['range3'], itog=session['itog'])

    elif request.method != "GET" and session['flag_helper'] == 1:
        return render_template('Table.html',  name=session['admin_prov'][3], terri=session['ter'], ne_otpr=session['ne_otpr'], range1=session['range_ne'], otpr_info=session['otpr_info'], range3=session['range3'], itog=session['itog'])

    elif request.method != "GET":
        session['terri'] = request.form['terri']
        if session['flag_helper'] == 1:
            session['ne_otpr'] = otchet_admin_klass(session['terri'])[0]
            session['otpr'] = otchet_admin_klass(session['terri'])[1]
        else:
            session['calender'] = request.form['date_cal']
            session['ne_otpr'] = otchet_admin_klass(session['terri'], session['calender'])[0]
            session['otpr'] = otchet_admin_klass(session['terri'], session['calender'])[1]
        session['range_ne'] = len(session['ne_otpr'])
        session['range_otpr'] = len(session['otpr'])
        session['otpr_info'] = otpr_info(session['otpr'])
        session['range3'] = len(session['otpr_info'])
        session['itog'] = itog(session['otpr_info'])



        session['itog'] = itog(session['otpr_info'])
        return render_template('Table.html',  name=session['admin_prov'][3], terri=session['terri'], ne_otpr=session['ne_otpr'], range1=session['range_ne'], otpr_info=session['otpr_info'], range3=session['range3'], itog=session['itog'])


@app.route('/class_ruk_alfa', methods = ['GET', 'POST'])
def for_klass_alfa():
    if request.method == 'GET':
        session['spisok_klass'] = klass_ruk('Улица Молостовых, дом 10А')
        return render_template('Missing_report.html', spisok_klass=session['spisok_klass'])
    else:
        session['ur_class'] = request.form['ur_class']
        session['reshenie'] = prov(request.form['reshenie'])
        session['ORVI'] = prov(request.form['ORVI'])
        session['grip'] = prov(request.form['grip'])
        session['dr_zab'] = prov(request.form['dr_zab'])
        session['tr_v_school'] = prov(request.form['tr_v_school'])
        session['tr_vne_school'] = prov(request.form['tr_vne_school'])
        session['neizvest'] = prov(request.form['neizvest'])
        session['dist'] = prov(request.form['dist'])
        session['e_mail_text'] = opred_kinder(ur_class = session['ur_class'],
                    reshenie = session['reshenie'],
                     ORVI = session['ORVI'], grip = session['grip'],
                     dr_zab = session['dr_zab'], tr_v_school = session['tr_v_school'],
                    tr_vne_school = session['tr_vne_school'], neizvest = session['neizvest'], dist=session['dist'])
        otpravka(session['e_mail_text'][0], 'Отчет по посещаемости', session['e_mail_text'][1])
        return render_template('thanks_teachers.html', clas=session['ur_class'])


@app.route('/class_ruk_beta', methods = ['GET', 'POST'])
def for_klass_beta():
    if request.method == 'GET':
        session['spisok_klass'] = klass_ruk('Улица Девятая Рота, дом 14 А')
        return render_template('Missing_report.html', spisok_klass=session['spisok_klass'])
    else:
        session['ur_class'] = request.form['ur_class']
        session['reshenie'] = prov(request.form['reshenie'])
        session['ORVI'] = prov(request.form['ORVI'])
        session['grip'] = prov(request.form['grip'])
        session['dr_zab'] = prov(request.form['dr_zab'])
        session['tr_v_school'] = prov(request.form['tr_v_school'])
        session['tr_vne_school'] = prov(request.form['tr_vne_school'])
        session['neizvest'] = prov(request.form['neizvest'])
        session['dist'] = prov(request.form['dist'])
        session['e_mail_text'] = opred_kinder(ur_class = session['ur_class'],
                    reshenie = session['reshenie'],
                     ORVI = session['ORVI'], grip = session['grip'],
                     dr_zab = session['dr_zab'], tr_v_school = session['tr_v_school'],
                    tr_vne_school = session['tr_vne_school'], neizvest = session['neizvest'], dist=session['dist'])
        otpravka(session['e_mail_text'][0], 'Отчет по посещаемости', session['e_mail_text'][1])
        return render_template('thanks_teachers.html', clas=session['ur_class'])


@app.route('/class_ruk_gamma', methods = ['GET', 'POST'])
def for_klass_gamma():
    if request.method == 'GET':
        session['spisok_klass'] = klass_ruk('2-я улица Бухвостова, дом 6')
        return render_template('Missing_report.html', spisok_klass=session['spisok_klass'])
    else:
        session['ur_class'] = request.form['ur_class']
        session['reshenie'] = prov(request.form['reshenie'])
        session['ORVI'] = prov(request.form['ORVI'])
        session['grip'] = prov(request.form['grip'])
        session['dr_zab'] = prov(request.form['dr_zab'])
        session['tr_v_school'] = prov(request.form['tr_v_school'])
        session['tr_vne_school'] = prov(request.form['tr_vne_school'])
        session['neizvest'] = prov(request.form['neizvest'])
        session['dist'] = prov(request.form['dist'])
        session['e_mail_text'] = opred_kinder(ur_class = session['ur_class'],
                    reshenie = session['reshenie'],
                     ORVI = session['ORVI'], grip = session['grip'],
                     dr_zab = session['dr_zab'], tr_v_school = session['tr_v_school'],
                    tr_vne_school = session['tr_vne_school'], neizvest = session['neizvest'], dist=session['dist'])
        otpravka(session['e_mail_text'][0], 'Отчет по посещаемости', session['e_mail_text'][1])
        return render_template('thanks_teachers.html', clas=session['ur_class'])


@app.route('/class_ruk_delta_1', methods = ['GET', 'POST'])
def for_klass_delta_1():
    if request.method == 'GET':
        session['spisok_klass'] = klass_ruk('Саянская улица, дом 3А')
        return render_template('Missing_report.html', spisok_klass=session['spisok_klass'])
    else:
        session['ur_class'] = request.form['ur_class']
        session['reshenie'] = prov(request.form['reshenie'])
        session['ORVI'] = prov(request.form['ORVI'])
        session['grip'] = prov(request.form['grip'])
        session['dr_zab'] = prov(request.form['dr_zab'])
        session['tr_v_school'] = prov(request.form['tr_v_school'])
        session['tr_vne_school'] = prov(request.form['tr_vne_school'])
        session['neizvest'] = prov(request.form['neizvest'])
        session['dist'] = prov(request.form['dist'])
        session['e_mail_text'] = opred_kinder(ur_class = session['ur_class'],
                    reshenie = session['reshenie'],
                     ORVI = session['ORVI'], grip = session['grip'],
                     dr_zab = session['dr_zab'], tr_v_school = session['tr_v_school'],
                    tr_vne_school = session['tr_vne_school'], neizvest = session['neizvest'], dist=session['dist'])
        otpravka(session['e_mail_text'][0], 'Отчет по посещаемости', session['e_mail_text'][1])
        return render_template('thanks_teachers.html', clas=session['ur_class'])


@app.route('/class_ruk_delta_2', methods = ['GET', 'POST'])
def for_klass_delta_2():
    if request.method == 'GET':
        session['spisok_klass'] = klass_ruk('Шоссе Энтузиастов, дом 96Г')
        return render_template('Missing_report.html', spisok_klass=session['spisok_klass'])
    else:
        session['ur_class'] = request.form['ur_class']
        session['reshenie'] = prov(request.form['reshenie'])
        session['ORVI'] = prov(request.form['ORVI'])
        session['grip'] = prov(request.form['grip'])
        session['dr_zab'] = prov(request.form['dr_zab'])
        session['tr_v_school'] = prov(request.form['tr_v_school'])
        session['tr_vne_school'] = prov(request.form['tr_vne_school'])
        session['neizvest'] = prov(request.form['neizvest'])
        session['dist'] = prov(request.form['dist'])
        session['e_mail_text'] = opred_kinder(ur_class = session['ur_class'],
                    reshenie = session['reshenie'],
                     ORVI = session['ORVI'], grip = session['grip'],
                     dr_zab = session['dr_zab'], tr_v_school = session['tr_v_school'],
                    tr_vne_school = session['tr_vne_school'], neizvest = session['neizvest'], dist=session['dist'])
        otpravka(session['e_mail_text'][0], 'Отчет по посещаемости', session['e_mail_text'][1])
        return render_template('thanks_teachers.html', clas=session['ur_class'])


@app.route('/class_ruk_delta_3', methods = ['GET', 'POST'])
def for_klass_delta_3():
    if request.method == 'GET':
        session['spisok_klass'] = klass_ruk('Шоссе Энтузиастов, дом 94А')
        return render_template('Missing_report.html', spisok_klass=session['spisok_klass'])
    else:
        session['ur_class'] = request.form['ur_class']
        session['reshenie'] = prov(request.form['reshenie'])
        session['ORVI'] = prov(request.form['ORVI'])
        session['grip'] = prov(request.form['grip'])
        session['dr_zab'] = prov(request.form['dr_zab'])
        session['tr_v_school'] = prov(request.form['tr_v_school'])
        session['tr_vne_school'] = prov(request.form['tr_vne_school'])
        session['neizvest'] = prov(request.form['neizvest'])
        session['dist'] = prov(request.form['dist'])
        session['e_mail_text'] = opred_kinder(ur_class = session['ur_class'],
                    reshenie = session['reshenie'],
                     ORVI = session['ORVI'], grip = session['grip'],
                     dr_zab = session['dr_zab'], tr_v_school = session['tr_v_school'],
                    tr_vne_school = session['tr_vne_school'], neizvest = session['neizvest'], dist=session['dist'])
        otpravka(session['e_mail_text'][0], 'Отчет по посещаемости', session['e_mail_text'][1])
        return render_template('thanks_teachers.html', clas=session['ur_class'])


@app.route('/class_ruk_delta_4', methods = ['GET', 'POST'])
def for_klass_delta_4():
    if request.method == 'GET':
        session['spisok_klass'] = klass_ruk('Шоссе Энтузиастов, дом 94Б')
        return render_template('Missing_report.html', spisok_klass=session['spisok_klass'])
    else:
        session['ur_class'] = request.form['ur_class']
        session['reshenie'] = prov(request.form['reshenie'])
        session['ORVI'] = prov(request.form['ORVI'])
        session['grip'] = prov(request.form['grip'])
        session['dr_zab'] = prov(request.form['dr_zab'])
        session['tr_v_school'] = prov(request.form['tr_v_school'])
        session['tr_vne_school'] = prov(request.form['tr_vne_school'])
        session['neizvest'] = prov(request.form['neizvest'])
        session['dist'] = prov(request.form['dist'])
        session['e_mail_text'] = opred_kinder(ur_class = session['ur_class'],
                    reshenie = session['reshenie'],
                     ORVI = session['ORVI'], grip = session['grip'],
                     dr_zab = session['dr_zab'], tr_v_school = session['tr_v_school'],
                    tr_vne_school = session['tr_vne_school'], neizvest = session['neizvest'], dist=session['dist'])
        otpravka(session['e_mail_text'][0], 'Отчет по посещаемости', session['e_mail_text'][1])
        return render_template('thanks_teachers.html', clas=session['ur_class'])


@app.route('/class_ruk_delta_5', methods = ['GET', 'POST'])
def for_klass_delta_5():
    if request.method == 'GET':
        session['spisok_klass'] = klass_ruk('Шоссе Энтузиастов, дом 96А')
        return render_template('Missing_report.html', spisok_klass=session['spisok_klass'])
    else:
        session['ur_class'] = request.form['ur_class']
        session['reshenie'] = prov(request.form['reshenie'])
        session['ORVI'] = prov(request.form['ORVI'])
        session['grip'] = prov(request.form['grip'])
        session['dr_zab'] = prov(request.form['dr_zab'])
        session['tr_v_school'] = prov(request.form['tr_v_school'])
        session['tr_vne_school'] = prov(request.form['tr_vne_school'])
        session['neizvest'] = prov(request.form['neizvest'])
        session['dist'] = prov(request.form['dist'])
        session['e_mail_text'] = opred_kinder(ur_class = session['ur_class'],
                    reshenie = session['reshenie'],
                     ORVI = session['ORVI'], grip = session['grip'],
                     dr_zab = session['dr_zab'], tr_v_school = session['tr_v_school'],
                    tr_vne_school = session['tr_vne_school'], neizvest = session['neizvest'], dist=session['dist'])
        otpravka(session['e_mail_text'][0], 'Отчет по посещаемости', session['e_mail_text'][1])
        return render_template('thanks_teachers.html', clas=session['ur_class'])


@app.route('/class_ruk_delta_6', methods = ['GET', 'POST'])
def for_klass_delta_6():
    if request.method == 'GET':
        session['spisok_klass'] = klass_ruk('Шоссе Энтузиастов, дом 96Б')
        return render_template('Missing_report.html', spisok_klass=session['spisok_klass'])
    else:
        session['ur_class'] = request.form['ur_class']
        session['reshenie'] = prov(request.form['reshenie'])
        session['ORVI'] = prov(request.form['ORVI'])
        session['grip'] = prov(request.form['grip'])
        session['dr_zab'] = prov(request.form['dr_zab'])
        session['tr_v_school'] = prov(request.form['tr_v_school'])
        session['tr_vne_school'] = prov(request.form['tr_vne_school'])
        session['neizvest'] = prov(request.form['neizvest'])
        session['dist'] = prov(request.form['dist'])
        session['e_mail_text'] = opred_kinder(ur_class = session['ur_class'],
                    reshenie = session['reshenie'],
                     ORVI = session['ORVI'], grip = session['grip'],
                     dr_zab = session['dr_zab'], tr_v_school = session['tr_v_school'],
                    tr_vne_school = session['tr_vne_school'], neizvest = session['neizvest'], dist=session['dist'])
        otpravka(session['e_mail_text'][0], 'Отчет по посещаемости', session['e_mail_text'][1])
        return render_template('thanks_teachers.html', clas=session['ur_class'])
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.run(debug=True)
