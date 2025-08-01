from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any
    from .models import Session

from .models import EntityType


# function definition
def scene_info(chapter: int) -> dict:
    response = {"chapter": f"{chapter}"}

    if chapter == 1:
        response["story_line"] = [
            "目が覚めるとそこは遺跡だった。",
            "目の前の少女が話しかけてくる。*ここは悪魔が封印されている遺跡である。しかしその封印が弱まっている。封印を施すため、手を貸してほしい。*"
        ]
        response["scene_info"] = {
            "ruin": {
                "detail": [
                    "荒廃した古代遺跡。朽ちた柱やひび割れた壁が目に入る。",
                    "先に進むことのできる通路が見える。奥から禍々しい雰囲気を感じる。"
                ],
                "notice": "雰囲気から数千年前に建てられたものだと推測できる。"
            }
        }
        response["story_progress_conditions"] = "少女とのやり取りを終了したうえで、奥に進む"
    
    elif chapter == 2:
        response["story_line"] = [
            "通路を進むと開けた場所に出た。",
            "ここで情報を得ることができそうだ。"
        ]
        response["scene_info"] = {
            "open_place": {
                "detail": "広々としており、声が反響する。禍々しい雰囲気が濃くなっている。",
                "entities": ["宝箱", "苔むした石碑"]
            }
        }
        response["story_progress_conditions"] = "魔法の剣を入手し、先に進む"
    
    elif chapter == 3:
        response["story_line"] = [
            "探索を終えた主人公 (と少女) は最奥の間へと進む。",
            "ちょうど封印がほどけ、悪魔が顕現する。"
        ]
        response["scene_info"] = {
            "innermost_place": {
                "detail": [
                    "禍々しい空気が充満している部屋。",
                    "中央には魔法陣や呪文らしきものが描かれているが、その半分以上が途切れてしまっている。"
                ]
            }
        }
        response["story_progress_conditions"] = [
            "封印の呪文を唱える (封印エンディング)",
            "悪魔に攻撃を2回成功させる (討伐エンディング)"
        ]
    
    elif chapter == 4:
        response["story_line"] = {
            "封印エンディング": [
                "悪魔は元通り封印された。",
                "少女が語りかける。*またいつか封印が綻びる時が来る。その時はまた手を貸してほしい*"
            ],
            "討伐エンディング": [
                "悪魔の息の根が止まり、脅威を退けることに成功した。",
                "少女が語りかける。*ありがとう。これで禍根を断つことができた*"
            ]
        }
    
    return response


def get_current_scene_info(session: Session) -> dict:
    return scene_info(session.chapter)


def get_next_scene_info(session: Session) -> dict:
    return scene_info(session.chapter + 1)


def get_an_entity_info(session: Session, entity_type: str) -> dict[str, list[str] | str]:
    response = {"entity_type": entity_type}

    if entity_type == EntityType.GIRL:
        response["detail"] = ["見た目は14~16歳くらいの女の子。白い衣を身にまとい、フードを深々とかぶっている。"]
        if session.chapter == 1:
            response["detail"].append("基本的に寡黙だが、こちらから話しかけると受け答えをしてくれる。ただし自分の正体やこの遺跡、封印の詳細については口を閉ざし**頑なに**答えようとしない。")
            response["secret_info"] = [
                "悪魔族の末裔の巫女。数百年に一度解ける封印を再度施す使命を引き受けている。"
            ]
        elif session.chapter == 2:
            response["detail"].append("基本的に寡黙だが、こちらから話しかけると受け答えをしてくれる。ただし自分の正体については口を閉ざし**頑なに**答えようとしない。")
            response["notice"] = "時折寂しそうな表情を見せる。"
            response["secret_info"] = [
                "悪魔族の末裔の巫女。数百年に一度解ける封印を再度施す使命を引き受けている。",
                "幼名はセレナ。"
            ]
        else:
            response["notice"] = "表情に緊張感がにじむ。"
            response["detail"].extend([
                "悪魔族の末裔の巫女。数百年に一度解ける封印を再度施す使命を引き受けている。",
                "幼名はセレナ。"
            ])

    elif entity_type == EntityType.TREASURE_CHEST:
        response["detail"] = "銀製の宝箱。鍵がかかっている。中身を取り出すには鍵を見つける必要がある。"
        response["additional_detail"] = {
            "content": "開錠した場合、魔法の剣を入手できる。",
            "magic_sword": get_an_entity_info(session, EntityType.MAGIC_SWORD)["detail"]
        }
        
    elif entity_type == EntityType.TREASURE_CHEST_KEY:
        response["detail"] = "錆びついた小さな鍵。一度しか使用できなさそう。"
        response["girl_thinking"] = "宝箱の鍵を開けられそうだ"
        
    elif entity_type == EntityType.STONE_MOMUMENT:
        response["detail"] = "苔むした石碑。不思議な文字が刻まれている。"
        response["girl_thinking"] = "悪魔の封印に関することが記述されている。魔法の剣を掲げて呪文を唱えることで悪魔を封印することができる。呪文は私が知っている。"
    
    elif entity_type == EntityType.MAGIC_SWORD:
        response["detail"] = "刀身が青白く輝く美しい剣。手に持つと不思議な力を感じる。"
        
    elif entity_type == EntityType.DEMON:
        response = {
            "detail": " 禍々しい色と形をした鳥のように見える。人間大。翼で宙に舞っている。",
            "notice": "胸の位置にクリスタルのような部位が見え、おそらくここが弱点であると推測できる。"
        }
        response["girl_thinking"] = "名前が「カイム」であることを知っている。"
    
    else:
        return {
            "state": "reject",
            "system_info": f"エンティティ \"{entity_type}\" は存在しません。"
        }
    
    return response


def get_entity_info(session: Session, entity_types: list[str]) -> list[dict[str, list[str] | str]]:
    return [get_an_entity_info(session, et) for et in entity_types]


def transition_scene(session: Session) -> dict:
    session.chapter += 1
    return {"state": "accept", "system_info": f"シーンを遷移しました。現在のチャプター: {session.chapter}"}


def call_function(session: Session, functions: dict) -> None:
    tool_map = {
        "get_current_scene_info": get_current_scene_info,
        "get_next_scene_info": get_next_scene_info,
        "transition_scene": transition_scene,
        "get_entity_info": get_entity_info
    }
    for name, tool in tool_map.items():
        if name in functions:
            functions[name]["result"] = tool(session, **functions[name]["arguments"])


# schema
def create_function(name: str, description: str, parameters: dict=None) -> dict:
    data = {
        "type": "function",
        "name": name,
        "description": description
    }
    if parameters:
        data["strict"] = True
        data["parameters"] = parameters

    return data


def gettable_info_type(session: Session) -> list[str]:
    if session.chapter == 1:
        return [EntityType.GIRL]
    elif session.chapter == 2:
        data = [EntityType.TREASURE_CHEST, EntityType.STONE_MOMUMENT]
    elif session.chapter == 3:
        data = [EntityType.DEMON]
    
    if session.flag[EntityType.GIRL]:
        data.append(EntityType.GIRL)
    if session.flag[EntityType.TREASURE_CHEST_KEY]:
        data.append(EntityType.TREASURE_CHEST_KEY)
    if session.flag[EntityType.MAGIC_SWORD]:
        data.append(EntityType.MAGIC_SWORD)
    
    return data


def tools(session: Session) -> list:
    data = [
        #create_function(
        #    name="get_current_scene_info", 
        #    description="現在のシーンに関する情報を取得する。"
        #),
        create_function(
            name="get_next_scene_info",
            description="次のシーンに関する情報を取得する。"
        ),
        create_function(
            name="get_entity_info",
            description="シーン描写に必要なエンティティ情報を取得する。",
            parameters={
                "type": "object",
                "properties": {
                    "entity_types": {
                        "type": "array",
                        "description": "取得するエンティティの種類",
                        "items": {
                            "type": "string",
                            "enum": gettable_info_type(session)
                        }
                    }
                },
                "required": ["entity_types"],
                "additionalProperties": False
            }
        ),
        #create_function(
        #    name="transition_scene", 
        #    description="次のシーンへ遷移する。"
        #),
        create_function(
            name="finish_drawing",
            description="現在のゲームを終了する。エンディングあるいは進行不能になったときに実行する。"
        )
    ]

    return data
