from elms.api.domain_api.domain_api import DomainAPI


class GroupsAPI(DomainAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process_get_request(self, request_queries, *args, **kwargs):
        if request_queries["action"] == "get_groupmates":
            result = self.sessions_manager.get_groupmates(
                request_queries["token"]
            )
            return result
        else:
            return f"Unsupported action {request_queries['action']}", False

    def process_post_request(self, request_queries, *args, **kwargs):
        pass
