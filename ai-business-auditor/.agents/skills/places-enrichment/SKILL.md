---
name: places-enrichment
description: "Fetches business location, contact, hours, rating, and review data from the Google Places API for a given business name or address. Use when a company profile needs verified location and reputation data."
---

# Google Places Enrichment Skill (`places-enrichment`)

This skill enriches a target business profile with physical location, contact metadata, operational hours, and public reputation intelligence using the Google Places API (New) or the Google Places MCP server.

---

## 1. Input Specification
- **Required**: `business_name` (Company trade name or legal entity name).
- **Optional**: `location` (Headquarters city, region, or country identified from firmographic profiling).
- **Optional**: `domain` (Target website domain to cross-validate matched place URL).

---

## 2. Enrichment Workflow

### Step 1: Query Places MCP Server
1. Call the Google Places MCP tool `places_text_search`:
   - Query: `"{business_name} {location}"`.
2. Inspect the candidate matches.

### Step 2: Match Selection & Confidence Scoring
Corroborate candidate entity attributes against the known company profile:
- `high`: Verified exact company name match AND matching website domain/subdomain.
- `medium`: Matching company name and confirmed headquarters city, but website not explicitly listed on the place profile.
- `low`: Generalized match on business name in an uncorroborated municipality or partial name ambiguity.

### Step 3: Extract Place Details
Pull the core firmographic and reputation attributes:
- `place_id`: Google Place identifier.
- `formatted_address`: Full physical address.
- `phone`: Primary business telephone number.
- `website`: Canonical website URL listed on Google Maps.
- `rating`: Overall Google star rating (1.0 to 5.0).
- `review_count`: Total count of public user reviews.
- `opening_hours`: Regular business operating hours.
- Extract the 5 most recent reviews and summarize customer sentiment (positive highlights vs recurring friction points).

---

## 3. Direct API Fallback (If MCP Server is Offline)
If the Google Places MCP server is unavailable, returns a 429/500 status, or transport fails:
1. Fall back to a direct Places API (New) call using Python or curl via `run_command`.
2. Ensure the `GOOGLE_PLACES_API_KEY` environment variable is present.
3. Make an HTTP POST request to:
   ```http
   POST https://places.googleapis.com/v1/places:searchText
   Content-Type: application/json
   X-Goog-Api-Key: $GOOGLE_PLACES_API_KEY
   X-Goog-FieldMask: places.id,places.displayName,places.formattedAddress,places.nationalPhoneNumber,places.websiteUri,places.rating,places.userRatingCount,places.regularOpeningHours,places.reviews
   ```
   Payload:
   ```json
   {
     "textQuery": "{business_name} {location}"
   }
   ```
4. If billing is not enabled or the API key is missing, log the event to `failed_sources` and return `null`.

---

## 4. Output JSON Schema

```json
{
  "place_id": string,
  "matched_name": string,
  "formatted_address": string,
  "phone": string,
  "website": string,
  "rating": number,
  "review_count": number,
  "opening_hours": [string],
  "recent_reviews_summary": string,
  "match_confidence": "high" | "medium" | "low"
}
```
