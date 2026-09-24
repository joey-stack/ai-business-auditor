"""
Opportunity Scoring Script for Google Maps Prospects
Parses prospects.csv and calculates an opportunity score (0-100) per lead.
"""
import sys
import csv
import json
from pathlib import Path

def find_column(headers, candidates):
    for h in headers:
        for c in candidates:
            if c.lower() in h.lower():
                return h
    return None

def score_prospects(csv_path="prospects.csv"):
    p = Path(csv_path)
    if not p.exists():
        return {"error": f"File not found: {csv_path}", "total_found": 0, "prospects": []}

    prospects = []
    with open(p, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []

        # Flexible column resolution
        col_name = find_column(headers, ["title", "name", "business", "company"])
        col_addr = find_column(headers, ["address", "location", "street"])
        col_phone = find_column(headers, ["phone", "tel", "contact", "mobile"])
        col_web = find_column(headers, ["website", "url", "site", "web"])
        col_rating = find_column(headers, ["rating", "stars", "score"])
        col_reviews = find_column(headers, ["reviews", "review_count", "ratings_count", "user_ratings_total"])

        for row in reader:
            name = (row.get(col_name) or "Unknown Business").strip()
            address = (row.get(col_addr) or "N/A").strip()
            phone = (row.get(col_phone) or "N/A").strip()
            web = (row.get(col_web) or "").strip()
            
            # Rating parsing
            raw_rating = row.get(col_rating) or ""
            try:
                rating = float(raw_rating.replace(",", ".").split()[0]) if raw_rating else None
            except Exception:
                rating = None

            # Review count parsing
            raw_rev = row.get(col_reviews) or "0"
            try:
                # Remove parentheses, commas, quotes
                clean_rev = "".join(c for c in raw_rev if c.isdigit())
                review_count = int(clean_rev) if clean_rev else 0
            except Exception:
                review_count = 0

            # Scoring Rubric (0-100)
            score = 10  # baseline market presence
            no_website = (not web or web.lower() in ["", "none", "n/a", "null"])
            low_rating_active = (rating is not None and rating < 3.5 and review_count > 10)
            recent_reviews = (review_count > 15)  # inferred active engagement
            no_socials = True  # typical for unoptimized local listings

            if no_website:
                score += 30
            if low_rating_active:
                score += 20
            if recent_reviews:
                score += 15
            if no_socials:
                score += 5

            score = min(score, 100)

            # Pitches
            if no_website:
                pitch = f"High local Maps presence with 0 website. Pitch rapid Next.js landing page & appointment capture to convert mobile searchers."
            elif low_rating_active:
                pitch = f"Sub-3.5 star rating ({rating} stars with {review_count} reviews) creates customer hesitation. Pitch automated SMS review filter."
            elif rating and rating >= 4.5 and review_count > 50:
                pitch = f"High reputation ({rating} stars, {review_count} reviews) but missing automated AI chat booking to capture off-hours inquiries."
            else:
                pitch = f"Standard local presence. Pitch Google Places local SEO enhancement & automated lead qualification."

            # Outreach Compliance Evaluation
            has_business_line = bool(phone and phone != "N/A")
            # Sole trader / partnership heuristic detection
            corporate_indicators = ["inc", "llc", "corp", "ltd", "limited", "group", "holdings", "co.", "co "]
            is_corporate = any(ind in name.lower() for ind in corporate_indicators)
            sole_trader_indicators = ["handyman", "consultant", "attorney", "cpa", "freelance", "& son", "& sons", "& partner"]
            is_sole_trader = any(st in name.lower() for st in sole_trader_indicators) or (not is_corporate and len(name.split()) <= 2)

            if is_sole_trader:
                recommended_channel = "phone" if has_business_line else "in_person"
                compliance_notes = "GDPR flag: Possible sole trader / personal data risk. Exercise email caution; prefer phone or in-person outreach. Document LIA if emailing."
            elif web:
                recommended_channel = "email"
                compliance_notes = "Corporate prospect. Ensure CAN-SPAM compliant footer (physical address + working unsubscribe link) or documented legitimate interest."
            elif has_business_line:
                recommended_channel = "phone"
                compliance_notes = "Listed business line detected. TCPA compliant B2B call: identify business immediately, avoid autodialers, and honor DNC requests."
            else:
                recommended_channel = "in_person"
                compliance_notes = "No digital or verified phone channel detected. Local walk-in / in-person outreach recommended."

            has_website = not no_website
            website_url = web if (web and not no_website) else None

            prospects.append({
                "name": name,
                "address": address,
                "phone": phone,
                "place_id": None,
                "rating": rating,
                "review_count": review_count,
                "has_website": has_website,
                "website_url": website_url,
                "social_profiles": [],
                "opportunity_score": score,
                "score_breakdown": {
                    "no_website": no_website,
                    "weak_website": False,
                    "low_rating_active_volume": low_rating_active,
                    "recent_reviews": recent_reviews,
                    "no_socials": no_socials
                },
                "compliance_check": {
                    "has_business_line": has_business_line,
                    "is_sole_trader": is_sole_trader,
                    "recommended_channel": recommended_channel,
                    "compliance_notes": compliance_notes
                },
                "recommended_pitch": pitch
            })

    # Sort descending by opportunity score
    prospects.sort(key=lambda x: x["opportunity_score"], reverse=True)

    return {
        "search_category": "Local Services",
        "search_location": "Local Municipality",
        "sourcing_path_used": "csv-fallback",
        "sourcing_notes": "Ingested and scored via local CSV fallback (prospects.csv).",
        "total_found": len(prospects),
        "prospects": prospects
    }

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "prospects.csv"
    res = score_prospects(path)
    print(json.dumps(res, indent=2))
