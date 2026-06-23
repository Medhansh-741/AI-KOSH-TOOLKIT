import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "AIKosh Dataset Quality Evaluation Toolkit"
    API_V1_STR: str = "/api/v1"
    
    # Postgres Database
    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: str = Field(default="postgres")
    POSTGRES_DB: str = Field(default="aikosh_quality")
    POSTGRES_HOST: str = Field(default="postgres")
    POSTGRES_PORT: str = Field(default="5432")
    
    @property
    def DATABASE_URL(self) -> str:
        # Standard synchronous URL for migrations/direct DB calls
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        # Async URL for FastAPI async database operations
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Redis (Broker + Results)
    REDIS_URL: str = Field(default="redis://redis:6379/0")

    # MinIO / S3 Object Storage
    S3_ENDPOINT_URL: str = Field(default="http://minio:9000")
    S3_ACCESS_KEY: str = Field(default="minioadmin")
    S3_SECRET_KEY: str = Field(default="minioadmin")
    S3_BUCKET_NAME: str = Field(default="aikosh-datasets")
    S3_REGION: str = Field(default="us-east-1")

    # Security
    API_KEY_SECRET: str = Field(default="tkt_secret_super_secure_key_12345678")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
