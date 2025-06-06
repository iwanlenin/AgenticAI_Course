# ---------------------------------------------------------------------------
# Description
# ---------------------------------------------------------------------------
"""
Email Agent Module

This module defines an EmailAgent that converts long-form markdown reports into
nicely formatted HTML and sends them via SendGrid. The actual 'send' operation is
exposed to the LLM as a JSON-schema function (@function_tool) so the model can
call it with the required parameters.

Place in the overall pipeline:
1. WriterAgent produces a ReportData object (markdown report)
2. ResearchManager passes that markdown to EmailAgent
3. EmailAgent renders HTML, chooses a subject line, and invokes send_email()

Environment Requirements:
- SENDGRID_API_KEY must be set in the environment
- The from_email address must be verified in SendGrid dashboard
"""

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import os
from typing import Dict

import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
# Default sender and recipient email addresses
from_email = os.getenv("DEFAULT_EMAIL")
to_email = os.getenv("DEFAULT_EMAIL")

# Model configuration
llm_to_use = os.getenv("DEFAULT_OPENAI_MODEL")


# ---------------------------------------------------------------------------
# Email Sending Function
# ---------------------------------------------------------------------------
@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """Send an email with the given subject and HTML body.
    
    This function uses SendGrid's API to send HTML-formatted emails. It requires
    proper configuration of SendGrid API key and verified sender email address.
    
    Args:
        subject (str): The email subject line
        html_body (str): The HTML-formatted content of the email
        
    Returns:
        Dict[str, str]: Response status dictionary with 'success' status
        
    Raises:
        sendgrid.SendGridException: If there's an error sending the email
    """
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(from_email)  # Verified sender address
    to_email = To(to_email)         # Recipient address
    content = Content("text/html", html_body)
    
    mail = Mail(from_email, to_email, subject, content).get()
    response = sg.client.mail.send.post(request_body=mail)
    print("Email response", response.status_code)
    
    return {"status": "success"}


# ---------------------------------------------------------------------------
# Agent Configuration
# ---------------------------------------------------------------------------
INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",                # Name used for logging/tracing
    instructions=INSTRUCTIONS,         # System prompt for the language model
    tools=[send_email],               # Email sending capability
    model=llm_to_use,                 # Language model to use
)
