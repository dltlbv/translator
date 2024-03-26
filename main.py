import hashlib
import sqlite3
from googletrans import Translator


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = hashlib.sha512(password.encode()).hexdigest()


class Controller:
    def __init__(self):
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()
        self.create_table()
        self.current_user = None
        self.translator = Translator()

    def create_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            username TEXT UNIQUE,
                            password TEXT)"""
        )
        self.conn.commit()

    def register(self):
        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")
        self.cursor.execute(
            """INSERT INTO users (username, password)
                            VALUES (?, ?)""",
            (username, hashlib.sha512(password.encode()).hexdigest()),
        )
        self.conn.commit()
        print("Успешная регистрация")

    def login(self):
        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")
        self.cursor.execute(
            """SELECT * FROM users WHERE username = ? AND password = ?""",
            (username, hashlib.sha512(password.encode()).hexdigest()),
        )
        user = self.cursor.fetchone()
        if user:
            self.current_user = User(user[1], user[2])
            print("Вы вошли в аккаунт!")
        else:
            print("Неверно введены данные!")

    def logout(self):
        self.current_user = None
        print("Вы вышли из аккаунта!")

    def translate(self):
        if self.current_user is None:
            print("Для выполнения перевода необходимо войти в систему")
            return

        translator = Translator()
        text = input("Введите текст для перевода: ")
        source_lang = translator.detect(text).lang
        print(f"Определен язык введенного текста: {source_lang}")
        target_lang = input(
            "Введите код языка, на который хотите перевести текст (например, en для английского): "
        )
        translation = self.translator.translate(text, src=source_lang, dest=target_lang)
        translated_text = translation.text
        print(f"Перевод: {translated_text}")


controller = Controller()

while True:
    print("1. Зарегистрироваться")
    print("2. Войти")
    print("3. Перевести текст")
    print("4. Выйти")

    user_input = input("Выберите действие: ")

    if user_input == "1":
        controller.register()
    elif user_input == "2":
        controller.login()
    elif user_input == "3":
        controller.translate()
    elif user_input == "4":
        controller.logout()
        break
    else:
        print("Некорректный ввод")
