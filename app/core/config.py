from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    DATABASE_URL: str
    SECRET_KEY: str
    USER_NAME: str
    PASS_WORD: str
    project_name: str = "Credit Information API"


settings = Settings()