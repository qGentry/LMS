from abc import ABC, abstractmethod
from typing import Tuple, Union


class LoginHandler(ABC):

    @abstractmethod
    def register(self, auth_code: str, email: str, password: str) -> Tuple[str, bool]:
        pass

    @abstractmethod
    def login(self, email: str, password: str) -> Tuple[str, Union[int, None], bool]:
        pass

    @staticmethod
    @abstractmethod
    def _get_auth_token():
        pass

    @abstractmethod
    def change_password(self, new_password: str, old_password: str, email: str):
        pass
