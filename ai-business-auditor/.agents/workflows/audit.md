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

Pass the audit JSON to Step 3.

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
2. Save Markdown to `outputs/{company_name}_audit_{YYYY-MM-DD}.md`
3. Convert to PDF via Pandoc → `outputs/{company_name}_audit_{date}.pdf`
4. Do NOT publish to Notion yet. Staging only.

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
- **Local PDF path**

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
