"""LLM service that supports multiple providers (OpenAI, Google Gemini)."""

from typing import Union, Optional
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from ..core.config import settings

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False


class LLMService:
    """Service for managing LLM instances across different providers."""
    
    @staticmethod
    def get_llm(
        model_name: Optional[str] = None,
        provider: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> BaseChatModel:
        """
        Get an LLM instance based on the provider and model.
        
        Args:
            model_name: Model name (e.g., "gpt-4o", "gemini-2.0-flash-lite")
            provider: Provider name ("openai" or "google")
            temperature: Model temperature
            max_tokens: Maximum tokens
            
        Returns:
            BaseChatModel: Configured LLM instance
        """
        # Use settings defaults if not provided
        model_name = model_name or settings.model_name
        provider = provider or settings.model_provider
        temperature = temperature if temperature is not None else settings.temperature
        max_tokens = max_tokens or settings.max_tokens
        
        # Auto-detect provider based on model name if not specified
        if provider == "auto" or (provider == "openai" and model_name.startswith("gemini")):
            provider = LLMService._detect_provider(model_name)
        
        if provider == "google":
            return LLMService._get_google_llm(model_name, temperature, max_tokens)
        elif provider == "openai":
            return LLMService._get_openai_llm(model_name, temperature, max_tokens)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    @staticmethod
    def _detect_provider(model_name: str) -> str:
        """Auto-detect provider based on model name."""
        if model_name.startswith("gemini"):
            return "google"
        elif model_name.startswith(("gpt-", "text-", "davinci", "curie", "babbage", "ada")):
            return "openai"
        else:
            # Default to OpenAI for unknown models
            return "openai"
    
    @staticmethod
    def _get_openai_llm(model_name: str, temperature: float, max_tokens: int) -> ChatOpenAI:
        """Get OpenAI LLM instance."""
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key is required for OpenAI models")
        
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=settings.openai_api_key,
        )
    
    @staticmethod
    def _get_google_llm(
        model_name: str, 
        temperature: float, 
        max_tokens: int
    ) -> "ChatGoogleGenerativeAI":
        """Get Google Gemini LLM instance."""
        if not GOOGLE_AVAILABLE:
            raise ImportError(
                "langchain-google-genai is required for Google models. "
                "Install it with: pip install langchain-google-genai"
            )
        
        if not settings.google_api_key:
            raise ValueError("Google API key is required for Gemini models")
        
        # Map model names to Google's naming convention
        google_model_map = {
            "gemini-2.0-flash-lite": "gemini-2.0-flash-lite",
            "gemini-2.0-flash": "gemini-2.0-flash",
            "gemini-1.5-pro": "gemini-1.5-pro",
            "gemini-1.5-flash": "gemini-1.5-flash",
            "gemini-pro": "gemini-pro",
        }
        
        google_model_name = google_model_map.get(model_name, model_name)
        
        return ChatGoogleGenerativeAI(
            model=google_model_name,
            temperature=temperature,
            max_output_tokens=max_tokens,
            google_api_key=settings.google_api_key,
        )
    
    @staticmethod
    def list_available_models() -> dict:
        """List available models by provider."""
        models = {
            "openai": [
                "gpt-4o",
                "gpt-4o-mini", 
                "gpt-4-turbo",
                "gpt-4",
                "gpt-3.5-turbo",
            ],
            "google": [
                "gemini-2.0-flash-lite",
                "gemini-2.0-flash",
                "gemini-1.5-pro",
                "gemini-1.5-flash",
                "gemini-pro",
            ] if GOOGLE_AVAILABLE else []
        }
        
        return models
    
    @staticmethod
    def is_model_available(model_name: str, provider: str) -> bool:
        """Check if a model is available for a given provider."""
        available_models = LLMService.list_available_models()
        return model_name in available_models.get(provider, [])
    
    @staticmethod
    def validate_configuration(model_name: str, provider: str) -> tuple[bool, str]:
        """
        Validate LLM configuration.
        
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            # Check if provider is supported
            if provider not in ["openai", "google"]:
                return False, f"Unsupported provider: {provider}"
            
            # Check API key availability
            if provider == "openai" and not settings.openai_api_key:
                return False, "OpenAI API key is required"
            
            if provider == "google":
                if not GOOGLE_AVAILABLE:
                    return False, "langchain-google-genai package is not installed"
                if not settings.google_api_key:
                    return False, "Google API key is required"
            
            # Check model availability
            if not LLMService.is_model_available(model_name, provider):
                available = LLMService.list_available_models()[provider]
                return False, f"Model {model_name} not available for {provider}. Available: {available}"
            
            return True, "Configuration is valid"
            
        except Exception as e:
            return False, f"Configuration validation error: {str(e)}"
