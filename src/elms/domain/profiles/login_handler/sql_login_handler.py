import random
import string
import sqlite3
import re
from elms.domain.profiles.login_handler.login_handler import LoginHandler
from typing import Tuple, Union

email_regex = re.compile(r'[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+')

# at least: 8 chars, 2 uppercase, 1 special character (!@#$&*), 2 numerals (0-9), 3 lowercase
password_regex = re.compile(r"(?=.*[A-Z].*[A-Z])(?=.*[!@#$&*])(?=.*[0-9].*[0-9])(?=.*[a-z].*[a-z].*[a-z]).{8,}")


class SqlLoginHandler(LoginHandler):

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.cursor = conn.cursor()

    @staticmethod
    def _check_email_ok(email):
        return email_regex.fullmatch(email)

    @staticmethod
    def _check_password_ok(password):
        return password_regex.fullmatch(password)

    def register(self, auth_code: str, email: str, password: str) -> Tuple[str, bool]:
        if not self._check_email_ok(email):
            return "Invalid email", False
        if not self._check_password_ok(password):
            return "Password not secure enough, your password should have at least: " \
                   "8 chars, 2 uppercase, 1 special character (!@#$&*), 2 numerals (0-9), 3 lowercase", False
        self.cursor.execute('UPDATE profiles SET email = ?, password = ? WHERE verification_code = ?',
                            (email, password, auth_code))
        self.conn.commit()
        if self.cursor.rowcount:
            return "OK", True
        else:
            return "Auth code doesn't exists", False

    def login(self, email: str, password: str) -> Tuple[str, Union[int, None], bool]:
        self.cursor.execute("SELECT profile_id FROM profiles WHERE email = ? and password = ?", (email, password))
        result = self.cursor.fetchone()
        if result:
            return self._get_auth_token(), result["profile_id"], True
        else:
            return "Invalid login or password", None, False

    def change_password(self, new_password: str, old_password: str, email: str):
        if not self._check_password_ok(new_password):
            return "New password not secure enough, your password should have at least: " \
                   "8 chars, 2 uppercase, 1 special character (!@#$&*), 2 numerals (0-9), 3 lowercase", False
        self.cursor.execute('UPDATE profiles SET password = ? WHERE password = ? and email = ?',
                            (new_password, old_password, email))
        self.conn.commit()
        if self.cursor.rowcount:
            return "OK", True
        else:
            return "Invalid email or password", False

    @staticmethod
    def _get_auth_token():
        pool = string.ascii_letters + string.digits
        return ''.join(random.choice(pool) for _ in range(64))
