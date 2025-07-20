#----------------Imports----------------
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


def save_to_json(expense_data):
    """Save to JSON file - FREE storage option"""
    filename = "expenses.json"

    try:
        with open(filename, 'r') as f:
            expenses = json.load(f)
    except FileNotFoundError:
        expenses = []

    expenses.append(expense_data)

    with open(filename, 'w') as f:
        json.dump(expenses, f, indent=2)

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

def classify_message(state : State):
    last_message = state["messages"][-1]
    classifier_llm = llm.with_structured_output(MessageClassifier)
    result = classifier_llm.invoke([{
        "role": "system",
        "content": """
You are a financial assistant that categorizes spending messages. 

Follow these rules:
1. Always extract the exact numerical amount
2. extract 
- category
- amount: numerical value only (convert any currency to Jordanian Dinars)
- description: short description of what they bought
3. Use ONLY these categories:
   - housing (rent, mortgage, utilities)
   - food (groceries, restaurants)
   - transportation (gas, public transit)
   - healthcare (medical bills, insurance)
   - debt (credit cards, loans)
   - entertainment (movies, games)
   - shopping (clothes, electronics)
   - personal_care (gym, haircuts)
   - savings (bank deposits)
   - investments (stocks, crypto)
   - gifts (presents, donations)
   - subscriptions (Netflix, Spotify)
   - other (anything else)


Example:
"I spent $25 on groceries" → category="food", amount=25.0, description="groceries"
"Paid 50 for gas" → category="transport", amount=50.0, description="gas"
"Bought coffee for $4.50" → category="food", amount=4.5, description="coffee"
"""
    }])

    return {
        "category": result.category,
        "amount": result.amount,
        "description": result.description,
    }


def save_expense(state: State):
    """Save expense to storage"""
    expense_data = {
        "date": datetime.now().isoformat(),
        "category": state["category"],
        "amount": state["amount"],
        "description": state["description"]
    }

    # Save to JSON file (simplest option)
    save_to_json(expense_data)

    # Optionally save to SQLite
    # save_to_sqlite(expense_data)

    response = f"💰 Saved: ${state['amount']:.2f} for {state['description']} ({state['category']})"

    return {
        "messages": [{"role": "assistant", "content": response}]
    }


def router(state : State):
    pass




