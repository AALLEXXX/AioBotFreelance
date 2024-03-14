from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int


@dataclass
class Settings:
    bots: Bots
    DB_PATH: str
    P2P_TOKEN: str
    REDIS_HOST: str
    REDIS_PORT: str

    @property
    def DATABASE_URL(self) -> str:
        return f"sqlite+aiosqlite:///{self.DB_PATH}"


def get_settings(path: str) -> Settings:
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(bot_token=env.str("TOKEN"), admin_id=env.int("ADMIN_ID")),
        DB_PATH=env.str("DB_PATH"),
        P2P_TOKEN=env.str("P2P_TOKEN"),
        REDIS_HOST=env.str("REDIS_HOST"),
        REDIS_PORT=env.str("REDIS_PORT"),
        # DB_HOST=env.str('DB_HOST'),
        # DB_NAME=env.str('DB_NAME'),
        # DB_PASS=env.str('DB_PASS'),
        # DB_PORT=env.str('DB_PORT'),
        # DB_USER=env.str('DB_USER')
    )


settings: Settings = get_settings("input")
