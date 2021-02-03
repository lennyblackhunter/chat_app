import sqlite3


class UsersDatabase:

    def __init__(self):
        self.conn = sqlite3.connect('users_database.db')
        self.curs = self.conn.cursor()

    def create_users_table(self):
        try:
            self.curs.execute(
                "CREATE TABLE users ('username' varchar(20) UNIQUE NOT NULL , 'password' varchar(20) NOT NULL)"
            )
        except sqlite3.OperationalError:
            pass
        self.conn.commit()

    def add_user(self, username, password):
        self.curs.execute(
            f"INSERT INTO users VALUES ('{username}', '{password}')"
        )
        self.conn.commit()

    def login_user(self, username, password):
        user = list(self.curs.execute(
            f"SELECT * FROM users WHERE username = '{username}'"
        ))
        if user:
            return password == user[0][1]
        else:
            self.add_user(username, password)
            return True

    def remove_user(self, username):
        self.curs.execute(
            f"DELETE FROM users WHERE username = '{username}'"
        )
        self.conn.commit()


if __name__ == '__main__':
    database = UsersDatabase()
    database.login_user('', '')
    database.remove_user('')

    database.conn.close()
