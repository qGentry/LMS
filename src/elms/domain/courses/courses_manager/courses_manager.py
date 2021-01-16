from abc import ABC, abstractmethod


class CoursesManager(ABC):

    def __init__(self):
        self.homework_fields = {"name", "description", "open_date", "close_date"}
        self.material_fields = {"material_name", "content"}

    def is_homework_data_valid(self, homework_data: dict):
        for key in homework_data:
            if key not in self.homework_fields:
                return False
        return True

    def is_homework_data_full(self, homework_data: dict):
        return set(homework_data.keys()) == self.homework_fields

    def is_material_data_valid(self, material_data: dict):
        for key in material_data:
            if key not in self.material_fields:
                return False
        return True

    def is_material_data_full(self, material_data: dict):
        return set(material_data.keys()) == self.material_fields

    @abstractmethod
    def get_course_info(self, course_id: int):
        pass

    @abstractmethod
    def get_profile_courses(self, profile_id: int):
        pass

    @abstractmethod
    def _is_profile_student(self, profile_id: int):
        pass

    @abstractmethod
    def add_homework(self, course_id: int, homework_data: dict):
        pass

    @abstractmethod
    def modify_homework(self, homework_id: int, homework_data: dict):
        pass

    @abstractmethod
    def delete_homework(self, homework_id: int):
        pass

    @abstractmethod
    def add_material(self, course_id: int, material_data: dict):
        pass

    @abstractmethod
    def modify_material(self, material_id: int, material_data: dict):
        pass

    @abstractmethod
    def delete_material(self, material_id: int):
        pass

    @abstractmethod
    def add_confidant(self, course_id: int, profile_id: int):
        pass

    @abstractmethod
    def delete_confidant(self, course_id: int, profile_id: int):
        pass

    @abstractmethod
    def upload_homework_parcel(self, profile_id: int, homework_id: int, content: str):
        pass

    @abstractmethod
    def get_parcel_content(self, homework_id: int, profile_id: int):
        pass

    @abstractmethod
    def get_course_homeworks(self, course_id: int):
        pass

    @abstractmethod
    def get_students_homeworks(self, homework_id: int):
        pass
