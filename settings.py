import os

from dotenv import load_dotenv

load_dotenv()


def read_bool(value: str) -> bool:
    return value.lower() in ("1", "true")


def read_list(value: str) -> list[str]:
    return value.split(",")


APP_ENV = os.environ["APP_ENV"]
APP_HOST = os.environ["APP_HOST"]
APP_PORT = int(os.environ["APP_PORT"])

CODE_HOTRELOAD = read_bool(os.environ["CODE_HOTRELOAD"])

DB_DIALECT = os.environ["DB_DIALECT"]
DB_USER = os.environ["DB_USER"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = int(os.environ["DB_PORT"])
DB_NAME = os.environ["DB_NAME"]
DB_DRIVER = os.environ["DB_DRIVER"]
DB_PASS = os.environ["DB_PASS"]
INITIALLY_AVAILABLE_DB = os.environ["INITIALLY_AVAILABLE_DB"]

REDIS_USER = os.environ.get("REDIS_USER")
REDIS_PASS = os.environ.get("REDIS_PASS")
REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = int(os.environ["REDIS_PORT"])
REDIS_DB = int(os.environ["REDIS_DB"])
REDIS_USE_SSL = read_bool(os.environ["REDIS_USE_SSL"])

ALLOWED_LAZER_CLIENT_IDS = read_list(os.environ["ALLOWED_LAZER_CLIENT_IDS"])
ALLOWED_LAZER_CLIENT_SECRETS = read_list(os.environ["ALLOWED_LAZER_CLIENT_SECRETS"])

OAUTH_ACCESS_TOKEN_VALIDITY_SECONDS = int(
    os.environ["OAUTH_ACCESS_TOKEN_VALIDITY_SECONDS"],
)
