from elms.domain.groups.group_manager.group_manager import GroupManager
import sqlite3


class SqlGroupManager(GroupManager):

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.cursor = conn.cursor()

    def get_groupmates(self, profile_id: int):
        self.cursor.execute(
            "SELECT profile_id FROM profiles WHERE group_id =(SELECT group_id FROM profiles WHERE profile_id = ?)",
            (profile_id,))
        return self.cursor.fetchall()
