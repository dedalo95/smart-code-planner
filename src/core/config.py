"""Configuration management for the coder assistant."""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings."""

    # API Keys
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    google_api_key: Optional[str] = Field(None, env="GOOGLE_API_KEY")
    langchain_api_key: Optional[str] = Field(None, env="LANGCHAIN_API_KEY")

    # LangChain Settings
    langchain_tracing_v2: bool = Field(default=False, env="LANGCHAIN_TRACING_V2")
    langchain_project: str = Field(default="smart-code-planner", env="LANGCHAIN_PROJECT")

    # Model Settings
    model_name: str = Field(default="gpt-4o", env="MODEL_NAME")
    model_provider: str = Field(default="openai", env="MODEL_PROVIDER")  # openai, google
    temperature: float = Field(default=0.3, env="TEMPERATURE")
    max_tokens: int = Field(default=2000, env="MAX_TOKENS")

    # Application Settings
    max_analysis_depth: int = Field(default=3, env="MAX_ANALYSIS_DEPTH")
    complexity_threshold: float = Field(default=0.7, env="COMPLEXITY_THRESHOLD")

    # Streamlit Settings
    streamlit_port: int = Field(default=8501, env="STREAMLIT_PORT")
    streamlit_host: str = Field(default="0.0.0.0", env="STREAMLIT_HOST")

    # Development Settings
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"  # Ignore extra fields
    }


# Global settings instance
try:
    settings = Settings()
except Exception as e:
    # Fallback settings if environment variables are missing
    print(f"Warning: Could not load settings from environment: {e}")
    settings = Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        langchain_api_key=os.getenv("LANGCHAIN_API_KEY"),
        langchain_tracing_v2=os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true",
        langchain_project=os.getenv("LANGCHAIN_PROJECT", "smart-code-planner"),
        model_name=os.getenv("MODEL_NAME", "gpt-4o"),
        model_provider=os.getenv("MODEL_PROVIDER", "openai"),
        temperature=float(os.getenv("TEMPERATURE", "0.3")),
        max_tokens=int(os.getenv("MAX_TOKENS", "2000")),
        max_analysis_depth=int(os.getenv("MAX_ANALYSIS_DEPTH", "3")),
        complexity_threshold=float(os.getenv("COMPLEXITY_THRESHOLD", "0.7")),
        streamlit_port=int(os.getenv("STREAMLIT_PORT", "8501")),
        streamlit_host=os.getenv("STREAMLIT_HOST", "0.0.0.0"),
    )


def get_prompts_dir() -> str:
    """Get the prompts directory path."""
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "prompts")


def load_prompt(prompt_name: str) -> str:
    """Load a prompt from the prompts directory."""
    prompts_dir = get_prompts_dir()
    prompt_path = os.path.join(prompts_dir, f"{prompt_name}.txt")

    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    except Exception as e:
        raise Exception(f"Error loading prompt {prompt_name}: {str(e)}")
