from pydantic import BaseSettings

class Settings(BaseSettings):
    db_username: str
    db_password: str
    db_hostname: str
    db_port: int
    db_name: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_token_expire_minutes: int

    class Config:
        env_file = '.env'

settings = Settings()

