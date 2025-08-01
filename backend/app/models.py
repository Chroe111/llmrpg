from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any


class EntityType:
    GIRL = "girl"
    DEMON = "demon"
    STONE_MOMUMENT = "stone_momument"
    TREASURE_CHEST = "treasure_chest"
    TREASURE_CHEST_KEY = "treasure_chest_key"
    MAGIC_SWORD = "magic_sword"


class Session:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.chapter = 1
        self.flag = {
            EntityType.GIRL: False,
            EntityType.STONE_MOMUMENT: False,
            EntityType.TREASURE_CHEST: False,
            EntityType.TREASURE_CHEST_KEY: False,
            EntityType.MAGIC_SWORD: False
        }
