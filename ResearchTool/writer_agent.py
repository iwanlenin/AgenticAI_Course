# ---------------------------------------------------------------------------
# Description
# ---------------------------------------------------------------------------
"""
Writer Agent Module

This module defines a WriterAgent that generates comprehensive research reports
from provided research data. The agent takes research findings and produces a
well-structured markdown report with summaries and follow-up questions.

The agent's output includes:
- A short summary of findings
- A detailed markdown report (5-10 pages)
- Suggested follow-up research topics
"""

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import os
from pydantic import BaseModel, Field
from agents import Agent


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
# The language model to use
llm_model_to_use = os.getenv("DEFAULT_OPENAI_MODEL")

# System prompt instructions for the language model
INSTRUCTIONS = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with the original query, and some initial research done by a research assistant.\n"
    "You should first come up with an outline for the report that describes the structure and "
    "flow of the report. Then, generate the report and return that as your final output.\n"
    "The final output should be in markdown format, and it should be lengthy and detailed. Aim "
    "for 5-10 pages of content, at least 1000 words."
)


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------
class ReportData(BaseModel):
    """Container for the complete research report data.

    This class holds all components of a research report, including a brief
    summary, the main report content, and suggestions for further research.

    Attributes:
        short_summary (str): A brief 2-3 sentence summary of the findings
        markdown_report (str): The complete detailed report in markdown format
        follow_up_questions (list[str]): List of suggested topics for further research
    """
    short_summary: str = Field(
        description="A short 2-3 sentence summary of the findings."
    )
    
    markdown_report: str = Field(
        description="The final report"
    )
    
    follow_up_questions: list[str] = Field(
        description="Suggested topics to research further"
    )


# ---------------------------------------------------------------------------
# Agent Configuration
# ---------------------------------------------------------------------------
writer_agent = Agent(
    name="WriterAgent",             # Name used for logging/tracing
    instructions=INSTRUCTIONS,      # System prompt for the language model
    model=llm_model_to_use,         # Language model to use
    output_type=ReportData,         # Output parsed into this type via JSON schema
)