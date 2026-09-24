---
name: prospect-finder
description: "Finds local business prospects by guiding the user through a free, manual Google Maps scraping process using a browser extension, then scores each prospect based on predefined criteria."
---

# Prospect Finder Skill (`prospect-finder`)

This skill guides the user through collecting local business prospects using free browser extensions on Google Maps, then systematically evaluates, scores, and ranks them by service opportunity.

---

## 1. Purpose

Enable zero-cost client acquisition and prospecting for AI agency and consulting services by extracting unoptimized local businesses (e.g., missing websites, low ratings, missing social channels) from Google Maps and generating high-conversion pitch angles.

---

## 2. Step-by-Step Execution Workflow

### Step 1: Extension Guidance
Prompt the user to install a free, zero-login Google Chrome or Chromium scraping extension:
- **Primary Recommendation**: **Instant Data Scraper** (Chrome Web Store) or **GeoLeadScraper** / **LeadGrabber**.
- Instruct the user to ensure the extension icon is pinned to their browser toolbar.

### Step 2: Target Search on Google Maps
Instruct the user to navigate to [Google Maps](https://www.google.com/maps) and search for a targeted industry and municipality:
- *Example Searches*:
  - `"Plumbers in Austin, TX"`
  - `"HVAC contractors in Chicago, IL"`
  - `"Real estate agencies in Abuja, Nigeria"`
  - `"Dental clinics in Manchester, UK"`
- Tell the user to scroll through the left results panel to load at least 20–50 businesses.

### Step 3: Export to `prospects.csv`
1. Instruct the user to click the scraper extension icon to automatically detect the table columns (Business Name, Address, Phone, Website, Rating, Review Count).
2. Instruct the user to click **"CSV"** to download the results.
3. Ask the user to save the file into the project root or workspace as:
   ```
   prospects.csv
   ```

### Step 4: Ingestion & Scoring
Once the user confirms `prospects.csv` is saved:
1. Read `prospects.csv` from the workspace using `view_file` or execute the bundled scoring script:
   ```bash
   python .agents/skills/prospect-finder/scripts/score_prospects.py prospects.csv
   ```
2. Apply the **Opportunity Scoring Rubric** (0–100) to each business.

---

## 3. Opportunity Scoring Rubric (0–100)

| Condition | Points Added | Strategic Rationale |
| :--- | :---: | :--- |
| **No Website Listed** | **+30** | Direct opportunity to pitch high-converting web design & modern Next.js development. |
| **Rating < 3.5 AND Review Count > 10** | **+20** | Active business suffering severe reputation drag; prime candidate for automated review recovery. |
| **Recent Reviews (Last 90 Days)** | **+15** | Confirms business is actively trading and receiving customer traffic. |
| **No Social Profiles Detected** | **+5** | Opportunity to pitch omnichannel presence and social automation. |
| **Base Market Relevance** | **+10** | Baseline score for active local trading presence. |

---

## 4. Pitch Angle Generation

For each scored prospect, synthesize a high-impact outreach angle based on the highest point contributor:
- **No Website (+30)**: *"We noticed your Google Maps profile has strong local traffic but no website link. You are losing 40%+ of mobile callers who want to see pricing before dialing. We can deploy a high-speed web portal in under 5 days."*
- **Rating < 3.5 (+20)**: *"Your Google rating currently sits at [X.X] stars. In your trade, 73% of customers will not call a contractor under 4.0. We implement an automated post-service SMS review filter that repairs star ratings within 30 days."*
- **No Direct Chat / Off-Hours Leakage**: *"We noticed your business receives calls after 5:00 PM when nobody is available. An AI receptionist can qualify jobs and book estimates into your calendar 24/7."*

---

## 5. Output JSON Schema

```json
{
  "total_found": number,
  "prospects": [
    {
      "name": string,
      "address": string,
      "phone": string,
      "website": string | null,
      "rating": number | null,
      "review_count": number,
      "opportunity_score": number,
      "score_breakdown": {
        "no_website": boolean,
        "low_rating_active_volume": boolean,
        "recent_reviews": boolean,
        "no_socials": boolean
      },
      "recommended_pitch": string
    }
  ]
}
```
