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

            prospects.append({
                "name": name,
                "address": address,
                "phone": phone,
                "website": web if web else None,
                "rating": rating,
                "review_count": review_count,
                "opportunity_score": score,
                "score_breakdown": {
                    "no_website": no_website,
                    "low_rating_active_volume": low_rating_active,
                    "recent_reviews": recent_reviews,
                    "no_socials": no_socials
                },
                "recommended_pitch": pitch
            })

    # Sort descending by opportunity score
    prospects.sort(key=lambda x: x["opportunity_score"], reverse=True)

    return {
        "total_found": len(prospects),
        "prospects": prospects
    }

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "prospects.csv"
    res = score_prospects(path)
    print(json.dumps(res, indent=2))
