import sqlite3

from flask import Flask, request, abort

import json

from elms.api.courses_api.courses_api import CoursesAPI
from elms.api.domain_api.domain_api import DomainAPI
from elms.api.groups_api.groups_api import GroupsAPI
from elms.api.profile_api.profile_api import ProfileAPI
from elms.domain.courses.courses_manager.sql_courses_manager import SqlCoursesManager
from elms.domain.groups.group_manager.sql_group_manager import SqlGroupManager
from elms.domain.profiles.login_handler.sql_login_handler import SqlLoginHandler
from elms.domain.profiles.profile_manager.sql_profile_manager import SqlProfileManager
from elms.presenter.session_manager import SessionsManager
from elms.domain.utils.secutiry_helper.sql_security_helper import SqlSecurityHelper


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


conn = sqlite3.connect("databases/database", check_same_thread=False)
conn.row_factory = dict_factory

params = {
    "login_handler": SqlLoginHandler(conn),
    "profile_manager": SqlProfileManager(conn),
    "group_manager": SqlGroupManager(conn),
    "courses_manager": SqlCoursesManager(conn),
    "sequrity_params": {
        "other_allowed_profile_fields": ('admission_year', 'academic_degree', 'form', 'city', 'about', 'link_vk',
                                         'phone', 'link_instagram', 'link_facebook', 'link_linkedin', 'name', 'email'),
        "self_allowed_profile_fields": ('admission_year', 'academic_degree', 'form', 'city', 'about', 'link_vk',
                                        'link_instagram', 'link_facebook', 'link_linkedin', 'name', 'email',
                                        'phone', "education_base"),
        "security_helper": SqlSecurityHelper(conn)
    }
}

sessions_manager = SessionsManager(**params)
app = Flask(__name__)


def create_api_handler(api: DomainAPI, name: str):
    def handler():
        if "token" not in request.args:
            abort(403)
        if "action" not in request.args:
            abort(400)
        if request.method == "GET":
            response, ok = api.process_get_request(request.args, json_content=request.json)
            return_code = 200
        else:
            response, ok = api.process_post_request(request.args, json_content=request.json)
            return_code = 201
        if ok:
            return json.dumps({"response": response}), return_code
        else:
            return json.dumps({"error": response}), 401

    handler.__name__ = name
    return handler


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/login', methods=["POST"])
def login():
    if "email" not in request.args or "password" not in request.args:
        abort(400)
    email = request.args["email"]
    password = request.args["password"]
    response, ok = sessions_manager.login(email, password)
    if ok:
        return json.dumps({"response": response}), 200
    else:
        return json.dumps({"error": response}), 401


@app.route('/logout', methods=["POST"])
def logout():
    if "token" not in request.args:
        abort(400)
    sessions_manager.logout(request.args["token"])
    return json.dumps({"response": "OK"}), 200


@app.route('/register', methods=["POST"])
def register():
    if "email" not in request.args or "password" not in request.args or "auth_code" not in request.args:
        abort(400)
    response, ok = sessions_manager.register(request.args["auth_code"], request.args["email"], request.args["password"])
    if ok:
        return json.dumps({"response": response}), 200
    else:
        return json.dumps({"error": response}), 401


@app.route('/profiles/<profile_id>', methods=["GET"])
def profiles(profile_id):
    if "token" not in request.args:
        abort(403)
    response, ok = profile_api.process_get_request(
        {"action": "get_profile_info", "profile_id": profile_id, "token": request.args["token"]}
    )
    if ok:
        return json.dumps({"response": response})
    else:
        return json.dumps({"error": response})


@app.route('/courses/<course_id>', methods=["GET"])
def courses_info(course_id):
    if "token" not in request.args:
        abort(403)
    response, ok = courses_api.process_get_request(
        {"action": "get_course_info", "course_id": course_id, **request.args}
    )
    if ok:
        return json.dumps({"response": response})
    else:
        return json.dumps({"error": response})


@app.route('/courses/<course_id>/<action>', methods=["GET", "POST"])
def courses_action(course_id, action):
    if "token" not in request.args:
        abort(403)
    if request.method == "GET":
        response, ok = courses_api.process_get_request(
            {"action": action, "course_id": course_id, **request.args}
        )
    else:
        response, ok = courses_api.process_post_request(
            {"action": action, "course_id": course_id, **request.args}
        )
    if ok:
        return json.dumps({"response": response})
    else:
        return json.dumps({"error": response})


@app.route('/courses/homeworks/<homework_id>/<action>', methods=["GET", "POST"])
def homework_action(homework_id, action):
    if "token" not in request.args:
        abort(403)
    if request.method == "GET":
        response, ok = courses_api.process_get_request(
            {"action": action, "homework_id": homework_id, **request.args}
        )
    else:
        response, ok = courses_api.process_post_request(
            {"action": action, "homework_id": homework_id, **request.args}
        )
    if ok:
        return json.dumps({"response": response})
    else:
        return json.dumps({"error": response})


@app.route('/groups/<action>', methods=["GET"])
def group_action(action):
    if "token" not in request.args:
        abort(403)
    response, ok = groups_api.process_get_request(
        {"action": action, **request.args}
    )
    if ok:
        return json.dumps({"response": response})
    else:
        return json.dumps({"error": response})


profile_api = ProfileAPI(sessions_manager)
app.route("/profile", methods=["GET", "POST"])(create_api_handler(profile_api, "profile_methods"))
courses_api = CoursesAPI(sessions_manager)
app.route("/courses", methods=["GET", "POST"])(create_api_handler(courses_api, "course_methods"))
groups_api = GroupsAPI(sessions_manager)
app.route("/groups", methods=["GET"])(create_api_handler(groups_api, "group_methods"))

if __name__ == "__main__":
    app.run()
