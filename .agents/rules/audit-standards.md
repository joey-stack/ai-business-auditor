---
description: "Core operational standards, ethical constraints, scoring rules, parallel execution requirements, and human-in-the-loop safeguards for all business audits."
trigger: always_on
---

# Audit Standards & Operational Constraints

All agents operating within the AI Business Auditor system must strictly adhere to the following governance rules and behavioral boundaries.

---

## 1. Ethical Data Sourcing & Privacy

1. **Public Information Exclusively**:
   - Only publicly accessible internet data, official open corporate registries, public job listings, and published marketing materials may be accessed or analyzed.
   - Never attempt to bypass authentication screens, access private intranets, or crawl behind gated customer portals.
2. **Strict Paywall Respect**:
   - Never scrape, bypass, or attempt to extract content from paywalled news or business intelligence services (e.g., Bloomberg, Wall Street Journal, Financial Times, paywalled industry databases).
3. **Resilient Failure Logging & Ladder Escalation**:
   - If a target data source, MCP server, or endpoint is unreachable, offline, or returns an error (such as a 429 rate limit or 404 entity miss), immediately log the incident in `failed_sources` or `rate_limit_events`.
   - **Escalate to the NEXT RUNG of the enrichment ladder instead of retrying the failed endpoint**. Never abort an entire audit due to a single data source outage.

---

## 2. Inferred Data & Technographics Governance

1. **Mandatory Confidence Labeling**:
   - No free tool provides verified real-time technographics. Technographic data must be inferred from primary artifacts (job requirements, engineering blog posts, developer docs, footer scripts).
   - Every inferred tool or platform **MUST** be explicitly categorized with a confidence rating:
     - `high`: Verified from primary technical job postings or official technical documentation published directly by the company.
     - `medium`: Inferred from public open-source repos, developer profiles, or common frontend script tags.
     - `low`: Inferred from generalized ecosystem alignment or secondary indicators.
2. **Zero Factual Misrepresentation**:
   - Inferred items must **never** be presented as verified, empirical fact in any output deliverable.
   - Every technographic entry must explicitly cite its evidentiary source (e.g., `"source": "Senior Backend Engineer job posting on /careers"`).

---

## 3. Diagnostic Rigor & Scoring Standards

1. **Actionable & Context-Specific Guidance**:
   - Generic consulting clichés (e.g., "Implement AI to improve efficiency", "Upgrade CRM") are strictly prohibited.
   - Every recommendation must directly reference the company's verified scale, target customer profile, detected tech stack, and observable friction points.
2. **Mandatory Reasoning Scaffold (Evidence → Expected → Gap → Score)**:
   - In the 4-Pillar Scoring Matrix (Sales & Marketing, Customer Support, Product Delivery, Internal Operations), every score from 1 to 10 **MUST** be preceded by the four-step reasoning scaffold:
     - **Step A — Evidence**: Cite specific data points and signals directly observed in the company profile.
     - **Step B — Expected State**: Define the expected operational benchmark for an enterprise of this scale and sector.
     - **Step C — Gap Description**: Measure the operational distance between observed state and expected state.
     - **Step D — Score**: Derive the final numerical score (1-10) directly from the gap magnitude.
   - An unsupported numerical score without this written rationale is considered an invalid audit output.
3. **Named Competitive Benchmarking**:
   - The diagnostic must benchmark the company against **2 to 3 specifically named, active competitors** in the same market or sector.
4. **Dollarized Financial Impact & Revenue Leakage Modeling (McKinsey / Big-4 Standard)**:
   - Technical and operational friction must never remain purely qualitative. Every audit deliverable **MUST** translate identified bottlenecks into an estimated dollar range of monthly and annual revenue or margin leakage.
   - Economic models must ground their formulas in observable volume (e.g., website visitors, review shortfall vs. local competitors, estimated dispatch ticket size, or manual administrative hours):
     $$\text{Estimated Leakage} = \text{Observable Volume} \times \text{Conversion Delta / Bounce Penalty} \times \text{Average Ticket Size}$$
   - Clearly label all modeled figures as calibrated operational estimates to maintain factual integrity.
5. **Deloitte-Style Effort vs. Impact Prioritization Matrix**:
   - Every transformation roadmap must include a structured executive matrix evaluating recommended initiatives across:
     - **Implementation Effort & Complexity** (`Low`, `Medium`, `High`)
     - **Estimated Setup / Tooling Cost ($)**
     - **Projected 90-Day Gross Value Recovery ($)**
     - **Projected Payback Horizon** (e.g., `< 14 Days`, `< 30 Days`)
6. **Minto Pyramid Action Titles**:
   - All pillar diagnostic headings and key findings must lead with conclusion-driven **Action Titles** (stating the operational and financial impact) rather than static topic labels.

---

## 4. Multi-Agent Orchestration & Parallelization Rules

1. **Mandatory Parallel Execution**:
   - The four pillar audits (Sales & Marketing, Customer Support, Product & Service Delivery, Internal Operations & Infrastructure) are independent domains and **MUST run concurrently in parallel**.
   - The parent `business-auditor` subagent must spawn all four `pillar-auditor` subagents simultaneously via `invoke_subagent`. Sequential execution of the four pillars is prohibited.
2. **Explicit Context Isolation & Passing**:
   - Subagents **do not inherit the parent's conversation history**.
   - The full company profile JSON and the assigned pillar name **MUST be passed explicitly** in the initial prompt to each `pillar-auditor` instance.

---

## 5. Rate Limit Management

1. **Free-Tier Protection**:
   - Respect strict rate limits on all free-tier MCP servers and scraping endpoints (e.g., ENTIA TRACE tier 100 req/mo, Apify monthly credits, OpenCorporates query caps).
2. **Audit Logging**:
   - Any rate-limiting, 429 status code, or throttling event encountered during an audit must be logged in `rate_limit_events` within the audit record.

---

## 6. Human-in-the-Loop Gatekeeping (Mandatory)

1. **Prohibition of Autonomous Publication**:
   - Under no circumstances may an agent publish, email, upload, or externally share an audit report (including creating shareable Notion pages or Google Drive links) without explicit, interactive human confirmation.
2. **Verification Checkpoint**:
   - Once the local Markdown and PDF artifacts are compiled, the pipeline must pause and present an executive summary, the scoring table, data sources used, and local artifact paths to the user.
   - Only when the human operator replies with explicit confirmation may export or cloud sharing proceed.

---

## 7. Skills.sh Community Skills & Security Governance

1. **Dynamic Capability Discovery**:
   - When encountering a task or friction point that the project's existing skills do not cover, use the `find-skills` skill to search `skills.sh` for a community skill that fulfills the capability requirement.
2. **Mandatory Security Audit Verification**:
   - **Never install a community skill without verifying its security audit first**.
   - Before installing any third-party skill, inspect its automated security audit results (Agent Trust Hub, Socket, Snyk) on its `skills.sh` detail page or via the `skills.sh` API using `skill-security-check`.
   - **Zero Tolerance for High Risk**: Skills flagged as **HIGH risk** in any category are strictly prohibited from installation. Report the finding and propose a safe alternative.

---

## 8. Google Search Console & Google Places Governance

1. **Search Console Access Boundary**:
   - Google Search Console data may **only** be queried for properties the authenticated Google account has verified ownership or delegated access to. Never attempt to query or fabricate telemetry for arbitrary domains.
   - If a target domain is not present in `list_sites`, the SEO analysis step must cleanly skip with an explicit rationale (`"property not verified for this account"`). Never fabricate or guess SEO performance data.
2. **Places API Confidence & Verification**:
   - All Google Places API results must include an explicit `match_confidence` flag (`high`, `medium`, `low`).
   - If match confidence is `low`, the Places metadata must be highlighted as unverified in the diagnostic report.
3. **Places API Billing Requirement**:
   - The Google Places API requires an active billing account linked to the Google Cloud project, even though Google provides $200/month in recurring free credits. Agents must log this prerequisite prominently and handle missing billing / quota errors gracefully without failing the overall audit.

---

## 9. Third-Party SEO Prospecting Governance (Non-Owned Domains)

1. **Strict Source Separation**:
   - SEO data for non-owned prospect domains must come exclusively from third-party intelligence providers (SE Ranking, FetchSERP, Ahrefs DR, PageSpeed Insights, Common Crawl). Never attempt an unauthorized Google Search Console call for a prospect, which will fail with an HTTP 403 Forbidden error.
2. **Mandatory Data Source Tier Attribution**:
   - Every prospect SEO assessment must explicitly specify a `data_source_tier` field indicating the exact ladder rung reached and APIs queried.
3. **Factual Integrity & Estimation Disclaimers**:
   - Third-party organic traffic numbers and keyword positions represent statistical crawler estimates with wider confidence intervals than first-party telemetry. Output deliverables must clearly state that prospect traffic data is estimated and must never present modeled metrics as empirical fact.
4. **Universal Core Web Vitals Standard**:
   - Google PageSpeed Insights API is the sole Google API that operates across any public URL without ownership verification. Core Web Vitals (LCP, CLS, TBT) and Lighthouse technical SEO scores must be collected for every prospect audit.

---

## 10. Prospect Outreach & Regulatory Compliance

1. **Mandatory CAN-SPAM Footer**:
   - Every prospect outreach email must include the CAN-SPAM footer containing a valid physical postal address and a functioning unsubscribe link.
2. **Unsubscribe Processing & Suppression**:
   - Unsubscribe requests must be logged and honored within 10 business days (US) or immediately (EU/UK).
3. **GDPR Sole Trader & Personal Data Protection**:
   - Never email a named personal address at a sole trader or partnership under GDPR without a documented legitimate interest assessment (LIA). Prefer the business phone line or in-person outreach.
4. **Phone Line Preference (TCPA / TSR)**:
   - Prefer the listed business line over mobile numbers for cold calls. Avoid autodialers and prerecorded messages without consent.
5. **Clear Business Identification**:
   - All outreach across all channels must identify the sender's business clearly and immediately.

---

## 11. Google Maps Scraping & Prospect Sourcing Governance

1. **Strict Stdio Transport Mandate (Zero HTTP)**:
   - `gmaps-mcp` must be used over **stdio transport exclusively**. Never enable HTTP transport, and never expose the server over a public or network URL. This completely eliminates authentication and billed-endpoint vulnerability vectors.
2. **Resilient Failure Logging & CSV Escalation**:
   - If `gmaps-mcp` returns zero results for a valid category + location query, or if the server process is unreachable, log the event into `sourcing_notes` and immediately fall back to the manual CSV ingestion path (`prospects.csv`) rather than terminating or returning an empty prospect list.
3. **Mandatory Provenance Attribution**:
   - Every generated prospect list and diagnostic output deliverable must include a `sourcing_path_used` field (`"gmaps-mcp"` | `"csv-fallback"`) so the operational provenance of the raw data is always transparent.

---

## 12. LinkedIn Enrichment & Activity Reading Governance

1. **Strict Read-Only Mandate**:
   - LinkedIn integrations must only use read-only queries (`search_people`, `get_person_profile`, `get_inbox`, `get_conversation`).
   - Under no circumstances may an agent invoke mutation tools (`connect_with_person`, `send_message`, `send_inmail`). All outreach copy is drafted for human review and manual dispatch.
2. **Strict Quota & Frequency Boundaries**:
   - Limit to a maximum of **5 LinkedIn tool calls per prospect**.
   - Limit to a maximum of **5 prospects enriched per execution run**.
3. **Session Interruption & Checkpoint Protocol**:
   - If a CAPTCHA, verification code, or account checkpoint is detected in the browser profile, **halt immediately** and prompt the human operator. Never attempt automated evasion.
4. **Ethical Framing & Zero Hallucination**:
   - When referencing recent posts in approach strategies, never quote personal, sensitive, or political content.
   - Ground all conversation hooks strictly in publicly accessible business observations.

---

## 13. Video Generation Governance (`agent-loom`)

1. **Conditional Flag Requirement**:
   - The video generation step is strictly optional and **MUST only run if the `--video` flag is explicitly passed** in the audit command.
2. **TOS & Rate Limit Adherence**:
   - Video generation and browser walkthrough tools must respect the same rate limits, access controls, and Terms of Service of the underlying target domains and tooling platforms.
3. **Fail-Safe Pipeline Resilience**:
   - If the video CLI (`agent-loom`) is not installed, fails, or crashes during recording, the pipeline must log the incident and proceed to the human review checkpoint with the Markdown and PDF deliverables intact. A video rendering failure must never block the audit report.

---

## 14. Report Verification Gatekeeping

1. **Mandatory Quality Verification**:
   - Every completed audit JSON must pass the `report-verifier` subagent before report formatting and human review.
2. **Correction Loop Limit**:
   - If verification fails, a maximum of **2 correction loops** with `business-auditor` are permitted. If issues remain after 2 cycles, proceed with unresolved items explicitly noted in the report appendix.

---

## 15. ICP Qualification & Combined Ranking Governance

1. **Dual-Score Prospect Ranking**:
   - Discovered prospect lists must be scored and ranked by composite score ($0.6 \times \text{opportunity} + 0.4 \times \text{icp\_fit}$), never by opportunity score alone.
2. **Strict Disqualification**:
   - Any prospect that fails a must-have ICP attribute or matches a disqualifier in `.agents/rules/icp-definition.md` must receive an `icp_fit_score` of 0.

---

## 16. Local Competitor Benchmarking Governance

1. **Mandatory Benchmark Inclusion**:
   - Every audit must include an empirical competitor benchmark whenever 2–3 active competitors can be identified in the target category and location.
2. **Factual Integrity**:
   - Benchmark averages (reviews, ratings, DR, organic traffic) must be derived from verified public data or calibrated crawler models, never fabricated.

---

## 17. Outreach Outcome Tracking Mandate

1. **Zero Untracked Outreach**:
   - Every outreach touch (email, phone call, LinkedIn message, in-person visit) must be recorded to `outputs/outreach_outcomes.csv` immediately after execution. Untracked outreach is strictly prohibited.
2. **Weekly Pattern Analysis**:
   - Outreach performance must be reviewed periodically via `/outcome-analysis` to detect conversion patterns and refine messaging templates.

---

## 18. Standardized Proposal Pricing Governance

1. **Strict Tier Adherence**:
   - All client proposals must strictly utilize the standardized packages and price points defined in `.agents/rules/pricing.md` (Starter, Standard, Premium).
2. **Zero Price Improvisation**:
   - Ad-hoc, unapproved, or improvised pricing figures are strictly prohibited in proposal deliverables.

---

## 19. Client Slug Generation & Output Directory Governance

1. **Standardized Slug Algorithm**:
   Every agent and skill creating or referencing client-specific paths under `outputs/clients/<company-slug>/` must compute `<company-slug>` using the canonical normalization rules:
   - Convert text to lowercase.
   - Replace whitespace and ampersands (`&`) with single hyphens (`-`).
   - Strip apostrophes, periods, commas, exclamation marks, and all other punctuation.
   - Collapse consecutive hyphens into a single hyphen (`--` $\rightarrow$ `-`).
   - Trim leading and trailing hyphens.
   - If the resulting base slug already exists for a different business entity, append the city/municipality slug (e.g., `mikes-plumbing-austin` vs. `mikes-plumbing-dallas`).
2. **Directory Separation**:
   - Master files (`pipeline.md`, `prospects_all.csv`, `outreach_outcomes.csv`, `enrichment_log.jsonl`) reside at `outputs/` root.
   - Analytical insights reside at `outputs/insights/`.
   - All prospect-specific deliverables (`profile.json`, `audit_<date>.md`, `audit_<date>.pdf`, `walkthrough.mp4`, `call_script.md`, `proposal.md`, `conversation_log.md`, `outreach_log.csv`) reside in `outputs/clients/<company-slug>/`.

---

## 20. Scheduled Task Execution & Tool Authorization

1. **Autonomous Non-Interactive Execution Mode**:
   - Scheduled tasks execute in `accept-edits` mode so that file generation and automated audits do not block waiting for live human confirmation during off-hours.
2. **Pre-Approved Automated Tools**:
   - The following read and compilation tools are pre-authorized for unattended scheduled runs:
     - `gmaps-mcp` (read-only search)
     - `places-enrichment` (read-only place details)
     - `company-firmographic-enricher` / `entia` / `opencorporates`
     - `seo-analyst-gsc` / `seo-analyst-prospect`
     - `run_command` (exclusively for Pandoc and local Python report compilation)
3. **Strictly Blocked Tools During Scheduled Runs**:
   - Mutation and communication tools are **strictly blocked**:
     - `linkedin.send_message`
     - `linkedin.connect_with_person`
     - `linkedin.send_inmail`
     - Any email dispatch or webhook push tool
4. **Kill-Switch Protocol**:
   - Every scheduled automation task must be disablable via the `/schedule` management interface. If a task misbehaves or external endpoints degrade, disable the schedule via `/schedule` immediately rather than attempting hot code patches.
5. **Deliverables-Only Mandate**:
   - Scheduled runs compile reports, call scripts, and briefs only. They **NEVER** contact a prospect.
   - The transition from "report ready" to "outreach sent" is **ALWAYS manual**.
6. **Graceful Failure**:
   - If a scheduled run cannot complete without human input (e.g., CAPTCHA, authentication loss), it must log the blocker in `outputs/daily_brief.md` and exit cleanly rather than hanging or looping.

---

## 21. Top-N Batch Pursuit Governance

1. **Deliverables-Only Scope**:
   - Batch pursuit runs produce client dossiers and deliverables only. Autonomous outreach is strictly prohibited.
2. **Dual-Score Prioritization**:
   - Top-N candidate selection must use the composite ranking score:
     $$\text{combined\_score} = (\text{opportunity\_score} \times 0.6) + (\text{icp\_fit\_score} \times 0.4)$$
   - If `icp_fit_score` is unavailable, fall back to `opportunity_score` alone and explicitly record the fallback in `outputs/selection_log.csv`.
3. **Hard Iteration Caps**:
   - Batch runs must strictly enforce an iteration limit equal to `--count` (default: 20). Unbounded loops or pagination runaways are strictly prohibited.
4. **Rate Limit Graceful Halt**:
   - If a batch run encounters an HTTP 429 status or rate-limit warning from Google Maps or enrichment providers, it must halt immediately, log progress and completed counts to `outputs/batch_summary_{date}.md`, and conclude without aggressive retries.

---

## 22. Google Sheets Live Sync Governance

1. **Strict Column Demarcation & Contiguous Write Range**:
   - Automated pipeline writes are strictly confined to **columns A through K** (`Business Name`, `Location`, `Opportunity Score`, `Tier`, `Audit PDF Link`, `Video Walkthrough Link`, `Call Script Link`, `Suggested Opening Line`, `Contact Name`, `Contact Title`, `LinkedIn Profile URL`) in a single contiguous write.
   - Under no circumstances may an agent, workflow, or tool write, overwrite, modify, clear, or alter **columns L through R**, which are exclusively user-managed (`Outreach Status`, `Touch 1 Date`, `Touch 2 Date`, `Touch 3 Date`, `Last Touch Result`, `Next Action`, `Notes`).
2. **Append-Only & Idempotent Updates**:
   - New prospect entries must append to the first empty row below existing data.
   - If an existing prospect is audited again, update only columns A–K of that existing row; preserve all manual user inputs in L–R.
3. **Non-Blocking Resilience**:
   - Google Sheets sync failures (e.g. invalid credentials, quota exhaustion, network timeout) must be treated as non-fatal warnings.
   - The local pipeline and deliverables (Markdown, PDF, CSV ledgers) must continue unaffected. Never abort an audit due to a Google Sheets error.
4. **Outreach Status Truth**:
   - The live Google Sheet (specifically column L "Outreach Status" and manual logs in L–R) serves as the primary operational record for human outreach state. The `/sync-pipeline` workflow reconciles this state back into local client logs.

---

## 23. Token Efficiency & Interactive Fallback Feedback

1. **Model Tier Discipline**:
   - Routine tasks and specialized data workers must operate on token-optimized model tiers:
     - `gemini-3.5-flash-low` for `pillar-auditor`, `report-formatter`, `report-verifier`.
     - `gemini-3.1-flash-lite` for `seo-analyst` and data parsing.
     - `pro` is reserved exclusively for high-reasoning orchestration (`business-auditor`).
   - If granular aliases are unavailable in the active environment, agents fall back gracefully to `flash`.
2. **Prompt Cache Prefix Locking**:
   - Prompts must maintain consistent static instruction prefixes separated by the `# CACHE PREFIX` marker and `---VARIABLE---` delimiter to maximize Gemini cache hits across repetitive agent turns.
3. **Scoped Context Isolation**:
   - Parent agents must avoid passing monolithic JSON blobs to specialized workers. Workers must receive only the specific data fields required for their assigned domain.
4. **Interactive Fallback Transparency**:
   - When an enrichment rung or tool fails and triggers ladder escalation or rate limiting, log the incident and provide transparent operational feedback in execution summaries.
   - Never suppress failure telemetry or silently consume excessive API quotas.

---

## 24. Personal LinkedIn Profile Self-Audit Governance

1. **Strict Read-Only Enforcement**:
   - The `profile-self-audit` skill is strictly **READ-ONLY**. Under no circumstances may an agent invoke any mutation or edit tools against the user's LinkedIn account. All proposed changes and rewrites must be presented as text deliverables for the user to copy-paste manually.
2. **ICP Grounding Mandate**:
   - All profile recommendations, headline keywords, positioning angles, and skill suggestions **must be strictly grounded in `.agents/rules/icp-definition.md`**. Generating arbitrary keywords or positioning that is not directly supported by the target market definition is prohibited.
3. **Prioritized Impact Ranking**:
   - The audit must surface a **prioritized fix list ranked by operational impact** (HIGH: Headline & About section; MEDIUM: Skills, Featured, Experience; LOW: Photo, Banner, Custom URL, Recommendations, Activity), never an unranked flat list.








