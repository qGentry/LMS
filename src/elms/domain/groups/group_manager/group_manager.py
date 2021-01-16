from abc import ABC, abstractmethod


class GroupManager(ABC):

    @abstractmethod
    def get_groupmates(self, profile_id: int):
        pass
