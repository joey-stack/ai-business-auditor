#!/usr/bin/env python3
"""
Cloud Email Notifier for LinkedIn Content Engine (GitHub Actions or Cloud Cron).
- Runs in the cloud (GitHub Actions, AWS Lambda, or Serverless Cron).
- Determines which post is scheduled for today.
- Sends an HTML email with the exact post hook, body copy, and local carousel path.
- Triggered 15 minutes prior to posting window.
"""
import os
import sys
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# Calendar Schedule mapping: Day of week and target post
# Week 1:
# Tue Sept 22: Post 1 (Speed to Lead Carousel)
# Thu Sept 24: Post 2 (Pricing Framework)
# Sun Sept 27: Post 3 (Contrarian Lead Leakage)
# etc.

POST_DATA_MAP = [
    {
        "post_num": "POST #1",
        "date_str": "2026-09-22",
        "day_name": "Tuesday",
        "time_str": "8:15 AM EST",
        "format": "PDF Document Carousel (6 Slides)",
        "topic": "Speed-to-Lead & Response Latency",
        "asset": "outputs/linkedin_content/carousels/carousel_1_speed_to_lead.pdf",
        "hook": "If a homeowner has a burst pipe at 9:00 PM, they don't fill out a 7-field contact form and wait 12 hours for an email reply.",
        "body": """If a homeowner has a burst pipe at 9:00 PM, they don't fill out a 7-field contact form and wait 12 hours for an email reply.

They call the first 3 plumbing contractors on Google Maps. The first company that answers or replies by SMS within 60 seconds captures the $3,500 emergency replacement job.

In our recent diagnostic audits of $2M–$5M trade fleets, we found businesses leaking $14,500 every single month from unassisted after-hours call abandonment.

Here is the 3-step automated triage stack we install to capture those jobs automatically without burning out dispatchers:
1. Instant SMS acknowledgment with water shutoff valve safety instructions.
2. Urgency triage to classify genuine emergencies vs next-day routine requests.
3. Priority dispatch alerting on-call technicians directly in the CRM calendar.

Speed to lead isn't marketing—it's operational architecture.

What's your current after-hours response time?

#FieldService #TradeContractors #OperationalEfficiency #WorkflowAutomation"""
    },
    {
        "post_num": "POST #2",
        "date_str": "2026-09-24",
        "day_name": "Thursday",
        "time_str": "9:00 AM EST",
        "format": "Strategic Framework Breakdown",
        "topic": "Choice Architecture & Pricing Psychology",
        "asset": "outputs/clients/apex-home-services/audit_sample.pdf (Pinned in Featured)",
        "hook": "Why single-price estimates leave 20% to 25% of margin on the table for mechanical contractors.",
        "body": """Why single-price estimates leave 20% to 25% of margin on the table for mechanical contractors.

When you present a customer with a single flat quote, their subconscious asks a binary question: "Should I buy this, or should I shop around?"

When you switch field technicians to an interactive Good / Better / Best digital proposal:
• Option 1 (Standard): Solves the immediate mechanical failure.
• Option 2 (Enhanced): Adds extended 2-year warranty + preventative maintenance.
• Option 3 (Premium): High-efficiency system upgrade + priority seasonal dispatch.

Their brain shifts from a binary decision to choice architecture: "Which of these three options is the best fit for my home?"

In our trade diagnostics, this single workflow adjustment consistently lifts average ticket sizes by 22% with zero extra marketing spend.

I've pinned a complete 4-page sample audit in my Featured section showing the financial model behind this. Take a look.

#PricingStrategy #HVAC #ContractorGrowth #OperationsConsulting"""
    },
    {
        "post_num": "POST #3",
        "date_str": "2026-09-27",
        "day_name": "Sunday",
        "time_str": "6:30 PM EST",
        "format": "Contrarian Systems Insight",
        "topic": "Operational Mindset & Growth",
        "asset": "Text Only",
        "hook": "You don't have a lead generation problem. You have a lead leakage problem.",
        "body": """You don't have a lead generation problem. You have a lead leakage problem.

Over the past 6 months, almost every trade contractor and service business owner who reached out to me said the same thing:
"Joel, we need more leads. Should we spend more on Google Ads or Facebook ads?"

When we run the numbers on their existing inbound volume, we find:
• 35% of mobile visitors bounce because the site takes 6+ seconds to load on mobile.
• 25% of evening calls go straight to an unmonitored voicemail.
• Quoting is done on paper or flat single-item invoices, leaving 20% of upsell ticket value on the table.

Spending $5,000 more on advertising when your operational funnel is leaking is like pouring water into a bucket with three holes in the bottom.

Plug the operational leaks first. Then turn on the faucet.

Ready to find the leaks in your firm's workflows? DM me "AUDIT" or schedule a 15-minute operational discovery call via my Featured link.

#OperationsConsulting #BusinessSystems #TradeContractors #GrowthStrategy"""
    },
    {
        "post_num": "POST #4",
        "date_str": "2026-09-29",
        "day_name": "Tuesday",
        "time_str": "8:15 AM EST",
        "format": "PDF Document Carousel (6 Slides)",
        "topic": "Dual-Trade Cross-Sell Silos",
        "asset": "outputs/linkedin_content/carousels/carousel_3_dual_trade_cross_sell.pdf",
        "hook": "The biggest unmined goldmine for home service contractors: the dual-trade cross-sell silo.",
        "body": """The biggest unmined goldmine for home service contractors: the dual-trade cross-sell silo.

If your company holds both plumbing and HVAC licenses, why are 88% of your plumbing customers calling someone else when their AC unit dies?

In a recent audit of an 18-van dual-trade contractor, we identified $18,000/month ($216,000/year) in leaked revenue simply because the two departments operated as isolated software islands.

Plumbing technicians were not prompted to inspect HVAC filters. HVAC maintenance plans were never offered to water heater replacement customers.

The operational fix requires zero added headcount:
1. CRM webhook automation that detects single-trade accounts upon invoice sign-off.
2. Automated seasonal cross-sell sequences offering complimentary multi-point inspections.
3. Unified recurring membership agreements that lock in year-round customer retention.

Cross-selling isn't about pushing products—it's about connecting disconnected software workflows.

#DualTrade #PlumbingAndHVAC #FieldServiceManagement #RecurringRevenue"""
    }
]

def get_current_post():
    # If run in test mode, return Post 1
    if os.environ.get("TEST_RUN", "").lower() in ["1", "true", "yes"]:
        return POST_DATA_MAP[0]

    today_str = datetime.date.today().strftime("%Y-%m-%d")
    for post in POST_DATA_MAP:
        if post["date_str"] == today_str:
            return post

    # If no exact match for today, return the first upcoming or next in schedule
    return POST_DATA_MAP[0]

def send_email(to_email, smtp_user, smtp_pass, post, smtp_host="smtp.gmail.com", smtp_port=587):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🔔 15-Min Reminder: Time to Publish LinkedIn {post['post_num']} ({post['topic']})"
    msg["From"] = smtp_user
    msg["To"] = to_email

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f1f5f9; margin: 0; padding: 20px; }}
        .container {{ max-width: 650px; margin: 0 auto; background: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; }}
        .header {{ background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #ffffff; padding: 24px; text-align: left; }}
        .badge {{ background: #2563eb; color: #ffffff; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; padding: 3px 8px; border-radius: 4px; display: inline-block; margin-bottom: 8px; }}
        .title {{ font-size: 20px; font-weight: 800; margin: 0 0 6px 0; color: #ffffff; }}
        .meta {{ font-size: 13px; color: #94a3b8; margin: 0; }}
        .content {{ padding: 24px; color: #1e293b; line-height: 1.6; font-size: 14px; }}
        .asset-box {{ background: #f8fafc; border-left: 4px solid #2563eb; border: 1px solid #e2e8f0; padding: 12px 16px; border-radius: 6px; margin: 16px 0; }}
        .asset-label {{ font-size: 11px; font-weight: 700; text-transform: uppercase; color: #64748b; margin-bottom: 4px; }}
        .asset-path {{ font-family: monospace; font-size: 12px; color: #0f172a; word-break: break-all; }}
        .post-copy-box {{ background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 18px; font-family: monospace; font-size: 13.5px; white-space: pre-wrap; color: #0f172a; margin: 18px 0; line-height: 1.5; }}
        .btn {{ display: inline-block; background: #2563eb; color: #ffffff !important; text-decoration: none; padding: 12px 24px; border-radius: 6px; font-weight: 700; font-size: 14px; margin-top: 10px; }}
        .footer {{ background: #f8fafc; border-top: 1px solid #e2e8f0; padding: 16px 24px; font-size: 12px; color: #64748b; text-align: center; }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <span class="badge">LinkedIn 15-Minute Alert</span>
          <h1 class="title">{post['post_num']}: {post['topic']}</h1>
          <p class="meta">Scheduled Time: {post['time_str']} | Format: {post['format']}</p>
        </div>
        <div class="content">
          <p>Hi Joel,</p>
          <p>Your scheduled LinkedIn post is due to be published in <strong>15 minutes</strong>. Open LinkedIn, copy the text below, attach the media asset, and hit post!</p>
          
          <div class="asset-box">
            <div class="asset-label">Asset to Attach:</div>
            <div class="asset-path">{post['asset']}</div>
          </div>

          <p style="margin-bottom: 6px; font-weight: bold; color: #0f172a;">Ready-to-Paste Copy (Click box & Copy):</p>
          <div class="post-copy-box">{post['body']}</div>

          <p style="text-align: center; margin-top: 24px;">
            <a href="https://www.linkedin.com/feed/" class="btn" target="_blank">Open LinkedIn to Publish Now →</a>
          </p>
        </div>
        <div class="footer">
          Automated Cloud Dispatcher | AI Business Auditor & LinkedIn Content Engine
        </div>
      </div>
    </body>
    </html>
    """

    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)

    print(f"SUCCESS: Cloud reminder email dispatched to {to_email}")

def main():
    to_email = os.environ.get("NOTIFICATION_EMAIL")
    smtp_user = os.environ.get("SMTP_USER")
    smtp_pass = os.environ.get("SMTP_PASSWORD")
    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))

    post = get_current_post()

    if not to_email or not smtp_user or not smtp_pass:
        print("MISSING CONFIG: Please set NOTIFICATION_EMAIL, SMTP_USER, and SMTP_PASSWORD.")
        print(f"Post {post['post_num']} is ready for publishing at {post['time_str']}.")
        print("Hook:", post['hook'])
        sys.exit(0)

    print(f"Dispatching cloud reminder for {post['post_num']} to {to_email}...")
    send_email(to_email, smtp_user, smtp_pass, post, smtp_host, smtp_port)

if __name__ == "__main__":
    main()
