import pytest
from unittest.mock import patch, MagicMock
from llm_helper import LLM_MODEL_NAME
from search_agent import get_search_agent

# -----------------------------------------------------------------------------
# Test: get_search_agent should correctly create an agent using the specified model.
# -----------------------------------------------------------------------------
def test_get_search_agent_with_provider():
    """
    Test that get_search_agent uses the given provider and passes the correct model
    to the Agent constructor.
    """
    # Mock get_model to avoid real model instantiation
    with patch("search_agent.get_model") as mock_get_model, \
         patch("search_agent.Agent") as mock_agent:
        fake_model = MagicMock(name="fake_llm_model")
        mock_get_model.return_value = fake_model
        result = get_search_agent(LLM_MODEL_NAME.GEMINI)
        # Ensure get_model was called with the right provider
        mock_get_model.assert_called_once_with(LLM_MODEL_NAME.GEMINI)
        # Ensure Agent was created with our fake model
        mock_agent.assert_called_once()
        assert result == mock_agent.return_value

# -----------------------------------------------------------------------------
# Test: get_search_agent fails if not given a valid LLM_MODEL_NAME.
# -----------------------------------------------------------------------------
def test_get_search_agent_type_error():
    """
    Test that get_search_agent raises a TypeError if the provider is not an enum.
    """
    with pytest.raises(TypeError):
        get_search_agent("OPENAI")  # Not an enum; should fail