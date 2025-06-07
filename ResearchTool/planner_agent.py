# ---------------------------------------------------------------------------
# Description
# ---------------------------------------------------------------------------
"""
Planner Agent Module

This module defines a PlannerAgent that generates a structured plan of web searches
to answer a given query. The agent outputs a WebSearchPlan containing multiple 
WebSearchItems, each with a specific search query and the reasoning behind it.

Place in the overall pipeline:
1. User or system provides a research query
2. PlannerAgent generates multiple targeted search queries
3. These queries are then used by other agents to gather information
"""

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import os
from pydantic import BaseModel, Field
from agents import Agent
from llm_model_selector import get_model
from llm_helper import LLM_MODEL_NAME


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
# Number of distinct searches the model should propose
HOW_MANY_SEARCHES = 3

# Model configuration
#llm_model_to_use = os.getenv("DEFAULT_OPENAI_MODEL")
llm_model_to_use = get_model(LLM_MODEL_NAME.OPENAI)
print(f"llm_model_to_use: {llm_model_to_use}")

# System prompt instructions for the language model
INSTRUCTIONS = "You are a helpful research assistant. Given a query, come up with a set of web searches " \
              "to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for."


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------
class WebSearchItem(BaseModel):
    """A single search item in the research plan.

    This class represents an individual search query along with the reasoning
    for why this search is relevant to answering the original query.

    Attributes:
        reason (str): Justification for why this search is important to the query
        query (str): The actual search term to be used
    """
    reason: str = Field(
        description="Your reasoning for why this search is important to the query."
    )
    query: str = Field(
        description="The search term to use for the web search."
    )


class WebSearchPlan(BaseModel):
    """Container for multiple WebSearchItems forming a complete research plan.

    This class holds a collection of WebSearchItems that together form a
    comprehensive plan for researching a given query.

    Attributes:
        searches (list[WebSearchItem]): List of planned web searches to perform
    """
    searches: list[WebSearchItem] = Field(
        description="A list of web searches to perform to best answer the query."
    )


# ---------------------------------------------------------------------------
# Agent Configuration
# ---------------------------------------------------------------------------
planner_agent = Agent(
    name="PlannerAgent",        # Name used for logging/tracing
    instructions=INSTRUCTIONS,   # System prompt for the language model
    model=llm_model_to_use,     # Language model to use
    output_type=WebSearchPlan,  # Output parsed into this type via JSON schema
)