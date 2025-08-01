from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .models import Session

import random
import string
import textwrap


def clean(text: str, **kwargs: str) -> str:
    return textwrap.dedent(text.format(**kwargs)).strip()


def generate_session_id(length: int=8, session_list: list[Session]=[]) -> str:
    while True:
        id = "".join(random.choices(string.ascii_letters + string.digits, k=length))
        if id not in session_list:
            return id


def get_session(session_id: str, session_list: list[Session]) -> Session | None:
    for session in session_list:
        if session.session_id == session_id:
            return session
    return None


def close_session(session_id: str, session_list: list[Session]) -> bool:
    for session in session_list:
        if session_id == session_id:
            session_list.remove(session)
            return True
    return False
