---
name: outcome-analysis
description: "Runs a pattern analysis across all logged outreach touches in outputs/outreach_outcomes.csv to identify high-performing message angles and recommend template refinements."
---

# /outcome-analysis — Outreach Pattern Analysis Workflow

This workflow evaluates historical outreach performance data to identify conversion drivers, surface underperforming channels or messages, and suggest iterative template improvements.

---

## Trigger
The user types:
```
/outcome-analysis
```

---

## Steps

### Step 1 — Ingest & Analyze Outcomes
1. Verify `outputs/outreach_outcomes.csv` exists and contains logged touches.
2. Invoke the **`outcome-tracker`** skill in **Analysis Mode**.
3. Group data by channel, touch number, and message type to calculate conversion metrics.
4. Write the detailed analysis to `outputs/insights/outreach_insights.md`.

### Step 2 — Present Executive Insights
Present a clear summary to the user:
- Total touches recorded and active conversion rate.
- **Top 3 Highest-Performing Message Patterns**: What hooked prospects and secured replies.
- **Bottom 3 Lowest-Performing Message Patterns**: Angles resulting in ghosting or friction.
- Recommended adjustments for email, phone script, and LinkedIn sequence templates.

### Step 3 — User Checkpoint
Ask the user:
> *"Would you like me to update the outreach templates and call scripts based on these findings?"*

Wait for user direction before modifying any templates.
