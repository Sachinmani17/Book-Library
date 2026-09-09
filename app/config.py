from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
MONGODB_URI: str
DATABASE_NAME: str = "library_db"
COLLECTION_NAME: str = "books"
PORT: int = 8000
model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
settings = Settings()
