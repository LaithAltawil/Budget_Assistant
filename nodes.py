from datetime import datetime

from main import State, MessageClassifier, llm
from Storing import database_setup, save_to_db


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
    save_to_db(expense_data)

    # Optionally save to SQLite
    # save_to_sqlite(expense_data)

    response = f"💰 Saved: ${state['amount']:.2f} for {state['description']} ({state['category']})"

    return {
        "messages": [{"role": "assistant", "content": response}]
    }


def router(state: State) -> Literal[
    "classify_message", "save_expense", "handle_query", "send_monthly_report", "handle_error", "END"]:
    """
    Enhanced router with email reporting capability
    """
    last_message = state["messages"][-1]
    message_content = last_message.get("content", "").lower()

    # Check if we already have classification data
    has_category = state.get("category") is not None
    has_amount = state.get("amount") is not None
    has_description = state.get("description") is not None

    # Route 1: Monthly report request
    if is_monthly_report_request(message_content):
        return "send_monthly_report"

    # Route 2: New expense message that needs classification
    if not has_category and is_expense_message(message_content):
        return "classify_message"

    # Route 3: Classification complete, ready to save
    if has_category and has_amount and has_description:
        return "save_expense"

    # Route 4: Handle queries about expenses (reports, summaries, etc.)
    if is_query_message(message_content):
        return "handle_query"

    # Route 5: Handle errors or invalid messages
    if state.get("error") or not is_valid_message(message_content):
        return "handle_error"

    # Route 6: End conversation
    return "END"


def is_expense_message(content: str) -> bool:
    """Check if message contains expense information"""
    expense_indicators = [
        "spent", "bought", "paid", "cost", "price", "$", "jd", "dinar",
        "expense", "purchase", "bill", "receipt", "money", "cash"
    ]
    return any(indicator in content for indicator in expense_indicators)


def is_query_message(content: str) -> bool:
    """Check if message is asking for information/reports"""
    query_indicators = [
        "how much", "total", "summary", "report", "show me", "list",
        "what did i spend", "weekly", "budget", "category breakdown",
        "recent expenses", "last month", "this month"
    ]
    return any(indicator in content for indicator in query_indicators)


def is_monthly_report_request(content: str) -> bool:
    """Check if user wants monthly email report"""
    report_indicators = [
        "monthly report", "email report", "send report", "monthly summary email",
        "email monthly", "monthly email", "send monthly", "email me monthly"
    ]
    return any(indicator in content for indicator in report_indicators)


def is_valid_message(content: str) -> bool:
    """Basic validation for message content"""
    return len(content.strip()) > 0 and len(content) < 1000


def send_monthly_report(state: State):
    """
    Generate and send monthly expense report via Gmail
    """
    try:
        # Get current month/year or parse from message
        now = datetime.now()
        year = now.year
        month = now.month

        # Check if user specified a different month
        message_content = state["messages"][-1].get("content", "").lower()
        if "last month" in message_content:
            if month == 1:
                month = 12
                year -= 1
            else:
                month -= 1

        # Get monthly summary
        summary = get_monthly_summary(year, month)
        month_name = calendar.month_name[month]

        if summary['total'] == 0:
            response = f"📧 No expenses found for {month_name} {year}. No email sent."
            return {"messages": [{"role": "assistant", "content": response}]}

        # Generate email content
        email_subject = f"Monthly Expense Report - {month_name} {year}"
        email_body = generate_monthly_email_body(summary, month_name, year)

        # Send email
        success = send_gmail(email_subject, email_body)

        if success:
            response = f"📧 Monthly report for {month_name} {year} sent successfully!\n"
            response += f"💰 Total: ${summary['total']:.2f} JD ({summary['transaction_count']} transactions)"
        else:
            response = f"❌ Failed to send monthly report. Please check email configuration."

        return {"messages": [{"role": "assistant", "content": response}]}

    except Exception as e:
        error_response = f"❌ Error generating monthly report: {str(e)}"
        return {
            "messages": [{"role": "assistant", "content": error_response}],
            "error": str(e)
        }