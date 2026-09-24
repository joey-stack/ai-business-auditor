---
name: sync-pipeline
description: "Reads the Outreach Pipeline Google Sheet, pulls the user's manual status updates (columns L–R), and updates the local per-client outreach logs accordingly."
---

# /sync-pipeline — Google Sheet Status Synchronization Workflow

This workflow pulls manual outreach interactions, contact dates, responses, and stage updates made by the human operator in the live Google Sheet back into the local client logs and commercial pipeline dashboard.

---

## Trigger
The user types:
```bash
/sync-pipeline
```

---

## Steps

### Step 1 — Read Live Outreach Sheet
1. Read the Sheet ID from [`.agents/rules/sheet-config.md`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/.agents/rules/sheet-config.md).
2. Call the Google Sheets MCP `read-values` tool to retrieve all populated rows across columns A through R on the "Outreach Pipeline" sheet.

### Step 2 — Reconcile Local Client Logs
For each row in the sheet:
1. Extract the business name from Column A and compute its canonical slug.
2. Check the user-managed status in Column L (e.g. `Touch 1 Sent`, `Replied`, `Call Scheduled`, `Closed`, `Lost`) and any touch notes in Columns M–R.
3. If Column L is populated and represents new or modified information compared to `outputs/clients/{slug}/outreach_log.csv`:
   - Append an updated record to `outputs/clients/{slug}/outreach_log.csv`.
   - Also append the latest touch to master `outputs/outreach_outcomes.csv`.

### Step 3 — Regenerate Commercial Pipeline Dashboard
1. Re-run the aggregation logic in [`.agents/workflows/pipeline.md`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/.agents/workflows/pipeline.md).
2. Update and save `outputs/pipeline.md`.

### Step 4 — Summary & Overdue Alert Report
Present a summary in chat:
- Number of rows read from the live Google Sheet.
- Number of client records updated locally.
- Specific list of prospects where the next follow-up action is **overdue**.
