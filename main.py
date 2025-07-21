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
from Storing import save_to_json
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




def router(state : State):
    pass




