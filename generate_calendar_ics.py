#!/usr/bin/env python3
"""
Generate iCalendar (.ics) file with all 25 scheduled LinkedIn posts.
Includes:
- Exact dates & times across 60 days
- 15-minute popup and email notification alarms (RFC 5545 VALARM)
- Full post copy, hooks, hashtags, and local asset paths in event description
- Compatible with Google Calendar, Outlook, and Apple Calendar.
"""
import datetime
from pathlib import Path
from generate_60_day_content import build_data

def format_ics_text(text: str) -> str:
    # Escape special characters for .ics
    return text.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")

def main():
    data = build_data()
    # Posts start at row index 7
    posts = data[7:]

    # Schedule mapping: 25 posts across 8.5 weeks starting Sept 22, 2026
    # Days: Tuesday 08:15, Thursday 09:00, Sunday 18:30 EST (UTC-5 or UTC-4 during daylight savings)
    # In September/October/November 2026:
    # US EDT is UTC-4 until Nov 1, 2026, then EST is UTC-5.
    
    events_dates = [
        # Week 1
        datetime.datetime(2026, 9, 22, 8, 15), # Tue
        datetime.datetime(2026, 9, 24, 9, 0),  # Thu
        datetime.datetime(2026, 9, 27, 18, 30),# Sun
        # Week 2
        datetime.datetime(2026, 9, 29, 8, 15), # Tue
        datetime.datetime(2026, 10, 1, 9, 0),  # Thu
        datetime.datetime(2026, 10, 4, 18, 30),# Sun
        # Week 3
        datetime.datetime(2026, 10, 6, 8, 15), # Tue
        datetime.datetime(2026, 10, 8, 9, 0),  # Thu
        datetime.datetime(2026, 10, 11, 18, 30),# Sun
        # Week 4
        datetime.datetime(2026, 10, 13, 8, 15), # Tue
        datetime.datetime(2026, 10, 15, 9, 0),  # Thu
        datetime.datetime(2026, 10, 18, 18, 30),# Sun
        # Week 5
        datetime.datetime(2026, 10, 20, 8, 15), # Tue
        datetime.datetime(2026, 10, 22, 9, 0),  # Thu
        datetime.datetime(2026, 10, 25, 18, 30),# Sun
        # Week 6
        datetime.datetime(2026, 10, 27, 8, 15), # Tue
        datetime.datetime(2026, 10, 29, 9, 0),  # Thu
        datetime.datetime(2026, 11, 1, 18, 30), # Sun
        # Week 7
        datetime.datetime(2026, 11, 3, 8, 15), # Tue
        datetime.datetime(2026, 11, 5, 9, 0),  # Thu
        datetime.datetime(2026, 11, 8, 18, 30), # Sun
        # Week 8
        datetime.datetime(2026, 11, 10, 8, 15), # Tue
        datetime.datetime(2026, 11, 12, 9, 0),  # Thu
        datetime.datetime(2026, 11, 15, 18, 30), # Sun
        # Week 9
        datetime.datetime(2026, 11, 17, 8, 15), # Tue (Capstone)
    ]

    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//AI Business Auditor//LinkedIn 60-Day Content Engine//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:LinkedIn Publishing Schedule (Joel Adawah Sani)",
        "X-WR-TIMEZONE:America/New_York",
    ]

    for idx, (post, dt_local) in enumerate(zip(posts, events_dates)):
        post_num = post[0]
        timing_str = post[1]
        post_format = post[2]
        topic = post[3]
        hook = post[5]
        body = post[6]
        asset_path = post[7]
        cta = post[8]

        # EDT is UTC-4 (Sept-Oct), EST is UTC-5 (Nov)
        utc_offset = 4 if dt_local < datetime.datetime(2026, 11, 1, 2, 0) else 5
        dt_utc_start = dt_local + datetime.timedelta(hours=utc_offset)
        dt_utc_end = dt_utc_start + datetime.timedelta(minutes=15)

        start_str = dt_utc_start.strftime("%Y%m%dT%H%M%SZ")
        end_str = dt_utc_end.strftime("%Y%m%dT%H%M%SZ")
        now_str = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        uid = f"linkedin-post-{idx+1}-2026@business-auditor"

        desc = (
            f"LINKEDIN SCHEDULED POST: {post_num}\\n"
            f"FORMAT: {post_format}\\n"
            f"TOPIC: {topic}\\n"
            f"ATTACHED ASSET: {asset_path}\\n"
            f"TARGET GOAL: {cta}\\n\\n"
            f"READY-TO-PASTE COPY:\\n"
            f"-----------------------------------------\\n"
            f"{format_ics_text(body)}\\n"
            f"-----------------------------------------\\n\\n"
            f"POSTING INSTRUCTIONS:\\n"
            f"1. Copy the text above.\\n"
            f"2. Attach the local file if required.\\n"
            f"3. Publish to LinkedIn at {dt_local.strftime('%I:%M %p')}!"
        )

        ics_lines.extend([
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{now_str}",
            f"DTSTART:{start_str}",
            f"DTEND:{end_str}",
            f"SUMMARY:📢 Post #{idx+1}: {post_format} — {topic}",
            f"DESCRIPTION:{desc}",
            f"LOCATION:LinkedIn (https://www.linkedin.com)",
            "STATUS:CONFIRMED",
            # 15-Minute Popup Display Alarm
            "BEGIN:VALARM",
            "TRIGGER:-PT15M",
            "ACTION:DISPLAY",
            f"DESCRIPTION:Reminder: Time to publish LinkedIn Post #{idx+1} in 15 minutes!",
            "END:VALARM",
            # 15-Minute Email Alarm (Native to Google Calendar & Outlook)
            "BEGIN:VALARM",
            "TRIGGER:-PT15M",
            "ACTION:EMAIL",
            f"SUMMARY:Reminder: Publish LinkedIn Post #{idx+1} in 15 minutes",
            f"DESCRIPTION:Your scheduled LinkedIn post ({topic}) is due in 15 minutes. Open event to copy text and asset path.",
            "END:VALARM",
            "END:VEVENT"
        ])

    ics_lines.append("END:VCALENDAR")

    out_path = Path("outputs/linkedin_content/linkedin_posting_schedule.ics")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\r\n".join(ics_lines))

    print(f"SUCCESS: Generated 25 calendar events with 15-minute alerts to: {out_path}")

if __name__ == "__main__":
    main()
