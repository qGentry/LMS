from elms.domain.utils.secutiry_helper.security_helper import SecurityHelper


class SequrityManager:
    NOT_ALLOWED_MESSAGE = "Action not allowed for this profile"
    INVALID_TOKEN_MESSAGE = "Invalid auth token"

    def __init__(self,
                 self_allowed_profile_fields: tuple,
                 other_allowed_profile_fields: tuple,
                 security_helper: SecurityHelper,
                 ):
        self.self_allowed_profile_fields = set(self_allowed_profile_fields)
        self.other_allowed_profile_fields = set(other_allowed_profile_fields)
        self.security_helper = security_helper
        self.sessions = {}

    def is_allowed_manipulate_course_material(self, profile_id: int, course_id: int):
        return (
                self.security_helper.is_profile_teacher_for_course(profile_id, course_id)
                or
                self.security_helper.is_profile_confidant_for_course(profile_id, course_id)
        )

    def is_allowed_manipulate_course_material_by_material_id(self, profile_id: int, material_id: int):
        return self.security_helper.is_allowed_manipulate_course_material_by_material_id(profile_id, material_id)

    def is_allowed_full_course_control(self, profile_id: int, course_id: int):
        return self.security_helper.is_profile_teacher_for_course(profile_id, course_id)

    def is_allowed_homework_control(self, profile_id: int, homework_id: int):
        return self.security_helper.is_allowed_homework_control(profile_id, homework_id)

    def is_allowed_upload_homework(self, profile_id: int, homework_id: int):
        return (
                self.security_helper.can_student_upload_homework(profile_id, homework_id)
                and
                self.security_helper.can_homework_be_uploaded_by_date(homework_id)
        )

    def is_allowed_watch_homeworks(self, profile_id: int, course_id: int):
        return self.security_helper.is_student_course_listener(profile_id, course_id)

    def start_sessions(self, token: str, profile_id: int):
        self.sessions[token] = profile_id

    def get_profile_id_by_token(self, token: str):
        return self.sessions[token]

    def end_sessions(self, token: str):
        if token in self.sessions:
            del self.sessions[token]

    def check_sessions_exists(self, token: str):
        return token in self.sessions

    def get_allowed_profile_fields(self, token: str, profile_id: int):
        if self.sessions[token] == profile_id:
            return self.self_allowed_profile_fields
        else:
            return self.other_allowed_profile_fields
