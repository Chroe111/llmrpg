from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any

import random
import string


class Session:
    session_id_list = []
    
    @classmethod
    def create_session_id(cls, length: int=8) -> str:
        while True:
            id = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            if id not in cls.session_id_list:
                break
        cls.session_id_list.append(id)
        return id

    def __init__(self, session_id: str | None=None):
        if session_id is None:
            self.id = type(self).create_session_id()
        else: 
            self.session_id = session_id
        self.scene = 1
        self.flag = {
            "girl": False,
            "stone_monument": False,
            "treasure_chest": False,
            "treasure_chest_key": False,
            "magic_dagger": False
        }