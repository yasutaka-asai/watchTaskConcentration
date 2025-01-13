import os
from dataclasses import dataclass

@dataclass
class Settings:
    openai_api_key: str
    task_description: str

def get_settings() -> Settings:
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        task_description=os.getenv("TASK_DESCRIPTION", "指定したタスクを実行中")
    )
