# ---------------------------------------------------------------------------
# Description
# ---------------------------------------------------------------------------
"""
Search Agent Module

This module defines a SearchAgent that performs web searches and generates concise
summaries of the search results. The agent is designed to be part of a larger
research pipeline, providing focused and relevant information for report generation.

The agent:
- Performs web searches using provided search terms
- Generates brief, focused summaries (2-3 paragraphs, <300 words)
- Captures essential information while removing unnecessary details
"""

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import os
from agents import Agent, WebSearchTool, ModelSettings


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
# The language model to use
llm_model_to_use = os.getenv("DEFAULT_OPENAI_MODEL")

# System prompt instructions for the language model
INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 "
    "words. Capture the main points. Write succintly, no need to have complete sentences or good "
    "grammar. This will be consumed by someone synthesizing a report, so its vital you capture the "
    "essence and ignore any fluff. Do not include any additional commentary other than the summary itself."
)


# ---------------------------------------------------------------------------
# Agent Configuration
# ---------------------------------------------------------------------------
search_agent = Agent(
    name="Search agent",                                    # Name used for logging/tracing
    instructions=INSTRUCTIONS,                              # System prompt for the language model
    tools=[WebSearchTool(search_context_size="low")],       # Web search tool with minimal context
    model=llm_model_to_use,                                 # Language model to use
    model_settings=ModelSettings(tool_choice="required"),   # Require tool usage
)