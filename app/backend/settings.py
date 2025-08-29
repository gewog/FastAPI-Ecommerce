"""
Этот модуль предоставляет класс `Settings`, который загружает параметры подключения
к базе данных из переменных окружения (файл `.env`) и формирует строку подключения
в формате, совместимом с SQLAlchemy и asyncpg.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Класс для загрузки и управления настройками приложения из переменных окружения.
    Атрибуты:
        DB_USER (str): Имя пользователя базы данных.
        DB_PASS (str): Пароль пользователя базы данных.
        DB_PORT (int): Порт, по которому доступна база данных.
        DB_HOST (str): Хост (адрес сервера) базы данных.
        DB_NAME (str): Название базы данных.
    """
    DB_USER: str
    DB_PASS: str
    DB_PORT: int
    DB_HOST: str
    DB_NAME: str
    
    @property
    def get_path(self):
        """
        :return: str: Строка подключения в формате:
                 `postgresql+asyncpg://<DB_USER>:<DB_PASS>@<DB_HOST>:<DB_PORT>/<DB_NAME>`
        """
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file="./.env",  # Путь к файлу с переменными окружения
        extra="ignore"  # Игнорировать лишние переменные в .env
    )

setting = Settings()