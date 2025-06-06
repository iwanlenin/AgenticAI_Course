from llm_model_selector import get_model
from llm_helper import LLM_MODEL_NAME
from agents import Agent, ModelSettings, WebSearchTool

# -----------------------------------------------------------------------------
# System prompt for the agent's LLM.
# Used as the "system message" to instruct the language model how to behave.
# -----------------------------------------------------------------------------
INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must be 2-3 paragraphs and less than 300 "
    "words. Capture the main points. Write succinctly, no need to have complete sentences or good "
    "grammar. This will be consumed by someone synthesizing a report, so it's vital you capture the "
    "essence and ignore any fluff. Do not include any additional commentary other than the summary itself."
)

# -----------------------------------------------------------------------------
# Factory function to create a Search Agent using the specified LLM model.
# This allows easy injection of different models (OpenAI, Gemini, etc.)
# -----------------------------------------------------------------------------
def get_search_agent(provider: LLM_MODEL_NAME):
    """
    Creates and returns a configured Search Agent for web search and summarization.

    :param provider: The language model provider to use (must be LLM_MODEL_NAME enum).
    :return: Agent instance configured with the chosen LLM model and web search tool.
    """
    # Get the model instance for the specified provider
    llm_model = get_model(provider)
    # Instantiate and return the agent
    return Agent(
        name="Search agent",
        instructions=INSTRUCTIONS,
        tools=[WebSearchTool(search_context_size="low")],
        model=llm_model,
        model_settings=ModelSettings(tool_choice="required"),
    )

# Example usage:
# agent = get_search_agent(LLM_MODEL_NAME.OPENAI)
# agent = get_search_agent(LLM_MODEL_NAME.GEMINI)

# -----------------------------------------------------------------------------
# Example usage (uncomment as needed)
# -----------------------------------------------------------------------------
# agent = get_search_agent(LLM_MODEL_NAME.OPENAI)
# agent = get_search_agent(LLM_MODEL_NAME.GEMINI)



# # ---------------------------------------------------------------------------
# # Description
# # ---------------------------------------------------------------------------
# """
# Search Agent Module

# This module defines a SearchAgent that performs web searches and generates concise
# summaries of the search results. The agent is designed to be part of a larger
# research pipeline, providing focused and relevant information for report generation.

# The agent:
# - Performs web searches using provided search terms
# - Generates brief, focused summaries (2-3 paragraphs, <300 words)
# - Captures essential information while removing unnecessary details
# """

# # ---------------------------------------------------------------------------
# # Imports
# # ---------------------------------------------------------------------------
# import os
# from openai import OpenAI
# from agents import Agent, WebSearchTool, ModelSettings
# from llm_model_selector import get_model
# from llm_helper import LLM_MODEL_NAME

# # ---------------------------------------------------------------------------
# # Configuration
# # ---------------------------------------------------------------------------
# # The language model to use - using Gemini from environment
# # llm_model_to_use = os.getenv("DEFAULT_OPENAI_MODEL")
# llm_model_to_use = get_model(LLM_MODEL_NAME.GEMINI)


# # System prompt instructions for the language model
# INSTRUCTIONS = (
#     "You are a research assistant. Given a search term, you search the web for that term and "
#     "produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 "
#     "words. Capture the main points. Write succintly, no need to have complete sentences or good "
#     "grammar. This will be consumed by someone synthesizing a report, so its vital you capture the "
#     "essence and ignore any fluff. Do not include any additional commentary other than the summary itself."
# )


# # ---------------------------------------------------------------------------
# # Agent Configuration
# # ---------------------------------------------------------------------------
# search_agent = Agent(
#     name="Search agent",                                    # Name used for logging/tracing
#     instructions=INSTRUCTIONS,                              # System prompt for the language model
#     tools=[WebSearchTool(search_context_size="low")],       # Web search tool with minimal context
#     model=llm_model_to_use,                                 # Language model to use
#     model_settings=ModelSettings(tool_choice="required"),   # Require tool usage
# )