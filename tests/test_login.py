import unittest
from elms.domain.profiles.login_handler.sql_login_handler import SqlLoginHandler
import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class TestAuth(unittest.TestCase):
    def test_login(self):
        conn = sqlite3.connect("databases/database")
        conn.row_factory = dict_factory
        slh = SqlLoginHandler(conn)
        token, profile_id, ok = slh.login("test", "test")
        self.assertEqual(ok, True)


if __name__ == '__main__':
    unittest.main()
