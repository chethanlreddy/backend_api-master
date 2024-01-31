from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secrete_key: str
    algorithm:  str
    access_token_expiry_minutes: int

    class Config:
        env_file = '.env'


setting = Setting()
