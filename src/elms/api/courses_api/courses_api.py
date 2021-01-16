from elms.api.domain_api.domain_api import DomainAPI


class CoursesAPI(DomainAPI):

    NO_PROFILE_ID_ERROR = "You must specify profile_id"
    NO_COURSE_ID_ERROR = "You must specify course_id"
    NO_HOMEWORK_ID_ERROR = "You must specify homework_id"
    NO_MATERIAL_ID_ERROR = "You must specify material_id"
    NO_HOMEWORK_DATA_ERROR = "You must specify homework data as json content"
    NO_MATERIAL_DATA_ERROR = "You must specify material data as json content"
    NO_PARCEL_CONTENT_ERROR = "You must specify content to upload homework parcel"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process_get_request(self, request_queries, *args, **kwargs):
        if request_queries["action"] == "get_course_homeworks":
            if "course_id" not in request_queries:
                return self.NO_COURSE_ID_ERROR, False
            return self.sessions_manager.get_course_homeworks(
                request_queries["course_id"],
                request_queries["token"],
            )
        elif request_queries["action"] == "get_parcel_content":
            if "profile_id" not in request_queries:
                return self.NO_PROFILE_ID_ERROR, False
            if "homework_id" not in request_queries:
                return self.NO_HOMEWORK_ID_ERROR, False
            return self.sessions_manager.get_parcel_content(
                request_queries["homework_id"],
                request_queries["profile_id"],
                request_queries["token"]
            )
        elif request_queries["action"] == "get_students_homeworks":
            if "homework_id" not in request_queries:
                return self.NO_HOMEWORK_ID_ERROR, False
            return self.sessions_manager.get_students_homeworks(
                request_queries["homework_id"],
                request_queries["token"],
            )
        elif request_queries["action"] == "get_profile_courses":
            return self.sessions_manager.get_profile_courses(
                request_queries["token"]
            )
        elif request_queries["action"] == "get_course_info":
            if "course_id" not in request_queries:
                return self.NO_COURSE_ID_ERROR, False
            return self.sessions_manager.get_course_info(
                request_queries["course_id"],
                request_queries["token"],
            )
        else:
            return f"Unsupported action {request_queries['action']}", False

    def process_post_request(self, request_queries, *args, **kwargs):
        if request_queries["action"] == "add_homework":
            if "course_id" not in request_queries:
                return self.NO_COURSE_ID_ERROR, False
            if kwargs["json_content"] is None:
                return self.NO_HOMEWORK_DATA_ERROR, False
            return self.sessions_manager.add_homework(
                request_queries["course_id"],
                kwargs["json_content"],
                request_queries["token"],
            )
        elif request_queries["action"] == "modify_homework":
            if "homework_id" not in request_queries:
                return self.NO_HOMEWORK_ID_ERROR, False
            if kwargs["json_content"] is None:
                return self.NO_HOMEWORK_DATA_ERROR, False
            return self.sessions_manager.modify_homework(
                request_queries["homework_id"],
                kwargs["json_content"],
                request_queries["token"],
            )
        elif request_queries["action"] == "delete_homework":
            if "homework_id" not in request_queries:
                return self.NO_HOMEWORK_ID_ERROR, False
            return self.sessions_manager.delete_homework(
                request_queries["homework_id"],
                request_queries["token"]
            )
        elif request_queries["action"] == "add_material":
            if "course_id" not in request_queries:
                return self.NO_COURSE_ID_ERROR, False
            if kwargs["json_content"] is None:
                return self.NO_MATERIAL_DATA_ERROR, False
            return self.sessions_manager.add_material(
                request_queries["course_id"],
                kwargs["json_content"],
                request_queries["token"],
            )
        elif request_queries["action"] == "modify_material":
            if "material_id" not in request_queries:
                return self.NO_MATERIAL_ID_ERROR, False
            if kwargs["json_content"] is None:
                return self.NO_MATERIAL_DATA_ERROR, False
            return self.sessions_manager.modify_material(
                request_queries["material_id"],
                kwargs["json_content"],
                request_queries["token"],
            )
        elif request_queries["action"] == "delete_material":
            if "material_id" not in request_queries:
                return self.NO_MATERIAL_ID_ERROR, False
            return self.sessions_manager.delete_material(
                request_queries["material_id"],
                request_queries["token"]
            )
        elif request_queries["action"] == "add_confidant":
            if "course_id" not in request_queries:
                return self.NO_COURSE_ID_ERROR, False
            if "profile_id" not in request_queries:
                return self.NO_PROFILE_ID_ERROR, False
            return self.sessions_manager.add_confidant(
                request_queries["course_id"],
                request_queries["profile_id"],
                request_queries["token"],
            )
        elif request_queries["action"] == "delete_confidant":
            if "course_id" not in request_queries:
                return self.NO_COURSE_ID_ERROR, False
            if "profile_id" not in request_queries:
                return self.NO_PROFILE_ID_ERROR, False
            return self.sessions_manager.delete_confidant(
                request_queries["course_id"],
                request_queries["profile_id"],
                request_queries["token"],
            )
        elif request_queries["upload_homework_parcel"]:
            if "homework_id" not in request_queries:
                return self.NO_HOMEWORK_ID_ERROR, False
            if "content" not in request_queries:
                return self.NO_PARCEL_CONTENT_ERROR, False
            return self.sessions_manager.upload_homework_parcel(
                request_queries["homework_id"],
                request_queries["content"],
                request_queries["token"],
            )
        else:
            return f"Unsupported action {request_queries['action']}", False
