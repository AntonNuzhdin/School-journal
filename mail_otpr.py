import smtplib
from email.mime.text import MIMEText
from email.header    import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import os


def otpravka(poluchatel, tema_msg, pismo):
    login, password = 'admin@stu.1502.moscow', 'fqc,thu1502'
    server = smtplib.SMTP_SSL('smtp.yandex.ru:465')
    server.login(login, password)
    msg = MIMEMultipart('alternative','utf-8')
    msg['From'] = login
    msg['Subject'] = Header(tema_msg, 'utf-8')
    msg['To'] = poluchatel
    part2 = MIMEText(pismo, 'html')
    msg.attach(part2)
    server.sendmail(msg['From'], poluchatel, msg.as_string())
    server.close()


def text_prof(prof_1, prof_2, prof_3, nickname):
    text_otp = ('''
    <h1 style="text-align: center;"><strong>Доброго времени суток!</strong></h1>
    <p style="text-align: center;"><em>''' +
    nickname + ''', Вы выбрали следующие направления:</em></p>
    <p style="text-align: left;"><em>1. ''' + prof_1 + '''</em></p>
    <p style="text-align: left;"><em>2. ''' + prof_2 + '''</em></p>
    <p style="text-align: left;"><em>3. ''' + prof_3 + '''</em></p>
    <p style="text-align: center;">Они расположены в порядке Вашего приоритета</p>
    ''')
    return text_otp

#otpravka('tumanov-nv@1502.moscow', 'жопа', 'yb j xtv')
