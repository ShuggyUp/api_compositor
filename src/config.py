from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServersSettings(BaseSettings):
    """
    Настройки сервера
    """

    host: str = Field(default="localhost")
    port: int = Field(default=8000)
    vlp_service_host: str = Field(default="localhost")
    vlp_service_port: int = Field(default=8001)
    ipr_service_host: str = Field(default="localhost")
    ipr_service_port: int = Field(default=8002)
    nodal_analysis_host: str = Field(default="localhost")
    nodal_analysis_port: int = Field(default=8003)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="UTF-8")


server_settings = ServersSettings()
