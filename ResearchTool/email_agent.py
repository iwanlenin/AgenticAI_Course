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
from llm_model_selector import get_model
from llm_helper import LLM_MODEL_NAME, EMAIL_ADDRESS

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
# Default sender and recipient email addresses
#from_email = "j.geberlin@gmail.com" #os.getenv("DEFAULT_EMAIL")""
#to_email = "j.geberlin@gmail.com" #os.getenv("DEFAULT_EMAIL")

# Model configuration
llm_to_use = get_model(LLM_MODEL_NAME.OPENAI)


# ---------------------------------------------------------------------------
# Email Sending Function
# ---------------------------------------------------------------------------
@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """ Send an email with the given subject and HTML body """
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("j.geberlin@gmail.com") # put your verified sender here
    to_email = To("j.geberlin@gmail.com") # put your recipient here
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
