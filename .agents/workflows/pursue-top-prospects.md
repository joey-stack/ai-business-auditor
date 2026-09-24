---
name: pursue-top-prospects
description: "Reads the scored prospect list, selects the top N by combined opportunity and ICP score, and runs the full audit pipeline on each. Produces ready-to-send deliverables but never contacts anyone."
---

# /pursue-top-prospects — Top-N Batch Pursuit Workflow

This workflow automates discovery, prioritization, and deep diagnostic audit generation for the highest-ranked $N$ local prospects. It generates complete, ready-to-dispatch client dossiers (profile, audit report, PDF, call script, walkthrough video) without making external contact.

---

## Trigger
The user types:
```bash
/pursue-top-prospects --count <N> --category "<category>" --location "<location>"
```
*(Example: `/pursue-top-prospects --count 20 --category "plumber" --location "Austin, TX"`)*

---

## Steps

### Step 0 — Parse Arguments
1. Read `--count` (integer, default: `20`), `--category` (string), and `--location` (string) from the invocation arguments.
2. If `--category` or `--location` is omitted:
   - Check [`.agents/rules/icp-definition.md`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/.agents/rules/icp-definition.md) for target industry and primary geography.
   - If still undetermined, prompt the user for input before proceeding.

### Step 1 — Source and Score Prospects
1. Invoke the **`prospect-finder`** skill with:
   - `category`: Target industry
   - `location`: Target city/region
   - `max_results`: At least $\max(50, N \times 2)$ to guarantee adequate candidate depth
2. Receive the scored JSON array containing `opportunity_score` and `icp_fit_score`.

### Step 2 — Select Top N Prospects
1. Sort the qualified prospect list descending by `combined_score`:
   $$\text{combined\_score} = (\text{opportunity\_score} \times 0.6) + (\text{icp\_fit\_score} \times 0.4)$$
   *(Fallback: If `icp_fit_score` is missing or uncalculated, sort strictly by `opportunity_score` alone and note the fallback in the log).*
2. Extract the top $N$ records (strict cap: never exceed $N$).
3. Ensure `outputs/selection_log.csv` exists with headers:
   ```csv
   date,prospect_name,score,rank,reason_selected
   ```
4. Append each selected prospect row to `outputs/selection_log.csv`.

### Step 3 — Batch Audit Execution (Loop with Hard Cap $N$)
For each of the $N$ selected prospects:
1. **Client Setup**:
   - Compute the canonical slug using the rule in [`.agents/rules/audit-standards.md`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/.agents/rules/audit-standards.md).
   - Create `outputs/clients/<company-slug>/` if it does not exist.
   - Initialize `conversation_log.md` and `outreach_log.csv` if missing.
2. **Execute Audit in Scheduled Run Mode**:
   - Invoke `/audit <website_url>` under **SCHEDULED RUN MODE**:
     - Complete entity resolution, Places telemetry, and competitor benchmarking.
     - Spawn parallel 4-pillar audits.
     - Validate via `report-verifier`.
     - Compile Markdown and PDF to `outputs/clients/<company-slug>/audit_{date}.pdf`.
     - Generate phone decision tree to `outputs/clients/<company-slug>/call_script.md`.
     - Record video walkthrough to `outputs/clients/<company-slug>/walkthrough.mp4` (if configured).
   - **Hard Stop Enforcement**: Stop after compiling local artifacts. Do NOT transmit outreach copy, make calls, or message anyone.
3. **Daily Brief Update**:
   - Append a row for this completed audit into `outputs/daily_brief.md`.
4. **Google Sheets Sync**:
   - Invoke the `sheet-writer` skill to record this prospect into the live Google Sheet ("Outreach Pipeline") columns A–J.
   - Strictly leave columns K–Q untouched. If Google Sheets API fails, log and continue.

#### Loop Controls & Resilience:
- **Individual Failure**: If an individual prospect audit encounters an error (e.g. invalid website), log the failure reason into `outputs/selection_log.csv` and proceed to the next prospect.
- **Rate-Limit Event**: If `gmaps-mcp` or an enrichment provider returns HTTP 429 throttling or rate-limit saturation, **immediately HALT the batch loop** and log the stopping point. Never retry aggressively.
- **Hard Cap**: Terminate execution immediately upon reaching $N$ iterations.

### Step 4 — Batch Summary Generation
Compile an operational run summary saved to `outputs/batch_summary_{YYYY-MM-DD}.md`:
- Total prospects sourced from Google Maps.
- Total prospects audited successfully.
- Any failed prospects or rate-limited events.
- Clickable links to every populated client folder under `outputs/clients/`.
