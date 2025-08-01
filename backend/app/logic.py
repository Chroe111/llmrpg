from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any

import asyncio
import json

from fastapi import FastAPI, Depends
from openai import AsyncOpenAI
from pydantic import BaseModel

from . import db
from .functions import tools, call_function, get_current_scene_info
from .models import Session
from .utils import clean, generate_session_id, get_session, close_session


app = FastAPI()
openai_client = AsyncOpenAI(api_key="your_api_key")


session_list: list[Session] = []


# logic
async def should_scene_transition(message_history: list, condition: Any) -> tuple[bool, list]:
    class Response(BaseModel):
        result: bool
        reason: str | None
    
    response = await openai_client.responses.parse(
        model="gpt-4o-mini",
        instructions=clean(
            """
            ## instraction
            あなたはテキストベース RPG のコアシステムで、プレイヤーの行動処理を担当しています。
            プレイヤーの行動宣言を基に、シーンの遷移条件を満たしているかどうかを判定し、理由とともに出力してください。
            ## 現在のシーンにおける遷移条件
            {condition}
            """, condition=condition
        ),
        input=message_history,
        text_format=Response
    )
    return response.output_parsed.result, [output.model_dump() for output in response.output]


async def parse_player_action(session: Session, message_history: list, scene_info: Any) -> tuple[list, list]:
    response = await openai_client.responses.create(
        model="gpt-4o",
        instructions=clean(
            """
            ## instraction
            あなたはテキストベース RPG のコアシステムで、プレイヤーの行動処理を担当しています。
            まず、プレイヤーの行動入力を解釈し以下の形式で出力してください。
            ```markdown
            ## プレイヤー行動
            - <プレイヤーの行動 (例: 少女の正体を尋ねる, 悪魔に攻撃を仕掛ける)>
            - <プレイヤーの行動>
            - <プレイヤーの行動>
            ```
            解釈した結果を基に、ストーリー描写に必要な設定や情報を参照するための関数を実行してください。
            ## note
            - 複数呼び出すことができます。
            - シナリオに忠実なストーリー描写を行うため、些細なものでも必要な情報は必ず取得してください。
            ## 現在のシーン情報
            {scene_info}
            """, scene_info=scene_info
        ),
        input=message_history,
        tools=tools(session)
    )
    calling_functions = {
        "get_current_scene_info": {
            "arguments": {}
        }
    }
    for output in response.output:
        if output.type == "function_call":
            calling_functions[output.name] = {
                "arguments": json.loads(output.arguments)
            }
    return calling_functions, [output.model_dump() for output in response.output]


async def progress_user_input(session: Session, message_history: list[dict[str, str]], current_scene_info: dict):
    req1 = asyncio.create_task(
        should_scene_transition(message_history[-2:], current_scene_info["story_progress_conditions"])
    )
    req2 = asyncio.create_task(
        parse_player_action(session, message_history[-2:], current_scene_info)
    )

    res1, res1_raw = await req1
    res2, res2_raw = await req2

    if res1:
        res2["get_next_scene_info"] = {"arguments": {}}
        call_function(session, res2)
        session.chapter += 1
    else:
        call_function(session, res2)
    
    return res2, res1_raw, res2_raw


async def generate_narration(session: Session, refered_info: dict):
    message_history = db.message_history(session, "assistant")
    response = await openai_client.responses.create(
        model="gpt-4o",
        instructions=clean(
            """
            ## instraction
            あなたはテキストベース RPG のストーリー描写システムです。
            与えられたシナリオや設定、およびプレイヤーの入力を基に、続きのストーリーを生成してください。
            ## note
            - こちらかプレイヤー提示は基本的にしない。プレイヤーからの自由な入力を期待する。
            - ただし、プレイヤーが「何をしたらいいかわからない」と思うことがないように、最低限の情報は描写する。
            ## info
            {refered_info}
            """, refered_info=refered_info
        ),
        input=message_history
    )
    narration = response.output_text
    db.log_narration(session, narration)

    return narration, response


# route / endpoint
@app.get("/start")
async def start() -> dict:
    session_id = generate_session_id(session_list=session_list)
    session = Session(session_id)
    session_list.append(session)

    narration = clean(
        """
        冷たい石の床。
        あなたは、そこで目を覚ました。
        見上げると、朽ちた柱とひび割れた壁。 ここは遺跡だ。
        状況が飲み込めず立ち上がると、ふと影が現れる。
        白い衣をまとった、夢げな少女。
        彼女は静かにあなたを見つめ、こう言った。
        「…あの、私のことが、見えますか？」

        彼女の呼びかけに対し、あなたは行動する。
        (チャットで行動やセリフを入力してください)
        """
    )

    db.log_narration(session, narration)

    return {
        "state": "accept", 
        "session_id": session_id,
        "narration": narration
    }


@app.get("/action")
async def action(session_id: str, message: str) -> dict:
    session = get_session(session_id, session_list)
    
    db.log_user_input(session, message)
    message_histoty = db.message_history(session)

    current_scene_info = get_current_scene_info(session)

    calling_functions, res1_raw, res2_raw = await progress_user_input(session, message_histoty, current_scene_info)
    
    narration, res3_raw = await generate_narration(session, calling_functions)

    return {
        "input": message_histoty, 
        "response1": res1_raw, 
        "response2": res2_raw,
        "calling_functions": calling_functions, 
        "response3": res3_raw
    }


@app.get("/session")
async def get_session_info(id: str | None=None) -> dict:
    if id is None:
        return {"state": "reject", "message": "無効なセッション ID です。"}
    return get_session(id, session_list).__dict__
