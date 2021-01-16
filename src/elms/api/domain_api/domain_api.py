from abc import ABC, abstractmethod

from elms.presenter.session_manager import SessionsManager


class DomainAPI(ABC):

    def __init__(self, sessions_manager: SessionsManager):
        self.sessions_manager = sessions_manager

    @abstractmethod
    def process_get_request(self, request_queries, *args, **kwargs):
        pass

    @abstractmethod
    def process_post_request(self, request_queries, *args, **kwargs):
        pass
