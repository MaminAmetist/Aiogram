from __future__ import annotations
from dataclasses import dataclass
from environs import Env  # библиотека для хранения скрытых данных


@dataclass
class TGBot:
    token: str


@dataclass
class Config:
    tg_bot: TGBot


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)
    return Config(tg_bot=TGBot(token=env('API')))
