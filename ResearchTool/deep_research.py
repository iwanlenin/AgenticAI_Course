# ---------------------------------------------------------------------------
# Description
# ---------------------------------------------------------------------------
"""
Deep Research Web Interface Module

This module provides a web-based interface using Gradio for the research pipeline.
It allows users to input research queries and displays the results in real-time
as they are generated by the ResearchManager.

The interface includes:
- A text input for the research query
- A run button to start the research
- A markdown display area for showing the results
"""

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager


# ---------------------------------------------------------------------------
# Environment Setup
# ---------------------------------------------------------------------------
# Load environment variables from a local .env file, overriding any existing
# variables in the shell. This keeps API keys and other secrets out of source.
load_dotenv(override=True)


# ---------------------------------------------------------------------------
# Core Functionality
# ---------------------------------------------------------------------------
async def run(query: str):
    """Execute the research pipeline for a given query.

    This coroutine handles the main research workflow by instantiating a
    ResearchManager and streaming its output to the Gradio interface.

    Args:
        query (str): The research question/topic provided by the user.

    Yields:
        str: Incremental chunks of markdown content produced by ResearchManager.
             Gradio will stream these chunks to the frontend as they arrive.
    """
    # Instantiate a new ResearchManager and start the research pipeline.
    # We stream the output so the user sees partial results immediately.
    async for chunk in ResearchManager().run(query):
        yield chunk


# ---------------------------------------------------------------------------
# Gradio Interface Setup
# ---------------------------------------------------------------------------
# Build the Gradio UI interface with a modern sky-blue theme
with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    # Title section
    gr.Markdown("# Deep Research")

    # Input section
    query_textbox = gr.Textbox(
        label="What topic would you like to research?"
    )

    # Action section
    run_button = gr.Button(
        "Run",
        variant="primary"
    )

    # Output section
    report = gr.Markdown(
        label="Report"
    )
    
    # Event handlers
    # Wire the UI widgets to the `run` coroutine:
    # - Clicking the button triggers the research
    # - Pressing ENTER inside the textbox does the same
    run_button.click(fn=run, inputs=query_textbox, outputs=report)
    query_textbox.submit(fn=run, inputs=query_textbox, outputs=report)

# Launch the app in the user's default web browser
ui.launch(inbrowser=True)

