---
name: prospect-finder
description: "Finds local business prospects using gmaps-mcp as the primary direct Google Maps scraping path, with manual CSV export as a fallback, then scores each prospect based on predefined opportunity criteria."
---

# Prospect Finder Skill (`prospect-finder`)

- **Recommended Model Tier**: `gemini-3.1-flash-lite` (Fast scoring and structured list processing; falls back to `flash`)

This skill systematically extracts local business prospects across target municipalities and industries, evaluates their digital presence, scores their service opportunity, and outputs ranked leads.

---

## 1. Input Specification

- **`category`** (`string`, required): Industry or trade (e.g., `"plumber"`, `"HVAC contractor"`, `"dental office"`).
- **`location`** (`string`, required): Target city, municipality, or region (e.g., `"Austin, TX"`, `"London, UK"`, `"Abuja, Nigeria"`).
- **`min_reviews`** (`number`, optional): Minimum review threshold to filter out inactive listings (default: `5`).
- **`max_results`** (`number`, optional): Maximum number of prospects to retrieve (default: `50`).
- **`enrich_contacts`** (`boolean`, optional): When `true`, enriches top prospects (max 5) with LinkedIn decision-maker profiles (default: `false`).
- **`read_activity`** (`boolean`, optional): When `enrich_contacts` is `true`, reads recent posts to extract pain signals and generate an `approach_strategy` (default: `false`).

---

## 2. Sourcing Paths (Dual-Path Architecture)

Always attempt **Path 1** first. Only fall back to **Path 2** if Path 1 is unreachable or yields zero results.

### Path 1 (PRIMARY) — `gmaps-mcp` MCP Server
1. Construct the query string combining category and location:
   ```
   "{category} in {location}"  (e.g., "plumbers in Austin, TX")
   ```
2. Call the `search_google_maps` tool exposed by the `gmaps` MCP server, requesting up to `max_results`.
3. For each returned place record, extract:
   - `name`: Business display name
   - `address`: Full street address
   - `phone`: Listed business phone (local or international format)
   - `website`: Website URL (if present)
   - `rating`: Star rating (1.0–5.0)
   - `review_count`: Total number of user reviews
   - `place_id`: Google Place ID identifier
   - `categories`: Listed business trade categories
   - `coordinates`: Latitude and longitude
   - `maps_url`: Direct Google Maps listing link
4. If `search_google_maps` succeeds and returns results:
   - Set `sourcing_path_used`: `"gmaps-mcp"`
   - Set `sourcing_notes`: `"Successfully retrieved {count} places via gmaps-mcp stdio server."`
   - Proceed directly to **Section 3 (Filters & Opportunity Scoring)**.
5. **Fall-Through Condition**: If the MCP call fails, the server is unreachable, or returns 0 results:
   - Log the failure reason into `sourcing_notes`.
   - Escalate to **Path 2 (Fallback)**.

### Path 2 (FALLBACK) — CSV Import
1. Prompt the user:
   > *"gmaps-mcp is unavailable or returned zero results. Please export a CSV from a browser extension (Instant Data Scraper, GeoLeadScraper, LeadGrabber, or similar) from Google Maps and save it as `prospects.csv` in the project root. Let me know when it's ready."*
2. Wait for user confirmation.
3. Once confirmed, read `prospects.csv` using `view_file` or execute the scoring script:
   ```bash
   python .agents/skills/prospect-finder/scripts/score_prospects.py prospects.csv
   ```
4. Set `sourcing_path_used`: `"csv-fallback"`.
5. Map CSV columns to the standardized prospect schema (`place_id` is set to `null`).

---

## 3. Filters

Drop records from either sourcing path that meet any of the following exclusion conditions:
1. **`review_count < min_reviews`**: Filter out abandoned or newly created zero-history listings.
2. **`rating < 2.0`**: Exclude irrecoverable or permanently toxic listings.
3. **Business status is `"closed"` or `"temporarily closed"`**: Do not pitch inactive entities.
4. **Missing phone number**: Must have a callable contact line (`phone == null` or `"N/A"` → drop).

---

## 4. Opportunity Scoring Rubric (0–100)

Apply the point additions based on observable signals:

| Condition | Points Added | Strategic Pitch Focus |
| :--- | :---: | :--- |
| **No Website Listed** | **+30** | High-converting web design, appointment booking portal, mobile optimization. |
| **Has Website but Rated "Weak" / Outdated** | **+20** | Modernization to Next.js, mobile Core Web Vitals speed repair (<2s). |
| **Recent Reviews in Last 30 Days** | **+25** | Highly active trading volume; prime candidate for automated operations. |
| **Recent Reviews in Last 90 Days** | **+15** | Confirms active business and customer engagement. |
| **Rating < 3.5 AND Review Count > 10** | **+20** | Severe reputation drag; automated post-service review recovery filter. |
| **Rating < 4.0 AND Review Count > 5** | **+12** | Consumer hesitation threshold; proactive reputation enhancement. |
| **No Social Profiles Detected** | **+5** | Omnichannel expansion and automated social presence. |
| **Customer Review Sentiment Gaps** | **+15 per match** (cap at +30) | Reviews cite "hard to find", "no website", "nobody answers phone", "slow response". |
| **Base Market Relevance** | **+10** | Baseline score for active local trading presence. |

*Total score is capped at **100**.*

---

## 5. ICP Qualification Scoring (0–100)

Evaluate each prospect against the Ideal Customer Profile defined in [`.agents/rules/icp-definition.md`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/.agents/rules/icp-definition.md):

1. **Must-Have Attribute Gate**:
   - Verified physical or local service location.
   - Review count >= 10.
   - Dedicated callable business phone line.
   *If any must-have attribute is missing, set `icp_fit_score = 0` immediately.*

2. **Disqualification Filter**:
   - National or global franchise brand.
   - Known in-house marketing/software development department.
   - Status is closed or dormant.
   *If any disqualifier matches, set `icp_fit_score = 0` immediately.*

3. **ICP Fit Scoring (for passed prospects)**:
   - Target industry alignment (Plumbing, HVAC, Electrical, Professional/Medical): **+40**
   - Independent owner-operated structure: **+30**
   - Headcount/Scale indicator (10–50 employees): **+30**
   *Total ICP fit score capped at **100**.*

4. **Combined Priority Ranking**:
   Calculate the composite score used to rank the final list:
   $$\text{combined\_score} = (\text{opportunity\_score} \times 0.6) + (\text{icp\_fit\_score} \times 0.4)$$
   Sort all prospects descending by `combined_score`.

---

## 6. Outreach Compliance Assessment

Every prospect must undergo an outreach compliance check before selecting a communication channel:
- **`has_business_line`** (`boolean`): Confirm if the phone number is a listed public business line (as opposed to a private personal mobile).
- **`is_sole_trader`** (`boolean`): Evaluate if the business listing appears to be a sole proprietor or partnership (e.g., named individual tradesperson, personal domain/inbox).
- **`recommended_channel`** (`"email"` | `"phone"` | `"in_person"`):
  - **Rule**: If the prospect appears to be a sole trader or partnership, flag it for email caution under GDPR. Prefer phone or in-person outreach.
  - If a verified business line exists and website/email is missing or personal: recommend `"phone"`.
  - If an established corporate entity with clear business channels is verified: recommend `"email"`.
  - For local walk-in businesses with high opportunity scores: recommend `"in_person"`.
- **`compliance_notes`** (`string`): Any relevant compliance alerts (e.g., *"GDPR caution: possible sole trader; avoid cold emailing personal address; prefer phone"* or *"CAN-SPAM: ensure physical address & unsubscribe link are present"*).

---

## 7. LinkedIn Contact & Activity Enrichment (Optional)

When `enrich_contacts` is set to `true`:
1. Sort qualified prospects descending by `combined_score`.
2. Select at most the **top 5 prospects** (strict rate-limit cap).
3. For each prospect:
   - Invoke the `linkedin-enrichment` skill with `company_name`, `domain`, and `read_activity`.
   - Retrieve the verified decision-maker name, headline, title, and profile URL.
   - If `read_activity` is `true`, inspect recent posts to detect operational pain points and generate an `approach_strategy`.
4. Attach the resulting `decision_maker` object directly to the prospect record.

---

## 8. Output JSON Schema

```json
{
  "search_category": string,
  "search_location": string,
  "sourcing_path_used": "gmaps-mcp" | "csv-fallback",
  "sourcing_notes": string,
  "total_found": number,
  "prospects": [
    {
      "name": string,
      "address": string,
      "phone": string,
      "place_id": string | null,
      "rating": number | null,
      "review_count": number,
      "has_website": boolean,
      "website_url": string | null,
      "social_profiles": string[],
      "opportunity_score": number,
      "icp_fit_score": number,
      "combined_score": number,
      "score_breakdown": {
        "no_website": boolean,
        "weak_website": boolean,
        "low_rating_active_volume": boolean,
        "recent_reviews": boolean,
        "no_socials": boolean
      },
      "compliance_check": {
        "has_business_line": boolean,
        "is_sole_trader": boolean,
        "recommended_channel": "email" | "phone" | "in_person",
        "compliance_notes": string
      },
      "recommended_pitch": string,
      "decision_maker": {
        "found": boolean,
        "name": string | null,
        "title": string | null,
        "headline": string | null,
        "profile_url": string | null,
        "recent_activity": {
          "posts_analyzed": number,
          "last_post_date": string | null,
          "tone": string | null,
          "pain_signals": string[],
          "recurring_themes": string[],
          "conversation_hooks": string[]
        } | null,
        "approach_strategy": {
          "opening_line": string,
          "channel_recommendation": "email" | "phone" | "linkedin",
          "timing_note": string,
          "topics_to_avoid": string[],
          "reasoning": string
        } | null
      } | null
    }
  ]
}
```

---

## 9. Output Persistence & Client Folder Setup

1. **Master Prospect Ledger**:
   - Sourced and scored leads are saved/appended to the master prospect file at `outputs/prospects_all.csv`.
2. **Client Folder Initialization**:
   - When an audit is requested for a specific prospect, compute the prospect's canonical slug using the rule in [`.agents/rules/audit-standards.md`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/.agents/rules/audit-standards.md).
   - Create `outputs/clients/<company-slug>/` if it does not already exist.
   - Initialize `conversation_log.md` (from `.agents/templates/conversation-log.md`) and `outreach_log.csv` (with header `date,prospect_name,channel,touch_number,message_excerpt,result`) if missing.

