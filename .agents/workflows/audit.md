---
name: audit
description: "Runs a complete AI business audit on a company URL, from enrichment through parallel pillar diagnostics to a formatted PDF report, with a human review checkpoint before any sharing."
---

# /audit — AI Business Audit Workflow

PARALLELIZATION: Step 2 is the primary parallelization point. The four pillar
audits are independent and MUST run concurrently. Do NOT run them
sequentially. A secondary parallelization point exists inside Step 1, where
Places enrichment and SEO analysis can run concurrently once the entity is
resolved.

> [!IMPORTANT]
> **SCHEDULED RUN MODE**: When this workflow is invoked by a scheduled task or batch pursuit command (and not by an interactive human session), it must:
> 1. Run all automated phases (research $\rightarrow$ parallel audit $\rightarrow$ report verification $\rightarrow$ formatting $\rightarrow$ video $\rightarrow$ call script).
> 2. Write all outputs into the dedicated client folder (`outputs/clients/{slug}/`).
> 3. Append an entry to `outputs/daily_brief.md`.
> 4. **STOP IMMEDIATELY**. Do not pause for live human review. Do not send anything. Do not contact anyone. Do not open an active conversation.
> The human review checkpoint occurs when the operator reviews `outputs/daily_brief.md`.

---

## Step -1 — CLIENT FOLDER SETUP

1. Compute the canonical slug for the target business using the rule defined in [`.agents/rules/audit-standards.md`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/.agents/rules/audit-standards.md).
2. Create `outputs/clients/{slug}/` if it does not already exist.
3. If `conversation_log.md` is missing, initialize it from `.agents/templates/conversation-log.md`.
4. If `outreach_log.csv` is missing, initialize it with:
   ```csv
   date,prospect_name,channel,touch_number,message_excerpt,result
   ```
5. If the folder already exists, reuse it without overwriting existing files.

---

## Step 0 — Input Normalization

Preprocessing, not an agent.

1. Accept the target URL from the user.
2. Strip `www.` / non-`www.` variants.
3. Extract the clean domain (e.g., `example.com`).
4. Pass the normalized domain downstream to Step 1.

---

## Step 0.5 — Capability Check (conditional)

Run ONLY if a prior step in this workflow failed or reported a missing
capability (e.g., an enrichment rung is down, a scraper is throttled, an
MCP server is unreachable).

1. Use the `find-skills` skill to search skills.sh for a community skill
   matching the unmet need.
2. Present the top 3 candidates with:
   - install count
   - security audit status (Agent Trust Hub / Socket / Snyk)
   - one-line description
3. Ask which to install before running `npx skills add`.
4. Before installing, invoke `skill-security-check` to confirm no HIGH risk
   flags. Never install a HIGH-risk skill.
5. Retry the failed step with the newly installed skill.

If nothing has failed, skip this step entirely.

---

## Step 0.7 — Data Prefetch & Local Cache Check

Before launching deep subagent diagnostics, check if local prefetch caches already exist in `outputs/clients/{slug}/`:
1. `benchmark.json` (Competitor benchmark metrics)
2. `places.json` (Google Places telemetry and sentiment)
3. `seo.json` (Search Console or third-party SEO intelligence)

If any of these files exist and are fresh (< 7 days old), load them directly to bypass redundant network/MCP tool calls and save token/API quota. If missing, they will be fetched in Step 1 and persisted to `outputs/clients/{slug}/` for downstream caching.

---

## Step 1 — Company Research

Invoke the **company-researcher** subagent.

The subagent performs the following, in order:

### 1a. Entity Resolution (enrichment ladder, sequential)
1. **Rung 1** — ENTIA MCP: resolve entity, pull firmographics.
2. **Rung 2** — Apify Firmographic Enricher: augment revenue / employee / HQ.
3. **Rung 3** — OpenCorporates: legal entity fallback.
Escalate to the next rung only if the current one returns insufficient data.

### 1b. Fallback Scraping (scraper ladder, only if 1a is thin)
1. **Rung 1** — ai-first-search
2. **Rung 2** — Spectrawl
3. **Rung 3** — Crawl4AI

### 1c. Places + SEO (PARALLEL — these two are independent)
Once the entity is resolved in 1a, spawn BOTH concurrently:

- **Places enrichment** — invoke the `places-enrichment` skill using the
  resolved company name and any location data. Produces `places_data`
  (address, phone, rating, review count, review sentiment, match confidence).

- **SEO analysis (Branching)**:
  Check whether the domain matches a verified property via Search Console `list_sites`:
  - **IF verified in GSC**:
    Invoke **`seo-analyst-gsc`** to extract live 90-day search actuals (clicks, impressions, CTR, position, crawl issues).
  - **ELSE (Cold Prospects, Competitors, Non-Owned Domains)**:
    Invoke **`seo-analyst-prospect`** to pull third-party search intelligence across the ladder (SE Ranking → FetchSERP → Ahrefs DR → PageSpeed Insights → Common Crawl).
  
  Both branches produce structured `seo_data` (top keywords, quick-win opportunities, performance/CWV metrics, SEO score with reasoning scaffold).

Wait for both to complete.

### 1d. Technographics (sequential, after 1a)
Scrape the careers page, engineering blog, job listings, and footer credits.
INFER the tech stack. Flag every item with a confidence level
(`high` | `medium` | `low`) and cite the source.

### 1e. Assemble the profile JSON
Merge everything into a single profile with keys:
`company_name`, `domain`, `revenue_range`, `employee_count`, `locations`,
`industry`, `technographics`, `places_data`, `seo_data`,
`data_sources_used`, `failed_sources`, `rate_limit_events`.

Pass this profile to Step 2.

---

## Step 2 — Business Audit (PARALLEL)

Invoke the **business-auditor** subagent.

The subagent performs the following:

### 2a. Spawn four pillar-auditor subagents CONCURRENTLY
Use `invoke_subagent` four times in parallel. Each receives:

- the **SAME full company profile JSON** in its initial prompt
  (context does NOT inherit — this must be passed explicitly)
- a **DIFFERENT assigned pillar**:

| Subagent | Pillar |
|---|---|
| pillar-auditor #1 | Sales & Marketing |
| pillar-auditor #2 | Customer Support |
| pillar-auditor #3 | Product & Service Delivery |
| pillar-auditor #4 | Internal Operations & Infrastructure |

Each pillar-auditor:
- Produces current state, gaps, proposed AI leverage
- Runs the mandatory reasoning scaffold (evidence → expected → gap → score)
- Returns a 1-10 score with rationale

**Pillar 1 special handling:** If the profile contains `seo_data` with
`skipped: false`, incorporate the SEO findings into the Sales & Marketing
assessment (reference specific quick-win queries in gaps, declining pages
in evidence). If `places_data` is present, incorporate the rating and
review sentiment into the reputation portion.

### 2b. Wait for all four to complete

### 2c. Synthesize
Merge the four pillar outputs into:
- Executive Summary (overview, unforced errors, high-leverage AI opportunities)
- Scoring Matrix (one entry per pillar, each with score + rationale)
- Domain Deep Dives (four sections, one per pillar)
- Roadmaps: Quick Wins / 3-6 month strategic / phased 30-60-90 day

Pass the audit JSON to Step 2.5.

---

## Step 2.5 — Report Verification (Quality Gate)

Invoke the **report-verifier** subagent (`model: pro`) with the consolidated audit JSON.

1. The verifier executes all 6 quality checks:
   - **Consistency**: No contradictions across pillars.
   - **Sourcing**: Every factual claim traces to `data_sources_used`.
   - **Rationale**: Scores cite specific evidence, not generic consulting statements.
   - **Reasoning Scaffold**: Complete four-step scaffold on every pillar score.
   - **Technographics**: Every tool has confidence flag and evidentiary citation.
   - **Numeric Integrity**: Metrics match profile data exactly.
2. **Evaluation & Correction Loop**:
   - If verdict is `"fail"`, loop back to Step 2 (`business-auditor`) with the issues list for correction.
   - A maximum of **2 correction loops** are permitted.
   - If unresolved issues remain after 2 loops, proceed to Step 3 with flagged items noted in the report appendix.
   - If verdict is `"pass"`, pass the validated audit JSON to Step 3.

---

## Step 3 — Report Formatting

Invoke the **report-formatter** subagent.

1. Render the audit JSON → Markdown with sections:
   - Executive Summary
   - Scoring Matrix (table)
   - Domain Deep Dives
   - Roadmaps
   - Data Sources Used + Rate Limit Notes
   - Technographics (with confidence flags)
   - Google Places data (with match confidence)
   - SEO findings (or a note explaining why SEO was skipped)
2. Save Markdown to `outputs/clients/{slug}/audit_{YYYY-MM-DD}.md`
3. Convert to PDF via Pandoc → `outputs/clients/{slug}/audit_{date}.pdf`
---

## Step 3.5 — VIDEO GENERATION (Optional)

If the user ran the audit with the `--video` flag:
1. Invoke the `video-generator` skill with the prospect's website URL and the executive summary from the audit JSON.
2. Wait for the video file to be generated at `outputs/clients/{slug}/walkthrough.mp4`.
3. Present the video path in the human review checkpoint (Step 4).

If the `--video` flag was not passed, skip this step entirely.

---

## Step 3.6 — Google Sheets Pipeline Sync

Invoke the **sheet-writer** skill to log or update this prospect's automated intelligence in the live Google Sheet ("Outreach Pipeline"):
1. Read `.agents/rules/sheet-config.md` for target spreadsheet configuration.
2. Find the first empty row or match the existing prospect row.
3. Write automated audit data contiguously into columns A–K:
   - Col A: Business Name
   - Col B: Location
   - Col C: Opportunity Score
   - Col D: Tier (`Tier A` | `Tier B` | `Tier C` | `Tier D`)
   - Col E: Audit PDF Link
   - Col F: Video Walkthrough Link
   - Col G: Call Script Link
   - Col H: Suggested Opening Line
   - Col I: Contact Name
   - Col J: Contact Title
   - Col K: LinkedIn Profile URL (or empty string if null)
4. **Strict Boundary Enforcement**: NEVER write or touch columns L–R (reserved exclusively for manual user tracking).
5. If Google Sheets MCP is unavailable or returns an error, log to `outputs/clients/{slug}/sync_status.json` and proceed cleanly without blocking the audit.

---

## Step 4 — Human Review Checkpoint

**PAUSE.** Do NOT proceed without explicit user confirmation.

Present to the user:

- **Executive summary** (from the audit JSON)
- **Scoring matrix** — pillar, score, one-line rationale per pillar
- **Data sources used** and any `rate_limit_events` or `failed_sources`
- **Technographics confidence summary** — how much was verified vs. inferred
- **Places data status** — match confidence (high/medium/low) or "not found"
- **SEO data status**:
  - Path utilized: `Verified GSC` (first-party actuals) vs. `Third-Party Prospect` (modeled estimates)
  - Data tier: `data_source_tier` (e.g., SE Ranking, FetchSERP, PageSpeed Insights + Ahrefs DR)
  - Data confidence note: highlights whether metrics represent actual search telemetry or estimated third-party crawler models
- **Compliance summary**:
  - For each prospect: recommended outreach channel (`email` | `phone` | `in_person`)
  - Any GDPR flags (sole trader, partnership, or EU-based personal data risk)
  - Confirmation that the outreach email footer includes the required CAN-SPAM elements (valid physical postal address + functioning unsubscribe link)
- **Local PDF path**
- **Walkthrough video path** (if `--video` flag was passed)

Ask: **"Approve, publish a shareable link, or revise?"**

Do NOT publish, export, or share anything until the user responds.

---

## Step 5 — Export (on confirmation)

On user confirmation:

1. If Notion is configured: publish the report as a Notion page, return the
   shareable URL.
2. Otherwise: confirm the local PDF is the final deliverable.
3. Append a log entry to `outputs/audit_log.csv` with: company name, date,
   four pillar scores, overall score, PDF path, SEO status, Places status.
4. (If hooks are active) The `PostToolCallHook` will have already logged
   every enrichment call to `outputs/enrichment_log.jsonl`.

Done.
