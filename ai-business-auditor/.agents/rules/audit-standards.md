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



