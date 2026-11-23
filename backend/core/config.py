from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    app_name: str = "Binary Trading Expert"
    frontend_origins: str = "http://localhost:5173"
    database_url: str = "sqlite:///./binary_expert.db"
    finnhub_api_key: str = ""
    twelve_data_api_key: str = ""
    max_tick_age_seconds: int = 10
    enable_otc: bool = False
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins(self):
        return [x.strip() for x in self.frontend_origins.split(",") if x.strip()]

settings = Settings()
