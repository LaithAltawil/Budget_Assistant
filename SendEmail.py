# import os
# import smtplib
# import ssl
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
#
# from datetime import datetime
# from config import config
#
#
# GMAIL_USER = os.getenv('GMAIL_USER')  # your-email@gmail.com
# GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')  # App-specific password
# RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')  # where to send reports
#
#
# # def generate_monthly_email_body(summary: dict, month_name: str, year: int) -> str:
# #     """Generate HTML email body for monthly report"""
# #     report_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# #
# #     html_body = f"""
# #     <html>
# #     <head>
# #         <style>
# #             body {{ font-family: Arial, sans-serif; margin: 20px; }}
# #             .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
# #             .summary {{ background-color: #f9f9f9; padding: 15px; margin: 10px 0; border-radius: 5px; }}
# #             .category {{ margin: 10px 0; padding: 10px; border-left: 4px solid #2196F3; }}
# #             .total {{ font-size: 24px; font-weight: bold; color: #4CAF50; }}
# #             .category-amount {{ font-weight: bold; color: #333; }}
# #             table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
# #             th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
# #             th {{ background-color: #f2f2f2; }}
# #         </style>
# #     </head>
# #     <body>
# #         <div class="header">
# #             <h1>💰 Expense Report</h1>
# #             <h2>{month_name} {year}</h2>
# #         </div>
# #
# #         <div class="summary">
# #             <h3>📊 Monthly Summary</h3>
# #             <p class="total">Total Spending: {summary['total']:.2f} JD</p>
# #             <p>Total Transactions: {summary['transaction_count']}</p>
# #             <p>Average per Transaction: {summary['total'] / summary['transaction_count']:.2f} JD</p>
# #         </div>
# #
# #         <div>
# #             <h3>📈 Spending by Category</h3>
# #             <table>
# #                 <tr>
# #                     <th>Category</th>
# #                     <th>Amount (JD)</th>
# #                     <th>Percentage</th>
# #                 </tr>
# #     """
# #
# #     # Add category breakdown
# #     for category, amount in summary['by_category'].items():
# #         percentage = (amount / summary['total']) * 100
# #         html_body += f"""
# #                 <tr>
# #                     <td>{category.title()}</td>
# #                     <td>{amount:.2f} JD</td>
# #                     <td>{percentage:.1f}%</td>
# #                 </tr>
# #         """
# #
# #     html_body += f"""
# #             </table>
# #         </div>
# #
# #         <div style="margin-top: 30px; padding: 15px; background-color: #e8f5e8; border-radius: 5px;">
# #             <p><strong>💡 Tip:</strong> Review your spending patterns and consider setting category budgets for next month!</p>
# #         </div>
# #
# #         <div style="margin-top: 20px; text-align: center; color: #666;">
# #             <p>Generated automatically by your Expense Tracker</p>
# #              <p>Reported Date : {report_date}</p>
# #         </div>
# #     </body>
# #     </html>
# #     """
# #
# #     return html_body
#
# def generate_monthly_email_body(summary: dict, month_name: str, year: int) -> str:
#     """Generate HTML email body for monthly report with pie chart"""
#     report_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#
#     # Define colors for categories
#     category_colors = {
#         'housing': '#FF6384',
#         'food': '#36A2EB',
#         'transportation': '#FFCE56',
#         'healthcare': '#4BC0C0',
#         'debt': '#9966FF',
#         'entertainment': '#FF9F40',
#         'shopping': '#FF6B6B',
#         'personal_care': '#C9CBCF',
#         'savings': '#4ECDC4',
#         'investments': '#45B7D1',
#         'gifts': '#96CEB4',
#         'subscriptions': '#FFEAA7',
#         'other': '#DDA0DD'
#     }
#
#     # Generate pie chart segments
#     pie_chart_html = generate_email_compatible_pie_chart(summary['by_category'], category_colors)
#
#     html_body = f"""
#     <html>
#     <head>
#         <style>
#             body {{ font-family: Arial, sans-serif; margin: 20px; }}
#             .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
#             .summary {{ background-color: #f9f9f9; padding: 15px; margin: 10px 0; border-radius: 5px; }}
#             .category {{ margin: 10px 0; padding: 10px; border-left: 4px solid #2196F3; }}
#             .total {{ font-size: 24px; font-weight: bold; color: #4CAF50; }}
#             .category-amount {{ font-weight: bold; color: #333; }}
#             table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
#             th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
#             th {{ background-color: #f2f2f2; }}
#
#             /* Email-compatible chart styles */
#             .chart-container {{
#                 text-align: center;
#                 margin: 20px 0;
#             }}
#             .chart-wrapper {{
#                 display: inline-block;
#                 margin: 20px;
#                 vertical-align: top;
#             }}
#             .bar-chart {{
#                 display: inline-block;
#                 vertical-align: top;
#                 margin-left: 30px;
#             }}
#             .chart-bar {{
#                 display: block;
#                 margin: 5px 0;
#                 height: 25px;
#                 min-width: 20px;
#                 border-radius: 3px;
#                 position: relative;
#             }}
#             .chart-label {{
#                 display: inline-block;
#                 width: 120px;
#                 text-align: right;
#                 padding-right: 10px;
#                 font-size: 12px;
#                 vertical-align: middle;
#             }}
#             .chart-value {{
#                 color: white;
#                 font-size: 11px;
#                 font-weight: bold;
#                 position: absolute;
#                 right: 5px;
#                 top: 6px;
#                 text-shadow: 1px 1px 1px rgba(0,0,0,0.5);
#             }}
#             .donut-chart {{
#                 width: 200px;
#                 height: 200px;
#                 border-radius: 50%;
#                 position: relative;
#                 margin: 0 auto 20px;
#             }}
#             .donut-segment {{
#                 position: absolute;
#                 width: 200px;
#                 height: 200px;
#                 border-radius: 50%;
#             }}
#             .legend-item {{
#                 display: inline-block;
#                 margin: 5px 10px;
#                 font-size: 12px;
#             }}
#             .legend-color {{
#                 display: inline-block;
#                 width: 15px;
#                 height: 15px;
#                 margin-right: 5px;
#                 border-radius: 3px;
#                 vertical-align: middle;
#             }}
#         </style>
#     </head>
#     <body>
#         <div class="header">
#             <h1>💰 Expense Report</h1>
#             <h2>{month_name} {year}</h2>
#         </div>
#
#         <div class="summary">
#             <h3>📊 Monthly Summary</h3>
#             <p class="total">Total Spending: {summary['total']:.2f} JD</p>
#             <p>Total Transactions: {summary['transaction_count']}</p>
#             <p>Average per Transaction: {summary['total'] / summary['transaction_count']:.2f} JD</p>
#         </div>
#
#         <div>
#             <h3>📈 Visual Spending Breakdown</h3>
#             <div class="chart-container">
#                 {pie_chart_html}
#             </div>
#         </div>
#
#         <div>
#             <h3>📋 Detailed Breakdown</h3>
#             <table>
#                 <tr>
#                     <th>Category</th>
#                     <th>Amount (JD)</th>
#                     <th>Percentage</th>
#                 </tr>
#     """
#
#     # Add category breakdown with colors
#     for category, amount in summary['by_category'].items():
#         percentage = (amount / summary['total']) * 100
#         color = category_colors.get(category, '#C9CBCF')
#         html_body += f"""
#                 <tr>
#                     <td>
#                         <span style="display: inline-block; width: 15px; height: 15px; background-color: {color}; margin-right: 8px; border-radius: 3px; vertical-align: middle;"></span>
#                         {category.title()}
#                     </td>
#                     <td>{amount:.2f} JD</td>
#                     <td>{percentage:.1f}%</td>
#                 </tr>
#         """
#
#     html_body += f"""
#             </table>
#         </div>
#
#         <div style="margin-top: 30px; padding: 15px; background-color: #e8f5e8; border-radius: 5px;">
#             <p><strong>💡 Tip:</strong> Review your spending patterns and consider setting category budgets for next month!</p>
#         </div>
#
#         <div style="margin-top: 20px; text-align: center; color: #666;">
#             <p>Generated automatically by your Expense Tracker</p>
#              <p>Reported Date : {report_date}</p>
#         </div>
#     </body>
#     </html>
#     """
#
#     return html_body
#
#
# def generate_email_compatible_pie_chart(categories: dict, colors: dict) -> str:
#     """Generate email-compatible visual chart using horizontal bars and simple shapes"""
#     total = sum(categories.values())
#     if total == 0:
#         return "<p>No data to display</p>"
#
#     # Sort categories by amount (largest first)
#     sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
#
#     # Create horizontal bar chart
#     chart_html = '<div class="chart-wrapper">'
#
#     # Add title
#     chart_html += '<h4 style="text-align: center; margin-bottom: 20px;">💰 Spending Distribution</h4>'
#
#     max_amount = max(categories.values()) if categories.values() else 1
#
#     for category, amount in sorted_categories:
#         if amount > 0:
#             percentage = (amount / total) * 100
#             bar_width = int((amount / max_amount) * 300)  # Max width 300px
#             color = colors.get(category, '#C9CBCF')
#
#             chart_html += f'''
#             <div style="margin: 8px 0; display: flex; align-items: center;">
#                 <span class="chart-label" style="display: inline-block; width: 100px; text-align: right; padding-right: 10px; font-size: 12px;">
#                     {category.title()}:
#                 </span>
#                 <div style="display: inline-block; background-color: {color}; height: 20px; width: {bar_width}px; min-width: 30px; border-radius: 3px; position: relative;">
#                     <span style="color: white; font-size: 10px; font-weight: bold; position: absolute; right: 3px; top: 3px; text-shadow: 1px 1px 1px rgba(0,0,0,0.5);">
#                         {percentage:.1f}%
#                     </span>
#                 </div>
#                 <span style="margin-left: 10px; font-size: 11px; color: #666;">
#                     {amount:.0f} JD
#                 </span>
#             </div>
#             '''
#
#     chart_html += '</div>'
#
#     # Add simple circular representation using HTML entities and colors
#     chart_html += '''
#     <div style="margin-top: 30px;">
#         <h4 style="text-align: center;">🎯 Category Indicators</h4>
#         <div style="text-align: center; line-height: 2;">
#     '''
#
#     for category, amount in sorted_categories:
#         if amount > 0:
#             percentage = (amount / total) * 100
#             color = colors.get(category, '#C9CBCF')
#             # Use circle size to represent proportion
#             circle_size = max(12, int(percentage / 5) + 12)  # Min 12px, scales with percentage
#
#             chart_html += f'''
#             <div class="legend-item" style="display: inline-block; margin: 5px 10px; text-align: center;">
#                 <div style="width: {circle_size}px; height: {circle_size}px; background-color: {color}; border-radius: 50%; margin: 0 auto 5px; border: 2px solid #fff; box-shadow: 0 2px 4px rgba(0,0,0,0.2);"></div>
#                 <div style="font-size: 11px; font-weight: bold;">{category.title()}</div>
#                 <div style="font-size: 10px; color: #666;">{percentage:.1f}%</div>
#             </div>
#             '''
#
#     chart_html += '''
#         </div>
#         <p style="font-size: 11px; color: #888; text-align: center; margin-top: 10px;">
#             Circle size represents spending proportion
#         </p>
#     </div>
#     '''
#
#     return chart_html
#
#
# def send_gmail(subject: str, body: str) -> bool:
#     """
#     Send email via Gmail SMTP
#
#     Setup required:
#     1. Enable 2-factor authentication on Gmail
#     2. Generate app-specific password
#     3. Set environment variables: GMAIL_USER, GMAIL_APP_PASSWORD, RECIPIENT_EMAIL
#     """
#
#     if not all([GMAIL_USER, GMAIL_APP_PASSWORD, RECIPIENT_EMAIL]):
#         print("❌ Gmail configuration missing. Please set environment variables:")
#         print("   - GMAIL_USER (your Gmail address)")
#         print("   - GMAIL_APP_PASSWORD (app-specific password)")
#         print("   - RECIPIENT_EMAIL (where to send reports)")
#         return False
#
#     try:
#         # Create message
#         message = MIMEMultipart("alternative")
#         message["Subject"] = subject
#         message["From"] = GMAIL_USER
#         message["To"] = RECIPIENT_EMAIL
#
#         # Add HTML body
#         html_part = MIMEText(body, "html")
#         message.attach(html_part)
#
#         # Create secure connection and send
#         context = ssl.create_default_context()
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#             server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
#             server.sendmail(GMAIL_USER, RECIPIENT_EMAIL, message.as_string())
#
#         print(f"✅ Email sent successfully to {RECIPIENT_EMAIL}")
#         return True
#
#     except Exception as e:
#         print(f"❌ Failed to send email: {e}")
#         return False

import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from config import config

GMAIL_USER = os.getenv('GMAIL_USER')  # your-email@gmail.com
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')  # App-specific password
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')  # where to send reports


def generate_monthly_email_body(summary: dict, month_name: str, year: int) -> str:
    """Generate modern, user-friendly HTML email body for monthly report"""
    report_date = datetime.now().strftime('%B %d, %Y at %I:%M %p')

    # Enhanced color palette
    category_colors = {
        'housing': '#FF6B6B',
        'food': '#4ECDC4',
        'transportation': '#45B7D1',
        'healthcare': '#96CEB4',
        'debt': '#FECA57',
        'entertainment': '#FF9FF3',
        'shopping': '#54A0FF',
        'personal_care': '#5F27CD',
        'savings': '#00D2D3',
        'investments': '#FF9F43',
        'gifts': '#EE5A24',
        'subscriptions': '#0ABDE3',
        'other': '#B2BEC3'
    }

    avg_transaction = summary['total'] / summary['transaction_count'] if summary['transaction_count'] > 0 else 0
    top_category = max(summary['by_category'].items(), key=lambda x: x[1]) if summary['by_category'] else ('none', 0)

    chart_html = generate_modern_chart(summary['by_category'], category_colors)
    insights_html = generate_spending_insights(summary, top_category)

    html_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Monthly Expense Report - {month_name} {year}</title>
        <style>
            /* Reset and base styles */
            body, table, div, p, a {{ 
                margin: 0; 
                padding: 0; 
                border: 0; 
                font-size: 100%; 
                font: inherit; 
                vertical-align: baseline; 
                line-height: 1.6; 
                color: #333; 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', sans-serif;
            }}
            body {{ 
                background: #f0f2f5; 
                padding: 20px; 
            }}
            .email-container {{
                max-width: 800px;
                margin: 0 auto;
                background: #ffffff;
                border-radius: 16px;
                overflow: hidden;
                box-shadow: 0 12px 30px rgba(0,0,0,0.12);
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
                padding: 50px 30px;
                position: relative;
            }}
            .header h1 {{
                font-size: 2.8em;
                margin: 0 0 10px;
                font-weight: 700;
                letter-spacing: -0.5px;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }}
            .header h2 {{
                font-size: 1.6em;
                font-weight: 300;
                opacity: 0.9;
                margin: 0;
            }}
            .content {{
                padding: 40px 30px;
                background: #ffffff;
            }}
            .summary-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }}
            .summary-card {{
                background: #f9faff;
                border-radius: 14px;
                padding: 24px;
                text-align: center;
                border-left: 6px solid #667eea;
                transition: all 0.3s ease;
                box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            }}
            .summary-card:hover {{
                transform: translateY(-6px);
                box-shadow: 0 12px 25px rgba(0,0,0,0.1);
            }}
            .summary-value {{
                font-size: 2.3em;
                font-weight: 700;
                color: #667eea;
                margin-bottom: 6px;
            }}
            .summary-label {{
                font-size: 0.9em;
                color: #6c757d;
                text-transform: uppercase;
                letter-spacing: 1.2px;
                font-weight: 500;
            }}
            .section {{
                background: #ffffff;
                border-radius: 14px;
                padding: 30px;
                margin: 35px 0;
                box-shadow: 0 5px 18px rgba(0,0,0,0.08);
                border: 1px solid #eef0f3;
            }}
            .section-title {{
                font-size: 1.5em;
                font-weight: 600;
                color: #2d3748;
                margin-bottom: 24px;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            .section-title::after {{
                content: '';
                flex: 1;
                height: 2px;
                background: linear-gradient(to right, #667eea, transparent);
            }}
            .chart-container {{
                background: #f8f9fa;
                border-radius: 14px;
                padding: 25px;
                margin-top: 15px;
            }}
            .insights {{
                background: #e8f5e8;
                border-radius: 14px;
                padding: 24px;
                margin: 30px 0;
                border: 1px solid #d4edda;
            }}
            .insight-item {{
                display: flex;
                align-items: flex-start;
                margin: 14px 0;
                padding: 14px;
                background: rgba(255,255,255,0.85);
                border-radius: 10px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            }}
            .insight-item:hover {{
                background: #ffffff;
                transform: scale(1.01);
            }}
            .insight-icon {{
                font-size: 1.6em;
                margin-right: 14px;
                min-width: 36px;
                text-align: center;
            }}
            .table-container {{
                overflow-x: auto;
                border-radius: 14px;
                box-shadow: 0 6px 16px rgba(0,0,0,0.06);
                border: 1px solid #eef0f3;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                table-layout: auto;
            }}
            th {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 18px 16px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-size: 0.85em;
                text-align: left;
            }}
            td {{
                padding: 16px;
                border-bottom: 1px solid #edf0f4;
                color: #4a5568;
            }}
            tr:hover td {{
                background: #f7f9fc;
            }}
            tr:last-child td {{
                border-bottom: none;
            }}
            .category-indicator {{
                display: inline-block;
                width: 16px;
                height: 16px;
                border-radius: 50%;
                margin-right: 12px;
                vertical-align: middle;
                box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            }}
            .footer {{
                background: #f8f9fa;
                padding: 30px;
                text-align: center;
                color: #777;
                border-top: 1px solid #eef0f3;
                font-size: 0.9em;
            }}
            .footer-logo {{
                font-size: 1.3em;
                font-weight: 600;
                color: #667eea;
                margin-bottom: 8px;
            }}
            .generated-text {{
                opacity: 0.8;
            }}
            /* Responsive */
            @media (max-width: 600px) {{
                .email-container {{ margin: 10px; }}
                .header {{ padding: 30px 20px; }}
                .content {{ padding: 25px 15px; }}
                .summary-grid {{ grid-template-columns: 1fr; }}
                .header h1 {{ font-size: 2.2em; }}
                .header h2 {{ font-size: 1.3em; }}
                .section, .insights, .chart-container {{ padding: 20px; }}
                .table-container {{ border-radius: 10px; }}
                table, thead, tbody, th, td, tr {{
                    display: block;
                }}
                th {{
                    text-align: left;
                    position: absolute;
                    width: 1px;
                    height: 1px;
                    overflow: hidden;
                    clip: rect(0 0 0 0);
                }}
                tr {{
                    margin-bottom: 15px;
                    border-bottom: 2px solid #eee;
                    padding-bottom: 10px;
                }}
                td {{
                    border: none;
                    position: relative;
                    padding-left: 120px;
                    text-align: left;
                    display: block;
                }}
                td:before {{
                    content: attr(data-label);
                    position: absolute;
                    left: 16px;
                    width: 100px;
                    font-weight: 600;
                    color: #555;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <h1>💰 Expense Report</h1>
                <h2>{month_name} {year}</h2>
            </div>

            <div class="content">
                <div class="summary-grid">
                    <div class="summary-card">
                        <div class="summary-value">{summary['total']:.0f} JD</div>
                        <div class="summary-label">Total Spending</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-value">{summary['transaction_count']}</div>
                        <div class="summary-label">Transactions</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-value">{avg_transaction:.0f} JD</div>
                        <div class="summary-label">Avg per Transaction</div>
                    </div>
                </div>

                {insights_html}

                <div class="section">
                    <h3 class="section-title">📊 Visual Breakdown</h3>
                    <div class="chart-container">
                        {chart_html}
                    </div>
                </div>

                <div class="section">
                    <h3 class="section-title">📋 Detailed Summary</h3>
                    <div class="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Category</th>
                                    <th>Amount (JD)</th>
                                    <th>Percentage</th>
                                    <th>Trend</th>
                                </tr>
                            </thead>
                            <tbody>
    """

    for category, amount in sorted(summary['by_category'].items(), key=lambda x: x[1], reverse=True):
        percentage = (amount / summary['total']) * 100
        color = category_colors.get(category, '#B2BEC3')
        trend_emoji = get_trend_emoji(percentage)
        html_body += f"""
                                <tr>
                                    <td data-label="Category">
                                        <span class="category-indicator" style="background-color: {color};"></span>
                                        <strong>{category.title()}</strong>
                                    </td>
                                    <td data-label="Amount"><strong>{amount:.2f} JD</strong></td>
                                    <td data-label="Percentage">
                                        <div style="display: flex; align-items: center; gap: 10px;">
                                            <span><strong>{percentage:.1f}%</strong></span>
                                            <div style="background: #e9ecef; height: 8px; width: 60px; border-radius: 4px; overflow: hidden;">
                                                <div style="background: {color}; height: 100%; width: {percentage}%; border-radius: 4px;"></div>
                                            </div>
                                        </div>
                                    </td>
                                    <td data-label="Trend" style="font-size: 1.2em; text-align: center;">{trend_emoji}</td>
                                </tr>
        """

    html_body += f"""
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div class="footer">
                <div class="footer-logo">💎 Smart Expense Tracker</div>
                <div class="generated-text">
                    Report generated on {report_date}<br>
                    Stay on top of your finances! 📈
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_body


def generate_modern_chart(categories: dict, colors: dict) -> str:
    """Generate modern, responsive chart visualization"""
    total = sum(categories.values())
    if total == 0:
        return "<p style='text-align: center; color: #6c757d; font-style: italic;'>No spending data available</p>"

    sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
    max_amount = max(categories.values()) if categories.values() else 1

    chart_html = """
    <div style="display: grid; gap: 20px;">
        <div style="text-align: center; margin-bottom: 20px;">
            <h4 style="color: #333; font-weight: 600; margin-bottom: 30px;">📈 Spending Distribution</h4>
        </div>
    """

    # Enhanced bar chart
    for category, amount in sorted_categories:
        if amount > 0:
            percentage = (amount / total) * 100
            bar_width = (amount / max_amount) * 100
            color = colors.get(category, '#B2BEC3')

            chart_html += f"""
            <div style="margin: 15px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="width: 12px; height: 12px; background: {color}; border-radius: 50%; box-shadow: 0 2px 4px rgba(0,0,0,0.2);"></div>
                        <span style="font-weight: 600; color: #333;">{category.title()}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <span style="font-weight: 600; color: {color};">{amount:.0f} JD</span>
                        <span style="font-size: 0.9em; color: #6c757d; min-width: 45px;">{percentage:.1f}%</span>
                    </div>
                </div>
                <div style="background: #e9ecef; height: 12px; border-radius: 6px; overflow: hidden; position: relative;">
                    <div style="background: linear-gradient(90deg, {color} 0%, {adjust_color_brightness(color, 0.8)} 100%); height: 100%; width: {bar_width}%; border-radius: 6px; transition: width 0.8s ease-in-out; box-shadow: inset 0 1px 2px rgba(0,0,0,0.1);"></div>
                </div>
            </div>
            """

    # Add donut-style visualization
    chart_html += """
        <div style="margin-top: 40px; text-align: center;">
            <h4 style="color: #333; margin-bottom: 20px;">🎯 Category Proportions</h4>
            <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; margin-top: 20px;">
    """

    for category, amount in sorted_categories:
        if amount > 0:
            percentage = (amount / total) * 100
            color = colors.get(category, '#B2BEC3')
            circle_size = max(30, int(percentage * 2) + 20)

            chart_html += f"""
            <div style="text-align: center; margin: 10px;">
                <div style="
                    width: {circle_size}px; 
                    height: {circle_size}px; 
                    background: linear-gradient(135deg, {color} 0%, {adjust_color_brightness(color, 0.7)} 100%); 
                    border-radius: 50%; 
                    margin: 0 auto 10px; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                    border: 3px solid white;
                    color: white;
                    font-weight: bold;
                    font-size: {max(10, circle_size // 6)}px;
                    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
                ">
                    {percentage:.0f}%
                </div>
                <div style="font-size: 0.85em; font-weight: 600; color: #333;">{category.title()}</div>
                <div style="font-size: 0.75em; color: #6c757d;">{amount:.0f} JD</div>
            </div>
            """

    chart_html += """
            </div>
        </div>
    </div>
    """

    return chart_html


def generate_spending_insights(summary: dict, top_category: tuple) -> str:
    """Generate personalized spending insights"""
    insights = []

    # Top spending category
    if top_category[1] > 0:
        percentage = (top_category[1] / summary['total']) * 100
        insights.append({
            'icon': '🏆',
            'text': f"Your highest spending category is <strong>{top_category[0].title()}</strong> at {percentage:.1f}% of total expenses"
        })

    # Transaction frequency insight
    if summary['transaction_count'] > 0:
        avg_transaction = summary['total'] / summary['transaction_count']
        if avg_transaction > 50:
            insights.append({
                'icon': '💳',
                'text': f"You averaged <strong>{avg_transaction:.0f} JD</strong> per transaction - consider tracking smaller purchases"
            })
        else:
            insights.append({
                'icon': '✅',
                'text': f"Great job on mindful spending! Average transaction: <strong>{avg_transaction:.0f} JD</strong>"
            })

    # Category diversity
    category_count = len(summary['by_category'])
    if category_count >= 5:
        insights.append({
            'icon': '🌟',
            'text': f"You have expenses across <strong>{category_count}</strong> categories - shows balanced lifestyle"
        })
    elif category_count <= 2:
        insights.append({
            'icon': '🎯',
            'text': f"Your spending is focused on <strong>{category_count}</strong> main categories - very streamlined!"
        })

    # Savings insight
    if 'savings' in summary['by_category']:
        savings_pct = (summary['by_category']['savings'] / summary['total']) * 100
        insights.append({
            'icon': '💰',
            'text': f"Excellent! You allocated <strong>{savings_pct:.1f}%</strong> to savings this month"
        })

    if not insights:
        insights.append({
            'icon': '📊',
            'text': "Keep tracking your expenses to unlock personalized insights!"
        })

    insights_html = f"""
    <div class="insights">
        <h3 style="color: #155724; margin-bottom: 20px; display: flex; align-items: center; gap: 10px;">
            💡 Smart Insights
        </h3>
    """

    for insight in insights:
        insights_html += f"""
        <div class="insight-item">
            <div class="insight-icon">{insight['icon']}</div>
            <div>{insight['text']}</div>
        </div>
        """

    insights_html += "</div>"
    return insights_html


def get_trend_emoji(percentage: float) -> str:
    """Get trend emoji based on percentage"""
    if percentage >= 30:
        return "🔴"  # High spending
    elif percentage >= 15:
        return "🟡"  # Medium spending
    else:
        return "🟢"  # Low spending


def adjust_color_brightness(hex_color: str, factor: float) -> str:
    """Adjust color brightness for gradients"""
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]

    # Convert hex to RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    # Adjust brightness
    r = min(255, int(r * factor))
    g = min(255, int(g * factor))
    b = min(255, int(b * factor))

    # Convert back to hex
    return f"#{r:02x}{g:02x}{b:02x}"


def send_gmail(subject: str, body: str) -> bool:
    """Send email via Gmail SMTP with enhanced error handling"""
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
        message["X-Priority"] = "1"  # High priority
        message["X-MSMail-Priority"] = "High"

        # Add HTML body
        html_part = MIMEText(body, "html", "utf-8")
        message.attach(html_part)

        # Create secure connection and send
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, RECIPIENT_EMAIL, message.as_string())

        print(f"✅ Enhanced email report sent successfully to {RECIPIENT_EMAIL}")
        return True

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False
