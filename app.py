from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
app = Flask(__name__)

def connect_db():
    conn = sqlite3.connect("data_base.db")
    conn.row_factory=sqlite3.Row
    return conn

def init_db():
    conn = connect_db()
    conn.execute("""
        CREATE TABLE IF NOT EXIST users(
        id INT PRIMARY KEY AUTOINCREMENT,
        password VARCHAR(25),
        login VARCHAR(20) UNIQUE,
        email VARCHAR(30) UNIQUE,
        phone_number VARCHAR(20) UNIQUE
        )


        CREATE TABLE IF NOT EXIST topics(
                   id INT PRIMARY KEY AUTOINCREMENT,
                   description TEXT,
                   name TEXT UNIQUE
        )
        CREATE TABLE IF NOT EXIST articles(
                   id INT PRIMARY KEY AUTOINCREMENT,
                   topics_id INT,
                   text TEXT

                   FOREIGN KEY (topics_id) REFERENCES topics(id)
        )
        CREATE TABLE IF NOT EXIST wikipedia(
                   id INT PROMARY KEY AUTOINCREMENT,
                   topics_id INT,
                   articles_id INT

                   FOREIGN KEY (topics_id) REFERENCES topics(id)
                   FOREIGN KEY (articles_id) REFERENCES articles(id) 
        )
        
    """)
    conn.execute("INSERT INTO topics (desciption, name) VALUES (?, ?)",
                 ("Пример описания", "Наука"))
    conn.execute("INSERT INTO topics (description, name) VALUES (?,?)",
                 ("Пример описания", "История"))
    conn.commit()
    conn.close()
    

def profile():
    conn = sqlite3.connect("data_base.db")
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO users(password, login, email, phone_number) VALUES(?, ?, ?, ?)""",
                   ( '123456789', 'Idontknow', 'qwerty@gmail.com', '+79262673131'))
    conn.commit()
    conn.close()



@app.route('/register')
def register():
    data = request.get_json()
    if not data:
        return jsonify({
    'ok' : False,
    'error' : 'no_json'
    }), 400
    password = data['password']
    login = data['login']
    email = data['email']
    phone_number = data['phone_number']

    if not password or not login or not email:
        return jsonify({
            "message" : "Не все поля были заполнены"
        })
    
    password_hash = generate_password_hash(password)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO users(password, login, email, phone_number) VALUES(?, ?, ?, ?)""",
                   (password_hash, login, email, phone_number))
    conn.commit()
    conn.close()
    return jsonify({
        "message" : "registration is ok"
    })
    

@app.route("/login")
def login():
    data = request.get_json()
    if not data:
        return jsonify({
            "message" : "Поля не могут быть пустыми"
        }), 400



    password = data['password']
    email = data['email']
    if not "@" in email:
        return jsonify({
            "message" : "В почте допущена ошибка"
        }), 400
    if len(password) < 8:
        return jsonify({
            "message" : "Пароль слишком короткий"
        }), 400


        
    conn = sqlite3.connect("data_base.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cur.fetchone()
    if not user:
        conn.close()
        return jsonify({
            "message" : "Пользователя не существует"
        }), 400
    # check_password_hash(пароль который пришел от польз, пароль из БД)
    if not check_password_hash(user["password"], password):
        conn.close()
        return jsonify({
            "message" : "Пароль не верный"
        }), 400
    conn.close()
    return jsonify({
        "message" : "Вы успешно авторизовались"
    }), 200


@app.route("/")
def main():
    conn = connect_db
    conn.execute("SELECT name FROM topics")
    name = conn.fetchall()
    return jsonify({
        "topics" : name
    })
    conn.close()
if __name__  == "__main__":
    app.run()