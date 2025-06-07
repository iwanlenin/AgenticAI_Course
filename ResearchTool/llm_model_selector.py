import os
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel
from llm_helper import LLM_MODEL_NAME, LLM_BASE_URL
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# llm_model_selector.py
# Helper to select and instantiate an OpenAIChatCompletionsModel.
# - Reads API key and base URL from environment variables using a naming convention.
# - Falls back to OPENAI if a key is missing.
# - Enforces enum type for clarity and safety.
# ---------------------------------------------------------------------------

def get_model(provider: LLM_MODEL_NAME) -> OpenAIChatCompletionsModel:
    """
    Selects and instantiates a chat model for the given provider.
    - Reads <PROVIDER>_API_KEY and <PROVIDER>_URL from environment.
    - Falls back to OPENAI if API key is missing.
    - Only accepts LLM_MODEL_NAME enums.
    """
    # Type safety: Only allow enum, never a string.
    if not isinstance(provider, LLM_MODEL_NAME):
        raise TypeError("provider must be a LLM_MODEL_NAME enum value")

    # Fetch provider credentials and base URL.
    key = os.getenv(f"{provider.name}_API_KEY")
    url = getattr(LLM_BASE_URL, f"{provider.name}_URL", LLM_BASE_URL.OPENAI_URL).value
    model = getattr(LLM_MODEL_NAME, f"{provider.name}" , LLM_MODEL_NAME.OPENAI).value
  
    # Fallback: If key is missing, switch to OpenAI defaults.
    if not key:
        key = os.getenv("OPENAI_API_KEY")
        url = LLM_BASE_URL.OPENAI_URL.value
        model = LLM_MODEL_NAME.OPENAI.value

    # Instantiate the async client and model wrapper.
    client = AsyncOpenAI(api_key=key, base_url=url)
    model = OpenAIChatCompletionsModel(model=model, openai_client=client)
    return model