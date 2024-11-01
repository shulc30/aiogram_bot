from dataclasses import dataclass

from environs import Env 

@dataclass
class TgBot:
    token: str # Токен для доступа к тг боту
    admin_ids: list[int] # Список id администраторов

@dataclass
class Config:
    tg_bot: TgBot

# Создадим функцию, которая будет читать файл .env т возвращать
# экземпляр класса Config с заполненными полями token  и admin_ids
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS')))
        )
    )
