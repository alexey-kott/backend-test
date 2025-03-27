from databases import DatabaseURL
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine.url import URL


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")


class _DatabaseSettings(_Settings):
    USER: str = ""
    PASSWORD: str = ""
    HOST: str = ""
    PORT: int = 5432
    DB_NAME: str = ""  # db name

    DRIVER: str = "postgresql+asyncpg"
    AUTOCOMMIT: bool = False
    ECHO: bool = False  # for debugging

    @property
    def DSN(self) -> DatabaseURL:
        return DatabaseURL(URL.create(self.DRIVER,
                                      self.USER,
                                      self.PASSWORD,
                                      self.HOST, self.PORT,
                                      self.DB_NAME).render_as_string(hide_password=False))

    # Не очень правильно, что в энвах мы используем специфичный префикс POSTGRES_. Что, если мы
    # вдруг решим сменить БД на, допустим, MySQL? Лучше использовать общий префикс DB_.
    model_config = SettingsConfigDict(env_prefix='POSTGRES_')

db_settings = _DatabaseSettings()
