from datetime import datetime

from main import State, MessageClassifier, llm
from Storing import save_to_json


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