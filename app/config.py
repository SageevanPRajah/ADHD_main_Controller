from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'ADHD Main Gateway Backend'
    app_version: str = '1.0.0'
    body_posture_base_url: str = 'http://localhost:8001'
    eye_tracking_base_url: str = 'http://localhost:8004'
    handwriting_base_url: str = 'http://localhost:8002'
    voice_analysis_base_url: str = 'http://localhost:8003'
    request_timeout_seconds: float = 300.0
    cors_origins: List[str] = Field(default_factory=lambda: ['http://localhost:5173'])


@lru_cache
def get_settings() -> Settings:
    return Settings()
