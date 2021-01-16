import datetime
from typing import Tuple

from elms.domain.courses.courses_manager.courses_manager import CoursesManager
from elms.domain.groups.group_manager.group_manager import GroupManager
from elms.domain.profiles.login_handler.login_handler import LoginHandler
from elms.domain.profiles.profile_manager.profile_manager import ProfileManager
from elms.presenter.security_manager import SequrityManager


class SessionsManager:

    def __init__(self,
                 login_handler: LoginHandler,
                 profile_manager: ProfileManager,
                 group_manager: GroupManager,
                 courses_manager: CoursesManager,
                 sequrity_params: dict,
                 ):
        self.login_handler = login_handler
        self.profile_manager = profile_manager
        self.action_map = {
            "about": self.profile_manager.set_about,
            "phone": self.profile_manager.set_phone,
            "city": self.profile_manager.set_city,
            "facebook_link": self.profile_manager.set_facebook_link,
            "instagram_link": self.profile_manager.set_instagram_link,
            "linkedin_link": self.profile_manager.set_linkedin_link,
            "vk_link": self.profile_manager.set_vk_link,
        }
        self.group_manager = group_manager
        self.courses_manager = courses_manager
        self.security_manager = SequrityManager(**sequrity_params)

    def login(self, email: str, password: str) -> Tuple[str, bool]:
        response, profile_id, ok = self.login_handler.login(email, password)
        if ok:
            self.security_manager.start_sessions(response, profile_id)
            response = {"token": response, "profile_id": profile_id}
        return response, ok

    def logout(self, token: str):
        self.security_manager.end_sessions(token)

    def register(self, auth_code: str, email: str, password: str) -> Tuple[str, bool]:
        return self.login_handler.register(auth_code, email, password)

    def get_profile_courses(self, token: str) -> Tuple[str, bool]:
        if not self.security_manager.check_sessions_exists(token):
            return self.security_manager.INVALID_TOKEN_MESSAGE, False
        else:
            response = self.courses_manager.get_profile_courses(self.security_manager.get_profile_id_by_token(token))
            return response, True

    def get_groupmates(self, token: str) -> Tuple[str, bool]:
        if not self.security_manager.check_sessions_exists(token):
            return self.security_manager.INVALID_TOKEN_MESSAGE, False
        else:
            result = self.group_manager.get_groupmates(self.security_manager.get_profile_id_by_token(token))
            return result, True

    def get_profile_info(self, profile_id: int, token: str) -> Tuple[str, bool]:
        if not self.security_manager.check_sessions_exists(token):
            return self.security_manager.INVALID_TOKEN_MESSAGE, False
        else:
            allowed_field = self.security_manager.get_allowed_profile_fields(token, profile_id)
            return self.profile_manager.get_full_info(profile_id, allowed_field)

    def set_profile_info(self, data: str, token: str, field: str) -> Tuple[str, bool]:
        if not self.security_manager.check_sessions_exists(token):
            return self.security_manager.INVALID_TOKEN_MESSAGE, False
        else:
            if field not in self.action_map:
                return "Unknown field", False
            else:
                return self.action_map[field](data, self.security_manager.get_profile_id_by_token(token))

    def add_homework(self, course_id: int, homework_data: dict, token: str):
        if not self.security_manager.check_sessions_exists(token):
            return self.security_manager.INVALID_TOKEN_MESSAGE, False
        elif not self.security_manager.is_allowed_full_course_control(
                self.security_manager.get_profile_id_by_token(token),
                course_id,
        ):
            return self.security_manager.NOT_ALLOWED_MESSAGE, False
        else:
            response, ok = self.courses_manager.add_homework(course_id, homework_data)
            return response, ok

    def modify_homework(self, homework_id: int, homework_data: dict, token: str):
        if not self.security_manager.check_sessions_exists(token):
            return self.security_manager.INVALID_TOKEN_MESSAGE, False
        elif not self.security_manager.is_allowed_homework_control(
                self.security_manager.get_profile_id_by_token(token),
                homework_id,
        ):
            return self.security_manager.NOT_ALLOWED_MESSAGE, False
        else:
            response, ok = self.courses_manager.modify_homework(homework_id, homework_data)
            return response, ok

    def delete_homework(self, homework_id: int, token: str):
        if not self.security_manager.check_sessions_exists(token):
            return self.security_manager.INVALID_TOKEN_MESSAGE, False
        elif not self.security_manager.is_allowed_homework_control(
                self.security_manager.get_profile_id_by_token(token),
                homework_id,
        ):
            return self.security_manager.NOT_ALLOWED_MESSAGE, False
        else:
            response, ok = self.courses_manager.delete_homework(homework_id)
            return response, ok

    def add_material(self, course_id: int, material_data: dict, token: str):
        if not self.security_manager.check_sessions_exists(token):
            return self.security_manager.INVALID_TOKEN_MESSAGE, False
        elif not self.security_manager.is_allowed_manipulate_course_material(
                self.security_manager.get_profile_id_by_token(token),
                course_id,
        ):
            return self.security_manager.NOT_ALLOWED_MESSAGE, False
        else:
            response, ok = self.courses_manager.add_material(course_id, material_data)
            return response, ok

    def modify_material(self, material_id: int, material_data: dict, token: str):
        if not self.security_manager.check_sessions_exists(token):
            return self.security_manager.INVALID_TOKEN_MESSAGE, False
        elif not self.security_manager.is_allowed_manipulate_course_material_by_material_id(
                self.security_manager.get_profile_id_by_token(token),
                material_id,
        ):
            return self.security_manager.NOT_ALLOWED_MESSAGE, False
        else:
            response, ok = self.courses_manager.modify_material(material_id, material_data)
            return response, ok

    def delete_material(self, material_id: int, token: str):
        if not self.security_manager.check_sessions_exists(token):
            return self.security_manager.INVALID_TOKEN_MESSAGE, False
        elif not self.security_manager.is_allowed_manipulate_course_material_by_material_id(
                self.security_manager.get_profile_id_by_token(token),
                material_id,
        ):
            return self.security_manager.NOT_ALLOWED_MESSAGE, False
        else:
            response, ok = self.courses_manager.delete_material(material_id)
            return response, ok

    def add_confidant(self, course_id: int, profile_id: int, token: str):
        if not self.security_manager.check_sessions_exists(token):
            return self.security_manager.INVALID_TOKEN_MESSAGE, False
        elif not self.security_manager.is_allowed_full_course_control(
                self.security_manager.get_profile_id_by_token(token),
                course_id
        ):
            return self.security_manager.NOT_ALLOWED_MESSAGE, False
        else:
            return self.courses_manager.add_confidant(course_id, profile_id)

    def delete_confidant(self, course_id: int, profile_id: int, token: str):
        if not self.security_manager.check_sessions_exists(token):
            return self.security_manager.INVALID_TOKEN_MESSAGE, False
        elif not self.security_manager.is_allowed_full_course_control(
                self.security_manager.get_profile_id_by_token(token),
                course_id
        ):
            return self.security_manager.NOT_ALLOWED_MESSAGE, False
        else:
            return self.courses_manager.delete_confidant(course_id, profile_id)

    def upload_homework_parcel(self, homework_id: int, content: str, token: str):
        if not self.security_manager.check_sessions_exists(token):
            return self.security_manager.INVALID_TOKEN_MESSAGE, False
        elif not self.security_manager.is_allowed_upload_homework(
                self.security_manager.get_profile_id_by_token(token),
                homework_id,
        ):
            return self.security_manager.NOT_ALLOWED_MESSAGE, False
        else:
            response, ok = self.courses_manager.upload_homework_parcel(
                self.security_manager.get_profile_id_by_token(token),
                homework_id,
                content,
            )
            return response, ok

    def get_parcel_content(self, homework_id: int, profile_id: int, token: str):
        if not self.security_manager.check_sessions_exists(token):
            return self.security_manager.INVALID_TOKEN_MESSAGE, False
        elif not self.security_manager.is_allowed_homework_control(
                self.security_manager.get_profile_id_by_token(token),
                homework_id,
        ):
            return self.security_manager.NOT_ALLOWED_MESSAGE, False
        else:
            response, ok = self.courses_manager.get_parcel_content(homework_id, profile_id)
            return response, ok

    def get_course_homeworks(self, course_id: int, token: str):
        if not self.security_manager.check_sessions_exists(token):
            return self.security_manager.INVALID_TOKEN_MESSAGE, False
        elif not self.security_manager.is_allowed_watch_homeworks(
                self.security_manager.get_profile_id_by_token(token),
                course_id,
        ):
            return self.security_manager.NOT_ALLOWED_MESSAGE, False
        else:
            response = self.courses_manager.get_course_homeworks(course_id)
            response = self._filter_homeworks_by_date(response)
            return response, True

    def get_students_homeworks(self, homework_id: int, token: str):
        if not self.security_manager.check_sessions_exists(token):
            return self.security_manager.INVALID_TOKEN_MESSAGE, False
        elif self.security_manager.is_allowed_homework_control(
                self.security_manager.get_profile_id_by_token(token),
                homework_id,
        ):
            return self.security_manager.NOT_ALLOWED_MESSAGE, False
        else:
            response, ok = self.courses_manager.get_students_homeworks(homework_id)
            return response, ok

    def get_course_info(self, course_id: int, token: str):
        if not self.security_manager.check_sessions_exists(token):
            return self.security_manager.INVALID_TOKEN_MESSAGE, False
        else:
            response, ok = self.courses_manager.get_course_info(course_id)
            if ok:
                response["course_homeworks"] = self._filter_homeworks_by_date(response["course_homeworks"])
            return response, ok

    @staticmethod
    def _filter_homeworks_by_date(homeworks):
        now = datetime.datetime.now()
        return list(
            filter(lambda x: datetime.datetime.strptime(x["open_date"], "%Y-%m-%d %H:%M:%S") <= now, homeworks)
        )
