#----------------Imports----------------
import json
from datetime import datetime
from typing import TypedDict, Annotated, Literal
import pandas as pd
from typing import Annotated
from pydantic import BaseModel
from pydantic.v1 import Field
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
import os
import dotenv as env
from langchain.chat_models import init_chat_model

#--------------------------------------
def config():
    env.load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("API_KEY")

llm = init_chat_model("openai:gpt-4o-mini")

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]
    category: str | None
    amount: float | None
    description: str | None

class MessageClassifier(BaseModel):
    category: Literal[
        "housing",
        "food",
        "transportation",
        "healthcare",
        "debt",
        "entertainment",
        "shopping",
        "personal_care",
        "savings",
        "investments",
        "gifts",
        "subscriptions",
        "other"
    ] = Field(
        ...,
        description="Broad classification of spending category if it is housing, food, transportation, healthcare, debt, entertainment, shopping, personal_care, savings, investments, gifts, subscriptions, or other."
    )
    amount: float = Field(..., description="Amount of money spent in the category.")
    description: str = Field(description="Brief description of the expense")


# Setup instructions for Gmail
def setup_gmail_instructions():
    """Print setup instructions for Gmail integration"""
    print("""
📧 Gmail Setup Instructions:

1. Enable 2-Factor Authentication:
   - Go to Google Account settings
   - Security > 2-Step Verification > Turn on

2. Generate App Password:
   - Security > App passwords
   - Select app: Mail
   - Select device: Other (custom name)
   - Copy the 16-character password

3. Set Environment Variables:
   export GMAIL_USER="your-email@gmail.com"
   export GMAIL_APP_PASSWORD="your-16-char-app-password"
   export RECIPIENT_EMAIL="where-to-send-reports@gmail.com"

4. Test the setup:
   python -c "from expense_router import send_gmail; send_gmail('Test', 'Hello!')"
""")





