---
name: outcome-tracker
description: "Records the result of every outreach touch (email, call, LinkedIn DM) to outputs/outreach_outcomes.csv, and runs a weekly pattern analysis that identifies which messages, openings, and objection responses drive replies. Use after every outreach attempt and weekly for analysis."
---

# Outcome Tracker Skill (`outcome-tracker`)

- **Recommended Model Tier**: `gemini-3.1-flash-lite` (Lightweight pattern analysis and CSV updates; falls back to `flash`)

This skill maintains a continuous feedback loop for outreach touches, recording touch outcomes to a persistent ledger and conducting pattern analyses to surface high-converting hooks and underperforming outreach approaches.

---

## 1. Operating Modes

The skill functions in two distinct modes:

### A. Recording Mode (Runs after each touch)
1. Ingest touch parameters:
   - `date`: ISO timestamp (e.g. `2026-09-18`)
   - `prospect_name`: Target business or contact name
   - `channel`: `"email"` | `"phone"` | `"linkedin"` | `"in_person"`
   - `touch_number`: Touch sequence index (`1`, `2`, `3`, etc.)
   - `message_excerpt`: Short excerpt or subject line/opening hook used
   - `result`: `"no_reply"` | `"replied"` | `"positive"` | `"negative"` | `"booked"` | `"closed"` | `"lost"`
2. Verify persistence at `outputs/outreach_outcomes.csv`. If the file does not exist, initialize it with headers:
   ```csv
   date,prospect_name,channel,touch_number,message_excerpt,result
   ```
3. Append the formatted row to `outputs/outreach_outcomes.csv`.
4. Compute the client slug for the prospect. If the client folder `outputs/clients/<company-slug>/` exists (or is initialized):
   - Check if `outputs/clients/<company-slug>/outreach_log.csv` exists; if not, initialize with the same header.
   - Append the formatted touch row to `outputs/clients/<company-slug>/outreach_log.csv`.

---

### B. Analysis Mode (Runs weekly or via `/outcome-analysis`)
1. Read the full `outputs/outreach_outcomes.csv` ledger (or aggregate from `outputs/clients/*/outreach_log.csv`).
2. Group records by:
   - `channel`
   - `touch_number`
   - `message_type` / hook category
3. Compute metrics:
   - Total touches per segment
   - Total replies and positive responses
   - Reply rate percentage per group
4. Identify the **Top 3 Highest-Performing Message Patterns** (highest positive reply rates).
5. Identify the **Bottom 3 Lowest-Performing Patterns** (highest no-reply/negative drop-offs).
6. Generate an executive insights deliverable saved to `outputs/insights/outreach_insights.md` with concrete recommendations for template adjustments.

---

## 2. Output Schema (Analysis Mode)

```json
{
  "total_touches_analyzed": number,
  "overall_reply_rate": number,
  "top_performing_patterns": [
    {
      "pattern": string,
      "channel": string,
      "reply_rate": number,
      "why_it_works": string
    }
  ],
  "lowest_performing_patterns": [
    {
      "pattern": string,
      "channel": string,
      "reply_rate": number,
      "remediation": string
    }
  ],
  "recommended_template_updates": [string]
}
```

---

## 3. Governance Constraints

- All outreach outcomes must be logged after every touch. Untracked outreach is not permitted.
- Recording mode must never overwrite existing historical rows.
- Analysis mode must require at least 5 logged touch events before asserting statistically grounded conclusions.
