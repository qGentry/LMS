from abc import ABC, abstractmethod


class SecurityHelper(ABC):

    @abstractmethod
    def is_profile_student(self, profile_id: int) -> bool:
        pass

    @abstractmethod
    def is_profile_confidant_for_course(self, profile_id: int, course_id: int) -> bool:
        pass

    @abstractmethod
    def is_profile_teacher_for_course(self, profile_id: int, course_id: int) -> bool:
        pass

    @abstractmethod
    def can_homework_be_uploaded_by_date(self, homework_id: int):
        pass

    @abstractmethod
    def can_student_upload_homework(self, profile_id: int, homework_id: int):
        pass

    @abstractmethod
    def is_student_course_listener(self, profile_id: int, course_id: int):
        pass

    @abstractmethod
    def is_allowed_homework_control(self, profile_id: int, homework_id: int):
        pass

    @abstractmethod
    def is_allowed_manipulate_course_material_by_material_id(self, profile_id: int, material_id: int):
        pass

