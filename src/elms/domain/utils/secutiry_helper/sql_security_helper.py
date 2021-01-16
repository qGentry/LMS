from elms.domain.utils.secutiry_helper.security_helper import SecurityHelper
import time
import sqlite3


class SqlSecurityHelper(SecurityHelper):

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.cursor = conn.cursor()

    def is_profile_student(self, profile_id: int) -> bool:
        self.cursor.execute(
            "SELECT * FROM teachers WHERE profile_id = ?", (profile_id,),
        )
        return not bool(self.cursor.fetchall())

    def is_student_course_listener(self, profile_id: int, course_id: int):
        self.cursor.execute(
            """
            SELECT * 
            FROM profiles 
            WHERE 
            group_id IN (SELECT group_id FROM group_courses WHERE course_id = ?)
            AND
            profile_id = ?
            """,
            (course_id, profile_id)
        )
        return bool(self.cursor.fetchone())

    def is_profile_confidant_for_course(self, profile_id: int, course_id: int) -> bool:
        self.cursor.execute(
            "SELECT * FROM courses_confidants WHERE profile_id = ? AND course_id = ?",
            (profile_id, course_id),
        )
        return bool(self.cursor.fetchone())

    def is_profile_teacher_for_course(self, profile_id: int, course_id: int) -> bool:
        if self.is_profile_student(profile_id):
            return False
        else:
            self.cursor.execute(
                """
                SELECT * FROM courses 
                WHERE course_id = ? AND 
                teacher_id = (SELECT teacher_id FROM teachers WHERE profile_id = ?)
                """,
                (course_id, profile_id),
            )
            return bool(self.cursor.fetchone())

    def can_homework_be_uploaded_by_date(self, homework_id: int):
        cur_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            """
            SELECT *
            FROM courses_homeworks
            WHERE homework_id = ? AND
            open_date < ? AND ? < close_date
            """,
            (homework_id, cur_time, cur_time)
        )
        return bool(self.cursor.fetchone())

    def can_student_upload_homework(self, profile_id: int, homework_id: int):
        self.cursor.execute(
            """
            SELECT * 
            FROM profiles 
            WHERE group_id IN
            (SELECT group_id FROM group_courses WHERE course_id = 
            (SELECT course_id FROM courses_homeworks WHERE homework_id = ?))
            AND
            profile_id = ?
            """,
            (homework_id, profile_id)
        )
        return bool(self.cursor.fetchone())

    def is_allowed_homework_control(self, profile_id: int, homework_id: int):
        self.cursor.execute(
            """
            SELECT * FROM courses 
            WHERE course_id = (SELECT course_id FROM courses_homeworks WHERE homework_id = ?)
            AND 
            teacher_id = (SELECT teacher_id FROM teachers WHERE profile_id = ?)
            """,
            (homework_id, profile_id)
        )
        return bool(self.cursor.fetchone())

    def is_allowed_manipulate_course_material_by_material_id(self, profile_id: int, material_id: int):
        self.cursor.execute(
            """
            SELECT * 
            FROM courses_confidants
            WHERE profile_id = ?
            AND
            course_id = (SELECT course_id FROM courses_materials WHERE material_id = ?)
            """,
            (profile_id, material_id)
        )
        is_confidant = bool(self.cursor.fetchone())
        self.cursor.execute(
            """
            SELECT course_id
            FROM courses_materials
            WHERE material_id = ?
            """,
            (material_id,)
        )
        course_id = self.cursor.fetchone()
        if course_id:
            is_teacher = self.is_profile_teacher_for_course(profile_id, course_id[0])
        else:
            is_teacher = False
        return is_confidant or is_teacher
