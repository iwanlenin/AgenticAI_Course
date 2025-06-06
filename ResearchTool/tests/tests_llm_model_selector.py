# tests_llm_model_selector.py

import os
import pytest
from unittest.mock import patch, MagicMock
from llm_helper import LLM_MODEL_NAME, LLM_BASE_URL
from llm_model_selector import get_model

# ------------------------------------------------------------------------------
# Test: get_model returns a model with OpenAI settings if OPENAI is chosen.
# Assumption:
#   - The function reads OPENAI_API_KEY and OPENAI_URL from environment.
# Setup:
#   - Set OPENAI_API_KEY for this test.
# Expectation:
#   - AsyncOpenAI and OpenAIChatCompletionsModel are called with the correct parameters.
# ------------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_get_model_openai(monkeypatch):
    # Set OPENAI_API_KEY in the environment for this test.
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    # Patch the client and model wrapper to avoid real API calls.
    with patch("llm_model_selector.AsyncOpenAI") as mock_client, \
         patch("llm_model_selector.OpenAIChatCompletionsModel") as mock_model:
        mock_client.return_value = MagicMock(name="openai_client")
        mock_model.return_value = MagicMock(name="model_instance")
        model = await get_model(LLM_MODEL_NAME.OPENAI)
    # The client should be initialized with our test API key and OpenAI base URL.
    mock_client.assert_called_once_with(
        api_key="test-key",
        base_url=LLM_BASE_URL.OPENAI_URL.value
    )
    # The model wrapper should be initialized with correct model name and client.
    mock_model.assert_called_once_with(
        model=LLM_MODEL_NAME.OPENAI.value,
        openai_client=mock_client.return_value
    )
    # The function should return our mocked model instance.
    assert model is mock_model.return_value

# ------------------------------------------------------------------------------
# Test: get_model returns a Gemini model with Gemini settings if GEMINI is chosen.
# Assumption:
#   - The function reads GEMINI_API_KEY and GEMINI_URL from environment.
# Setup:
#   - Set GEMINI_API_KEY for this test.
# Expectation:
#   - AsyncOpenAI and model wrapper are called with Gemini's key and URL.
# ------------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_get_model_gemini(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "gemini-key")
    with patch("llm_model_selector.AsyncOpenAI") as mock_client, \
         patch("llm_model_selector.OpenAIChatCompletionsModel") as mock_model:
        mock_client.return_value = MagicMock(name="gemini_client")
        mock_model.return_value = MagicMock(name="model_instance")
        model = await get_model(LLM_MODEL_NAME.GEMINI)
    mock_client.assert_called_once_with(
        api_key="gemini-key",
        base_url=getattr(LLM_BASE_URL, "GEMINI_URL").value
    )
    mock_model.assert_called_once_with(
        model=LLM_MODEL_NAME.GEMINI.value,
        openai_client=mock_client.return_value
    )
    assert model is mock_model.return_value

# ------------------------------------------------------------------------------
# Test: get_model falls back to OpenAI if provider's API key is missing.
# Assumption:
#   - If the selected provider's key is missing, function uses OpenAI's key and URL.
# Setup:
#   - Ensure GROK_API_KEY is not set, set OPENAI_API_KEY.
# Expectation:
#   - Function returns a model with OpenAI settings.
# ------------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_fallback_to_openai(monkeypatch):
    monkeypatch.delenv("GROK_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "openai-fallback")
    with patch("llm_model_selector.AsyncOpenAI") as mock_client, \
         patch("llm_model_selector.OpenAIChatCompletionsModel") as mock_model:
        mock_client.return_value = MagicMock(name="openai_client")
        mock_model.return_value = MagicMock(name="model_instance")
        # Simulate GROK, but GROK_API_KEY missing.
        model = await get_model(LLM_MODEL_NAME.GROK)
    # Should use OpenAI settings.
    mock_client.assert_called_once_with(
        api_key="openai-fallback",
        base_url=LLM_BASE_URL.OPENAI_URL.value
    )
    mock_model.assert_called_once_with(
        model=LLM_MODEL_NAME.OPENAI.value,
        openai_client=mock_client.return_value
    )

# ------------------------------------------------------------------------------
# Test: get_model raises TypeError if input is not an LLM_MODEL_NAME enum.
# Assumption:
#   - Function only accepts LLM_MODEL_NAME, not string.
# Setup:
#   - Call with string.
# Expectation:
#   - TypeError is raised.
# ------------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_type_guard():
    with pytest.raises(TypeError):
        await get_model("OPENAI")  # Not an enum member!