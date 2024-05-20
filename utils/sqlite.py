import sqlite3
from handlers.models.user import User
from handlers.models.products import Product


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=None, fetchall=None, commit=False):
        if not parameters:
            parameters = ()
        with self.connection as connection:
            cursor = connection.cursor()
            data = None
            cursor.execute(sql, parameters)
            if fetchone:
                data = cursor.fetchone()
            if fetchall:
                data = cursor.fetchall()
            if commit:
                connection.commit()

        return data

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += "AND ".join([f"{item}=?" for item in parameters])
        return sql, tuple(parameters.values())

    def create_user_table(self):
        sql = """CREATE TABLE Users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT,
            phone TEXT,
            telegram_id TEXT
        )"""
        return self.execute(sql, commit=True)

    def create_product_table(self):
        # Create Products table
        sql_products = """CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY,
            product_code TEXT NOT NULL UNIQUE,
            description TEXT,
            created_by INTEGER,
            created TEXT NOT NULL,
            price FLOAT,
            quantity INTEGER,
            FOREIGN KEY (created_by) REFERENCES Users(id)
        )"""
        self.execute(sql_products, commit=True)

        # Create Photos table
        sql_photos = """CREATE TABLE IF NOT EXISTS Photos (
            id INTEGER PRIMARY KEY,
            product_id INTEGER NOT NULL,
            photo_url TEXT,
            FOREIGN KEY (product_id) REFERENCES Products(id)
        )"""
        self.execute(sql_photos, commit=True)

        return True

    def create_menu_table(self):
        sql = """CREATE TABLE Product_Menu(
        id INTEGER PRIMARY,
        name TEXT NOT NULL,
        create_at TEXT NOT NULL
        )"""

        return self.execute(sql, commit=True)

    def create_incoming_payment_table(self):
        sql = """CREATE TABLE IncomingMoney (
        id integer PRIMARY KEY,
        user_telegram_id text, 
        product_title TEXT NOT NULL,
        menturement INTEGER not null,
        created_by INTEGER NOT NULL,
        create_at TEXT,
        FOREIGN KEY (created_by) REFERENCES Users(id)
        )"""

        return self.execute(sql, commit=True)

    def create_outgoing_payment_table(self):
        sql = """CREATE TABLE  OutgoingMoney (
        id integer PRIMARY KEY,
        user_telegram_id text, 
        product_title TEXT NOT NULL,
        menturement INTEGER not null,
        created_by INTEGER NOT NULL,
        create_at TEXT,
        FOREIGN KEY (created_by) REFERENCES Users(id)
        )"""

        return self.execute(sql, commit=True)

    """CREATE"""

    def note_outgoing_payment(self, user_telegram_id, product_title, menturement, created_by, created_at):
        sql = """INSERT INTO OutgoingMoney  (user_telegram_id, product_title,menturement,created_by, create_at) VALUES (?,?,?,?,?)"""
        return self.execute(sql,
                            parameters=(user_telegram_id, product_title, menturement, created_by, created_at),
                            commit=True)

    def note_incoming_payment(self, user_telegram_id, product_title, menturement, created_by, created_at):
        sql = """INSERT INTO IncomingMoney (user_telegram_id, product_title,menturement, created_by, create_at) VALUES (?,?,?,?,?)"""
        return self.execute(sql,
                            parameters=(user_telegram_id, product_title, menturement, created_by, created_at),
                            commit=True)

    def create_product(self, data: Product):
        sql = """INSERT INTO Products(product_code, description, created_by, created, price, quantity) 
        VALUES (?,?,?,?,?, ?)"""
        return self.execute(sql, parameters=(
            data.product_code, data.description, data.created_by, data.created, data.price, data.quantity,),
                            commit=True)

    def connect_photo_with_product(self, product_id, photo):
        sql = """INSERT INTO Photos(product_id, photo_url) VALUES (?,?)"""
        return self.execute(sql, parameters=(product_id, photo), commit=True)

    def create_user(self, data: User):
        sql = """INSERT INTO Users (username, password, phone, telegram_id) VALUES (?,?,?,?)"""
        return self.execute(sql, parameters=(data.username, data.password, data.phone, data.telegram_id))

    """GET"""

    def get_all_products(self):
        """
        Retrieves all items from the database table.

        Returns:
            list: A list of items retrieved from the database.
        """
        sql = """SELECT * FROM Products"""
        return self.execute(sql, parameters=(), fetchall=True)

    def get_last_product_menu(self):
        sql = """SELECT * FROM Products ORDER BY id DESC LIMIT 1"""
        return self.execute(sql, fetchone=True)

    def get_last_product(self):
        sql = "SELECT * FROM Products ORDER BY id DESC LIMIT 1"
        return self.execute(sql, fetchone=True)

    def get_user_by_telegra_id(self, telegram_id):
        sql = """SELECT * FROM Users WHERE telegram_id = ?"""

        return self.execute(sql, parameters=(telegram_id,), fetchone=True)

    def get_product_photo_by_product_id(self, product_id):
        sql = """SELECT * FROM Photos where product_id = ?"""
        return self.execute(sql, parameters=(product_id,), fetchone=True)

    def get_products_with_pagination(self, skip=0, take=9):
        """
                Retrieves items from the database table with pagination.

                Args:
                    skip (int): The number of items to skip.
                    limit (int): The maximum number of items to retrieve.

                Returns:
                    list: A list of items retrieved from the database.
                """
        sql = """SELECT * FROM Products ORDER BY rowid DESC LIMIT ? OFFSET ?;"""
        return self.execute(sql, parameters=(take, skip), fetchall=True)

    def get_photo_by_product_id(self, product_id):
        sql = """SELECT * FROM Photos WHERE product_id = ?"""
        return self.execute(sql, parameters=(product_id,), fetchall=True)

    def get_product_by_product_code(self, product_code):
        sql = """SELECT * FROM Products WHERE product_code = ?"""
        return self.execute(sql, parameters=(product_code,), fetchone=True)

    def get_users(self):
        sql = """SELECT * FROM Users"""
        return self.execute(sql, fetchall=True)

    def get_user_by_phone(self, phone):
        sql = """SELECT * FROM Users WHERE phone=?"""
        return self.execute(sql=sql, parameters=(phone,), fetchone=True)

    def find_user_by_username(self, username):
        sql = """SELECT * FROM Users WHERE username=?"""
        return self.execute(sql, parameters=(username,), fetchone=True)

    def get_user_by_id(self, user_id):
        sql = """SELECT * FROM Users WHERE id = ? """
        return self.execute(sql, parameters=(user_id,), fetchone=True)

    """UPDATE"""

    def update_product_attributes(self, product_code, column, new_attributes):
        sql = f"""UPDATE Products SET {column}=? WHERE id=?"""
        return self.execute(sql, parameters=(new_attributes, product_code,), commit=True)

    def update_user_telegram_id_by_phone(self, phone, telegram_id):
        sql = """UPDATE Users SET telegram_id=? where phone=?"""
        return self.execute(sql, parameters=(telegram_id, phone), commit=True)

    def update_product_quantity(self, quantity, product_id):
        sql = """UPDATE Products SET quantity= ? where id = ?"""
        return self.execute(sql, parameters=(quantity, product_id,), commit=True)

    """DELETE"""

    def delete_user(self, data: User):
        sql = """DELETE FROM Users WHERE username=?"""
        return self.execute(sql, parameters=(data.username,), commit=True)
