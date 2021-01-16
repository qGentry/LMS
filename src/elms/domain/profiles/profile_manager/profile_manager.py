from abc import ABC, abstractmethod


class ProfileManager(ABC):

    @abstractmethod
    def get_full_info(self, id: int, allowed_fields: set):
        pass

    @abstractmethod
    def set_phone(self, phone: str, profile_id: int):
        pass

    @abstractmethod
    def set_city(self, city: str, profile_id: int):
        pass

    @abstractmethod
    def set_about(self, about: str, profile_id: int):
        pass

    @abstractmethod
    def set_vk_link(self, vk_link: str, profile_id: int):
        pass

    @abstractmethod
    def set_instagram_link(self, instagram_link: str, profile_id: int):
        pass

    @abstractmethod
    def set_linkedin_link(self, linkedin_link: str, profile_id: int):
        pass

    @abstractmethod
    def set_facebook_link(self, facebook_link: str, profile_id: int):
        pass
