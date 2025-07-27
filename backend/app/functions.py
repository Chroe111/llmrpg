from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any
    from openai import OpenAI
    from .models import Session

from enum import Enum


def gettable_info_type(session: Session) -> list[str]:
    data = []

    if session.scene == 1:
        data.append("girl")
        return data
    elif session.scene == 2:
        data.append("treasure_chest")
        data.append("stone_momument")
    elif session.scene == 3:
        data.append("demon")
    
    if session.flag["girl"]:
        data.append("girl")
    if session.flag["treasure_chest_key"]:
        data.append("treasure_chest_key")
    if session.flag["magic_dagger"]:
        data.append("maggic_dagger")
    
    return data

    
def changeable_status(session: Session) -> dict[str, Any]:
    data = [
        {
            "type": "function",
            "name": "update_girl_acomponying_state",
            "description": "少女の同行状態を変更する。",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "state": {
                        "type": "boolean",
                        "description": "true: 同行する\nfalse: 別れる"
                    }
                },
                "required": ["state"],
                "additionalProperties": False
            }
        },
    ]

    if session.scene == 2 and session.flag["stone_monument"] == False:
        data.append(
            {
                "type": "function",
                "name": "examine_stone_monument",
                "description": "石碑を調べる。",
                "parameters": {}
            }
        )

    if session.scene == 2 and session.flag["treasure"] == False:
        data.append(
            {
                "type": "function",
                "name": "open_treasure_chest",
                "description": "宝箱を開ける。鍵が必要。",
                "parameters": {}
            }
        )
    
    return data


def tools(session: Session) -> list:
    data = [
        {
            "type": "function",
            "name": "get_info",
            "description": "シーン描写に必要なエンティティ情報を取得する。",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "info_type": {
                        "type": "array",
                        "description": "エンティティの種類",
                        "items": {
                            "type": "string",
                            "enum": gettable_info_type(session)
                        }
                    }
                },
                "required": ["info_type"],
                "additionalProperties": False
            }
        },
        {
            "type": "function",
            "name": "scene_transition",
            "description": "次のシーンへ遷移する。",
            "parameters": {}
        }
    ]

    data.extend(changeable_status(session))
    