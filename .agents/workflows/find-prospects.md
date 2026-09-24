---
name: find-prospects
description: "Discovers, scores, and filters local business prospects for AI consulting and audit services using gmaps-mcp as the primary search path, with CSV export as fallback."
---

# /find-prospects — Local Business Prospecting Workflow

> [!NOTE]
> **SOURCING NOTE**: The primary path uses the `gmaps-mcp` MCP server to scrape Google Maps directly without requiring API keys or browser extensions. If that server is unavailable or returns 0 results, the workflow falls back to reading a manually exported `prospects.csv` from the project root. The output includes a `sourcing_path_used` field so you always know which path produced the list.

---

## Step 0 — Input Definition
Obtain the search target from the user or slash command arguments:
- **`category`**: Target industry or trade (e.g., `"plumber"`, `"HVAC contractor"`, `"roofing"`, `"dental clinic"`).
- **`location`**: Target city or geographic area (e.g., `"Austin, TX"`, `"Manchester, UK"`, `"Abuja, Nigeria"`).
- **`min_reviews`** (optional, default `5`): Filter threshold for minimum review count.
- **`max_results`** (optional, default `50`): Maximum number of records to pull.

---

## Step 1 — Prospect Sourcing & Ingestion

Invoke the **`prospect-finder`** skill with the specified category and location:
1. **Try `gmaps-mcp` first (Path 1 - Primary)**:
   - Queries Google Maps via the `search_google_maps` MCP tool.
   - Extracts business name, full address, phone, website URL, Place ID, star rating, review count, categories, coordinates, and Google Maps URL.
2. **Fall back to CSV import if `gmaps-mcp` is unavailable (Path 2 - Fallback)**:
   - If `gmaps-mcp` is unreachable, offline, or returns 0 places, the skill prompts the user to export `prospects.csv` via a browser scraper extension.
   - Ingests `prospects.csv` and normalizes records into the standard prospect schema.

Wait for the structured prospect list.

---

## Step 2 — Opportunity Scoring & Filtering

For each prospect returned:
1. Apply the **Opportunity Scoring Rubric** (0–100):
   - No website: **+30**
   - Weak / outdated website: **+20**
   - Active reviews in last 30 days: **+25**
   - Active reviews in last 90 days: **+15**
   - Rating < 3.5 with review count > 10: **+20**
   - Rating < 4.0 with review count > 5: **+12**
   - Missing social profiles: **+5**
   - Negative sentiment / friction mentions: **+15** (cap at +30)
   - Base market presence: **+10**
2. Apply **Disqualification Filters**:
   - Discard listings with `review_count < min_reviews`.
   - Discard listings with status `"closed"` or `"temporarily closed"`.
   - Discard listings with no callable phone number.
3. Sort prospects descending by `opportunity_score`.

---

## Step 3 — Pitch Angle & Compliance Review

For each top-ranked prospect:
1. **Pitch Angle Generation**: Formulate a high-impact hook targeting the highest scoring deficiency (e.g., mobile speed bounce, zero website appointment capture, sub-4.0 review recovery, or off-hours AI receptionist).
2. **Outreach Compliance Check**:
   - Verify if phone line is a listed corporate/business line (`has_business_line`).
   - Flag sole proprietorships or partnerships (`is_sole_trader`) for GDPR email caution.
   - Assign `recommended_channel` (`"email"` | `"phone"` | `"in_person"`).
   - Verify mandatory CAN-SPAM / GDPR footer requirements before initiating contact.

---

## Step 4 — Presentation & Next Actions

Present the ranked prospects table to the user with:
- Search parameters and `sourcing_path_used` (`"gmaps-mcp"` vs. `"csv-fallback"`).
- Top prospects table (Rank, Name, Rating/Reviews, Website Status, Opportunity Score, Recommended Channel, and Pitch Hook).
- Offer next step:
  - Select any prospect to run a full 4-pillar deep diagnostic using `/audit <website_url>`.
  - Generate personalized, legally compliant outreach emails or phone scripts for top prospects.

Done.
