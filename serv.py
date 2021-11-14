from flask import Flask, render_template
import sqlite3


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

@app.route('/user/<username>/<int:value>')
def show_user_profile(username, value):
    # показать профиль данного пользователя
    db = sqlite3.connect(r"C:\Users\Senya\Downloads\baza_for_sait2.db")
    cursor = db.cursor()
    test = cursor.execute("Select присутствие From student_11 Where фио='"+username+"' ")
    if(test!='Да'):
        cursor = db.cursor()
        test = cursor.execute("Update student_11 Set присутствие='Дв' Where фио='" + username + "' ")
    else:
        cursor = db.cursor()
        test = cursor.execute("Update student_11 Set присутствие='Нет' Where фио='" + username + "' ")




    db.commit()
    return 'User %s' % username


if __name__ == "__main__":
    app.run()
