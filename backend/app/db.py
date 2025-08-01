from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, Sequence
    from .models import Session as Session

from datetime import datetime as dt
from enum import StrEnum, auto

import sqlmodel
from sqlmodel import SQLModel, Field


class LogType(StrEnum):
    USER_INPUT = auto()
    LLM_RESPONSE = auto()
    NARRATION = auto()
    FUNCTION_CALL = auto()


class Log(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    session_id: str
    log_type: LogType
    input: str
    output: str | None
    timestamp: dt


_engine = sqlmodel.create_engine("sqlite:///test.db")
SQLModel.metadata.create_all(_engine)


def read_log(session: Session) -> Sequence[Log]:
    with sqlmodel.Session(_engine) as db_session:
        statement = sqlmodel.select(Log).where(Log.session_id == session.session_id)
        return db_session.exec(statement).fetchall()


def message_history(session: Session, narration_role: str="system") -> list[dict[str, str]]:
    logs = read_log(session)
    return [
        {
            "role": "user" if log.log_type == LogType.USER_INPUT else narration_role,
            "content": log.input
        } for log in logs if log.log_type in (LogType.USER_INPUT, LogType.NARRATION)
    ]


def _insert(session: Session, log_type: LogType, input: str, output: str | None=None, timestamp: dt | None=None):
    log = Log(
        session_id=session.session_id,
        log_type=log_type.value,
        input=input,
        output=output,
        timestamp=timestamp or dt.now()
    )

    with sqlmodel.Session(_engine) as db_session:
        db_session.add(log)
        db_session.commit()


def log_user_input(session: Session, action: str):
    _insert(
        session=session,
        log_type=LogType.USER_INPUT,
        input=action
    )


def log_llm_response(session: Session, input: str, response: str) -> None:
    _insert(
        session=session,
        log_type=LogType.LLM_RESPONSE,
        input=input,
        output=response
    )


def log_function_call(session: Session, signature: str, result: dict) -> None:
    _insert(
        session=session,
        log_type=LogType.FUNCTION_CALL,
        input=signature,
        output=str(result)
    )


def log_narration(session: Session, narration: str) -> None:
    _insert(
        session=session,
        log_type=LogType.NARRATION,
        input=narration
    )
