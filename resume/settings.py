import os
from pathlib import Path
import dotenv
from pydantic_settings import BaseSettings

PROJECT_DIR = Path(__file__).resolve().parent
LOG_DIR = os.path.join(os.environ.get("LOG_DIR", PROJECT_DIR), "log")
dotenv.load_dotenv()

class Settings(BaseSettings):
    VERSION: str = "0.0.1"
    APP_NAME: str = "resume_gen"

    MYSQL_HOST: str = os.getenv('MYSQL_HOST')
    MYSQL_USERNAME: str = os.getenv('MYSQL_USERNAME')
    MYSQL_PASSWORD: str = os.getenv('MYSQL_PASSWORD')
    MYSQL_PORT: str = os.getenv('MYSQL_PORT')
    MYSQL_DATABASE: str = os.getenv('MYSQL_DATABASE')

    SQLITE_DATABASE_PATH: str = os.getenv('SQLITE_DATABASE_PATH')
    SQLITE_DATABASE: str = os.getenv('SQLITE_DATABASE')

    ACTIVE_DATABASE: str = os.getenv('DATABASE_TYPE')


settings = Settings()
YAML_NAME: str = "service.yaml"
SERVICE_YAML_PATH = os.path.join(PROJECT_DIR.parent, YAML_NAME)
