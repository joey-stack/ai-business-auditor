"""
Google Places API (New) Query Script
Queries Google Places API (New) via REST with automatic fallback and .env loading.
Usage: python query_places.py "Company Name" ["Location / Domain"]
"""
import os
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path

def load_env():
    # Attempt to load .env from workspace root or current dir
    search_paths = [
        Path.cwd() / ".env",
        Path(__file__).resolve().parents[4] / ".env",
        Path(__file__).resolve().parents[3] / ".env",
        Path(__file__).resolve().parents[2] / ".env",
    ]
    for p in search_paths:
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        if k.strip() not in os.environ:
                            os.environ[k.strip()] = v.strip()
            break

def search_places(query_text):
    load_env()
    api_key = os.environ.get("GOOGLE_PLACES_API_KEY", "").strip()
    if not api_key:
        return {
            "error": "GOOGLE_PLACES_API_KEY is not set.",
            "skipped": True
        }

    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.nationalPhoneNumber,places.websiteUri,places.rating,places.userRatingCount,places.regularOpeningHours,places.reviews"
    }
    payload = json.dumps({"textQuery": query_text}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            places = res_data.get("places", [])
            if not places:
                return {
                    "matched_name": query_text,
                    "place_id": None,
                    "rating": None,
                    "review_count": 0,
                    "match_confidence": "low",
                    "note": "No place found for query."
                }
            
            p = places[0]
            reviews = p.get("reviews", [])
            recent_reviews_summary = "No reviews available."
            if reviews:
                snippets = [r.get("text", {}).get("text", "")[:120] for r in reviews[:3] if r.get("text", {}).get("text")]
                if snippets:
                    recent_reviews_summary = " | ".join(snippets)

            return {
                "place_id": p.get("id"),
                "matched_name": p.get("displayName", {}).get("text", query_text),
                "formatted_address": p.get("formattedAddress", "N/A"),
                "phone": p.get("nationalPhoneNumber", "N/A"),
                "website": p.get("websiteUri", "N/A"),
                "rating": p.get("rating"),
                "review_count": p.get("userRatingCount", 0),
                "opening_hours": p.get("regularOpeningHours", {}).get("weekdayDescriptions", []),
                "recent_reviews_summary": recent_reviews_summary,
                "match_confidence": "high" if p.get("websiteUri") else "medium"
            }
    except Exception as e:
        return {
            "error": str(e),
            "skipped": True
        }

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Googleplex"
    result = search_places(q)
    print(json.dumps(result, indent=2))
