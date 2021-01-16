from elms.api.domain_api.domain_api import DomainAPI


class ProfileAPI(DomainAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process_get_request(self, request_queries, *args, **kwargs):
        if request_queries["action"] == "get_profile_info":
            if "profile_id" not in request_queries:
                return "No profile id specified", False
            return self.sessions_manager.get_profile_info(int(request_queries["profile_id"]), request_queries["token"])
        else:
            return f"Unsopported action {request_queries['action']}", False

    def process_post_request(self, request_queries, *args, **kwargs):
        if request_queries["action"] == "set_profile_info":
            if "field" not in request_queries:
                return "You must specify field to set", False
            if "data" not in request_queries:
                return f"You must specify data to set for field {request_queries['field']}"
            return self.sessions_manager.set_profile_info(
                request_queries["data"], request_queries["token"], request_queries["field"]
            )
        else:
            return f"Unsopported action {request_queries['action']}", False
