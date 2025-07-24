import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from main import config

config()
GMAIL_USER = os.getenv('GMAIL_USER')  # your-email@gmail.com
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')  # App-specific password
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')  # where to send reports


def generate_monthly_email_body(summary: dict, month_name: str, year: int) -> str:
    """Generate HTML email body for monthly report"""

    html_body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
            .summary {{ background-color: #f9f9f9; padding: 15px; margin: 10px 0; border-radius: 5px; }}
            .category {{ margin: 10px 0; padding: 10px; border-left: 4px solid #2196F3; }}
            .total {{ font-size: 24px; font-weight: bold; color: #4CAF50; }}
            .category-amount {{ font-weight: bold; color: #333; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>💰 Expense Report</h1>
            <h2>{month_name} {year}</h2>
        </div>

        <div class="summary">
            <h3>📊 Monthly Summary</h3>
            <p class="total">Total Spending: ${summary['total']:.2f} JD</p>
            <p>Total Transactions: {summary['transaction_count']}</p>
            <p>Average per Transaction: ${summary['total'] / summary['transaction_count']:.2f} JD</p>
        </div>

        <div>
            <h3>📈 Spending by Category</h3>
            <table>
                <tr>
                    <th>Category</th>
                    <th>Amount (JD)</th>
                    <th>Percentage</th>
                </tr>
    """

    # Add category breakdown
    for category, amount in summary['by_category'].items():
        percentage = (amount / summary['total']) * 100
        html_body += f"""
                <tr>
                    <td>{category.title()}</td>
                    <td>${amount:.2f}</td>
                    <td>{percentage:.1f}%</td>
                </tr>
        """

    html_body += """
            </table>
        </div>

        <div style="margin-top: 30px; padding: 15px; background-color: #e8f5e8; border-radius: 5px;">
            <p><strong>💡 Tip:</strong> Review your spending patterns and consider setting category budgets for next month!</p>
        </div>

        <div style="margin-top: 20px; text-align: center; color: #666;">
            <p>Generated automatically by your Expense Tracker</p>
            <p>Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </body>
    </html>
    """

    return html_body


def send_gmail(subject: str, body: str) -> bool:
    """
    Send email via Gmail SMTP

    Setup required:
    1. Enable 2-factor authentication on Gmail
    2. Generate app-specific password
    3. Set environment variables: GMAIL_USER, GMAIL_APP_PASSWORD, RECIPIENT_EMAIL
    """

    if not all([GMAIL_USER, GMAIL_APP_PASSWORD, RECIPIENT_EMAIL]):
        print("❌ Gmail configuration missing. Please set environment variables:")
        print("   - GMAIL_USER (your Gmail address)")
        print("   - GMAIL_APP_PASSWORD (app-specific password)")
        print("   - RECIPIENT_EMAIL (where to send reports)")
        return False

    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = GMAIL_USER
        message["To"] = RECIPIENT_EMAIL

        # Add HTML body
        html_part = MIMEText(body, "html")
        message.attach(html_part)

        # Create secure connection and send
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, RECIPIENT_EMAIL, message.as_string())

        print(f"✅ Email sent successfully to {RECIPIENT_EMAIL}")
        return True

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False
