---
name: pipeline
description: "Generates a single markdown view of all prospects and their current status, sourced from the outputs/ CSVs."
---

# /pipeline — Commercial Pipeline Dashboard Workflow

This workflow aggregates prospecting leads, audit records, and logged outreach touches into a centralized operational dashboard, computing current lifecycle stages and highlighting overdue follow-ups.

---

## Trigger
The user types:
```
/pipeline
```

---

## Steps

### Step 1 — Ingest Pipeline Data Sources
Scan and read active tracking data from `outputs/`:
1. `outputs/prospects_all.csv` (or `prospects.csv`): Master sourced prospect lists, ratings, opportunity scores, and ICP fit scores.
2. `outputs/audit_log.csv`: Completed audits, pillar scores, and deliverable paths.
3. `outputs/outreach_outcomes.csv`: Master outreach touch history.
4. `outputs/clients/*/outreach_log.csv`: Individual per-client touch logs providing granular interaction history.

If an outcomes file does not exist, treat uncontacted prospects as having zero prior touches.

### Step 2 — Consolidate Prospect Records
Merge all records into a single consolidated view keyed by prospect name:
- Include all prospects sourced in `prospects_all.csv` and every prospect with an active client folder under `outputs/clients/<company-slug>/`.
- Extract current interaction status from the per-client `outreach_log.csv`:
  - **Prospect**: Business or entity name.
  - **Tier**: Target digital presence tier (A, B, C, or D).
  - **Opportunity Score**: 0–100 score from `prospect-finder`.
  - **ICP Fit**: 0–100 score from `icp-definition.md`.
  - **Last Touch**: Date and channel of the most recent interaction (or `"None"`).
  - **Status**: `"New"`, `"Touch 1 Sent"`, `"Touch 2 Sent"`, `"Replied"`, `"Booked"`, `"Proposal Sent"`, `"Closed"`, or `"Lost"`.
  - **Next Action**: Prescribed next commercial step.

### Step 3 — Compute Next Action Rules
Determine the appropriate next step based on touch timing and response status:
- **No touch yet**: `"Send touch 1"`
- **Touch 1 sent > 3 days ago, no reply**: **`"Send touch 2 (Overdue)"`**
- **Touch 2 sent > 5 days ago, no reply**: **`"Send touch 3 (Overdue)"`**
- **Replied, awaiting response**: **`"Respond to prospect"`**
- **Call scheduled**: `"Prepare for call"`
- **Proposal delivered**: `"Follow up on proposal"`
- **Closed / Won**: `"Deliver onboarding"`
- **Lost / Unresponsive**: `"Archive / Nurture in 90 days"`

### Step 4 — Generate and Save Pipeline Dashboard
1. Format into a GitHub Flavored Markdown table.
2. Highlight rows where Next Action is **overdue** or requires immediate response in **bold**.
3. Save the formatted dashboard to `outputs/pipeline.md`.
4. Render the dashboard directly in chat for quick review.
