import sqlite3
from typing import Tuple, Union
import re

from elms.domain.profiles.profile_manager.profile_manager import ProfileManager


phone_regex = re.compile(r"(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}")


class SqlProfileManager(ProfileManager):

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.cursor = conn.cursor()

    @staticmethod
    def _check_phone_ok(phone):
        return phone_regex.fullmatch(phone)

    def set_phone(self, phone: str, profile_id: int) -> Tuple[str, bool]:
        if not self._check_phone_ok(phone):
            return "Incorrect phone number format", False
        self.cursor.execute("UPDATE profiles SET phone_number = ? WHERE profile_id = ?",
                            (phone, profile_id))
        self.conn.commit()
        if self.cursor.rowcount:
            return "OK", True
        else:
            return "Couldn't change about", False

    def set_city(self, city: str, profile_id: int) -> Tuple[str, bool]:
        self.cursor.execute("UPDATE profiles SET city = ? WHERE profile_id = ?",
                            (city, profile_id))
        self.conn.commit()
        if self.cursor.rowcount:
            return "OK", True
        else:
            return "Couldn't change city", False

    def set_about(self, about: str, profile_id: int) -> Tuple[str, bool]:
        self.cursor.execute("UPDATE profiles SET about = ? WHERE profile_id = ?",
                            (about, profile_id))
        self.conn.commit()
        if self.cursor.rowcount:
            return "OK", True
        else:
            return "Couldn't change about", False

    def get_full_info(self, profile_id: int, allowed_fields: set) -> Tuple[Union[str, dict], bool]:
        self.cursor.execute("SELECT * from profiles WHERE profile_id = ?",
                            (profile_id,))
        res = self.cursor.fetchone()
        if res is None:
            return "Profile id doesn't exists", False
        else:
            return {key: value for key, value in res.items() if key in allowed_fields}, True

    def set_linkedin_link(self, linkedin_link: str, profile_id: int) -> Tuple[str, bool]:
        if "linkedin.com" in linkedin_link:
            self.cursor.execute("UPDATE profiles SET link_linkedin = ? WHERE profile_id = ?",
                                (linkedin_link, profile_id))
            self.conn.commit()
            if self.cursor.rowcount:
                return "OK", True
            else:
                return "Couldn't change link", False
        else:
            return "Invalid LinkedIn link", False

    def set_facebook_link(self, facebook_link: str, profile_id: int) -> Tuple[str, bool]:
        if "facebook.com" in facebook_link:
            self.cursor.execute("UPDATE profiles SET link_facebook = ? WHERE profile_id = ?",
                                (facebook_link, profile_id))
            self.conn.commit()
            if self.cursor.rowcount:
                return "OK", True
            else:
                return "Couldn't change link", False
        else:
            return "Invalid Facebook link", False

    def set_vk_link(self, vk_link: str, profile_id: int) -> Tuple[str, bool]:
        if "vk.com" in vk_link:
            self.cursor.execute("UPDATE profiles SET link_vk = ? WHERE profile_id = ?",
                                (vk_link, profile_id))
            self.conn.commit()
            if self.cursor.rowcount:
                return "OK", True
            else:
                return "Couldn't change link", False
        else:
            return "Invalid VK link", False

    def set_instagram_link(self, instagram_link: str, profile_id: int) -> Tuple[str, bool]:
        if "instagram.com" in instagram_link:
            self.cursor.execute("UPDATE profiles SET link_instagram = ? WHERE profile_id = ?",
                                (instagram_link, profile_id))
            self.conn.commit()
            if self.cursor.rowcount:
                return "OK", True
            else:
                return "Couldn't change link", False
        else:
            return "Invalid Instagram link", False
