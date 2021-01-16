import sqlite3
import time
from elms.domain.courses.courses_manager.courses_manager import CoursesManager


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class SqlCoursesManager(CoursesManager):

    def _is_profile_student(self, profile_id: int):
        self.cursor.execute(
            "SELECT * FROM teachers WHERE profile_id = ?", (profile_id,),
        )
        return not bool(self.cursor.fetchall())

    def __init__(self, conn: sqlite3.Connection):
        super().__init__()
        self.conn = conn
        self.cursor = conn.cursor()

    @staticmethod
    def get_cur_time():
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def get_profile_courses(self, profile_id: int):
        if not self._is_profile_student(profile_id):
            self.cursor.execute(
                "SELECT course_name, description, course_id "
                "from courses where teacher_id = "
                "(SELECT teacher_id FROM teachers WHERE profile_id = ?)", (profile_id,))
            return self.cursor.fetchall()
        else:
            self.cursor.execute(
                "SELECT course_name, description, group_courses.course_id  "
                "FROM group_courses inner join courses on group_courses.course_id=courses.course_id "
                "WHERE group_id = (SELECT group_id FROM profiles WHERE profile_id = ?)",
                (profile_id,)
            )
            return self.cursor.fetchall()

    def add_homework(self, course_id: int, homework_data: dict):
        if not self.is_homework_data_full(homework_data):
            return "Not enough fields passed to add homework", False
        self.cursor.execute(
            "INSERT INTO courses_homeworks (course_id, name, description, open_date, close_date) VALUES (?, ?, ?, ?, ?)",
            (course_id,
             homework_data["name"],
             homework_data["description"],
             homework_data["open_date"],
             homework_data["close_date"],
             )
        )
        self.conn.commit()
        if self.cursor.rowcount:
            return "OK", True
        else:
            return "Couldn't add homework", False

    def modify_homework(self, homework_id: int, homework_data: dict):
        if not self.is_homework_data_valid(homework_data):
            return "Wrong fields passed for homework update", False
        changed_fields = list(homework_data.keys())
        # no sql injection here because of field checking above

        q = f"UPDATE courses_homeworks SET {','.join(field + '=?' for field in changed_fields)} " \
            f"WHERE homework_id = ?"
        data = [homework_data[field] for field in changed_fields]
        data.append(homework_id)
        self.cursor.execute(q, tuple(data))
        self.conn.commit()
        if self.cursor.rowcount:
            return "OK", True
        else:
            return f"Couldn't find homework with id = {homework_id}"

    def delete_homework(self, homework_id: int):
        self.cursor.execute("DELETE FROM courses_homeworks WHERE homework_id=?", (homework_id,))
        self.conn.commit()
        if self.cursor.rowcount:
            return "OK", True
        else:
            return f"Couldn't find homework with id = {homework_id}"

    def add_confidant(self, course_id: int, profile_id: int):
        self.cursor.execute(
            "INSERT INTO courses_confidants (course_id, profile_id) VALUES (?, ?)",
            (course_id, profile_id),
        )
        if self.cursor.rowcount:
            return "OK", True
        else:
            return "Couldn't add confidant", False

    def delete_confidant(self, course_id: int, profile_id: int):
        self.cursor.execute(
            "DELETE FROM courses_confidants WHERE course_id = ? AND profile_id = ?",
            (course_id, profile_id)
        )
        if self.cursor.rowcount:
            return "OK", True
        else:
            return "Couldn't delete confidant", False

    def add_material(self, course_id: int, material_data: dict):
        if not self.is_material_data_full(material_data):
            return "Not enough fields passed to add material", False
        self.cursor.execute(
            "INSERT INTO courses_materials (course_id, material_name, content, last_changed) VALUES (?, ?, ?, ?)",
            (course_id,
             material_data["material_name"],
             material_data["content"],
             self.get_cur_time(),
             )
        )
        self.conn.commit()
        if self.cursor.rowcount:
            return "OK", True
        else:
            return "Couldn't add material", False

    def modify_material(self, material_id: int, material_data: dict):
        if not self.is_material_data_valid(material_data):
            return "Wrong fields passed for homework update", False
        changed_fields = list(material_data.keys())

        q = f"UPDATE courses_materials SET {','.join(field + '=?' for field in changed_fields)}, last_changed = ? " \
            f"WHERE material_id = ?"
        data = [material_data[field] for field in changed_fields]
        data.append(self.get_cur_time())
        data.append(material_id)
        self.cursor.execute(q, tuple(data))
        self.conn.commit()
        if self.cursor.rowcount:
            return "OK", True
        else:
            return f"Couldn't find material with id = {material_id}"

    def delete_material(self, material_id: int):
        self.cursor.execute("DELETE FROM courses_materials WHERE material_id=?", (material_id,))
        self.conn.commit()
        if self.cursor.rowcount:
            return "OK", True
        else:
            return f"Couldn't find material with id = {material_id}"

    def _check_student_sent_any_parcel(self, profile_id: int, homework_id: int):
        self.cursor.execute(
            "SELECT * FROM courses_hw_parcels WHERE profile_id = ? AND homework_id = ?",
            (profile_id, homework_id)
        )
        return bool(self.cursor.fetchone())

    def upload_homework_parcel(self, profile_id: int, homework_id: int, content: str):
        if self._check_student_sent_any_parcel(profile_id, homework_id):
            self.cursor.execute(
                "UPDATE courses_hw_parcels SET content=?, date_uploaded=? WHERE profile_id = ? and homework_id = ?",
                (content, self.get_cur_time(), profile_id, homework_id)
            )
        else:
            self.cursor.execute(
                "INSERT INTO courses_hw_parcels (profile_id, homework_id, content, date_uploaded) VALUES (?, ?, ?, ?)",
                (profile_id, homework_id, content, self.get_cur_time())
            )
        self.conn.commit()
        if self.cursor.rowcount:
            return "OK", True
        else:
            return "Couldn't upload homework parcel", False

    def get_parcel_content(self, homework_id: int, profile_id: int):
        self.cursor.execute(
            "SELECT content FROM courses_hw_parcels WHERE profile_id = ? AND homework_id = ?",
            (profile_id, homework_id)
        )
        return self.cursor.fetchone()[0]

    def get_course_homeworks(self, course_id: int):
        self.cursor.execute(
            "SELECT name, description, open_date, close_date FROM courses_homeworks WHERE course_id = ?",
            (course_id,)
        )
        return self.cursor.fetchall()

    def get_students_homeworks(self, homework_id: int):
        self.cursor.execute(
            """
            SELECT profiles.profile_id, name, content, date_uploaded, group_id
            FROM profiles 
            LEFT JOIN courses_hw_parcels ON profiles.profile_id = courses_hw_parcels.profile_id 
            WHERE group_id IN
            (SELECT group_id FROM group_courses WHERE course_id = 
            (SELECT course_id FROM courses_homeworks WHERE homework_id = ?))  
             
            """,
            (homework_id,)
        )
        return self.cursor.fetchall()

    def get_course_info(self, course_id: int):
        self.cursor.execute(
            """
            SELECT course_name, description, teacher_id
            FROM courses
            WHERE course_id = ?
            """,
            (course_id,)
        )
        course_basics = self.cursor.fetchone()
        self.cursor.execute(
            """
            SELECT profile_id
            FROM courses_confidants
            WHERE course_id = ?
            """,
            (course_id,)
        )
        course_confidants = self.cursor.fetchall()
        self.cursor.execute(
            """
            SELECT material_name, content, last_changed
            FROM courses_materials
            WHERE course_id = ?
            """,
            (course_id,)
        )
        course_materials = self.cursor.fetchall()
        course_homeworks = self.get_course_homeworks(course_id)
        result = {
            "basic_information": course_basics,
            "course_materials": course_materials,
            "course_homeworks": course_homeworks,
            "course_confidants": course_confidants,
        }
        return result, True

