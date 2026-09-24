# AI Business Auditor

An agent-first, multi-tier diagnostic system that takes a single company URL, enriches it with firmographic, legal, and technographic intelligence, runs a structured management-consultant diagnostic across four operational pillars, and compiles an executive audit deliverable — using **exclusively free and open-source tooling**.

---

## Architecture Overview

```
                      +---------------------------------------+
                      |        Phase 0: URL Normalizer        |
                      +---------------------------------------+
                                          |
                                          v
                      +---------------------------------------+
                      |       1. company-researcher           |
                      | (Enrichment Ladder + Technographics)  |
                      |            Model: flash               |
                      +---------------------------------------+
                                          |  [Firmographic JSON]
                                          v
                      +---------------------------------------+
                      |        2. business-auditor            |
                      |     (Orchestrator, Model: pro)        |
                      +---------------------------------------+
                                          |
                                          |  Spawn CONCURRENTLY in Parallel
                                          |  (Explicit Profile Context Passing)
                                          +-------------------+-------------------+-------------------+
                                          |                   |                   |                   |
                                          v                   v                   v                   v
                               +-------------------+ +-------------------+ +-------------------+ +-------------------+
                               |  pillar-auditor   | |  pillar-auditor   | |  pillar-auditor   | |  pillar-auditor   |
                               | (Sales & Market.) | | (Customer Support)| | (Product Delivery)| | (Internal Ops)    |
                               |   Model: flash    | |   Model: flash    | |   Model: flash    | |   Model: flash    |
                               +-------------------+ +-------------------+ +-------------------+ +-------------------+
                                          |                   |                   |                   |
                                          +-------------------+-------------------+-------------------+
                                          |
                                          |  [Consolidated 4-Pillar JSON]
                                          v
                      +---------------------------------------+
                      |       3. report-formatter             |
                      |    (Local PDF Rendering via Pandoc)   |
                      |            Model: flash               |
                      +---------------------------------------+
                                          |
                                          v
                        [MANDATORY HUMAN REVIEW CHECKPOINT]
                                          |
                        +-----------------+-----------------+
                        |                                   |
                    [Approve]                       [Revise / Abort]
                        |
                        v
          [Optional: Notion Shareable Link]
```

---

## Custom Subagents & Model Tiering

The system is factored into four specialized subagents located in `.agents/agents/`:

| Agent File | Role & Function | Model Tier | Tools |
| :--- | :--- | :---: | :--- |
| [`.agents/agents/company-researcher.md`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/.agents/agents/company-researcher.md) | Walks the Enrichment Ladder (ENTIA, Apify, OpenCorporates), runs Places & SEO telemetry, and infers technographics. | `flash` | `invoke_mcp_tool`, `invoke_subagent`, `web_search`, `url_context`, `run_command` |
| [`.agents/agents/seo-analyst-gsc.md`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/.agents/agents/seo-analyst-gsc.md) | First-party GSC specialist querying actual search performance (clicks, impressions, quick wins) for verified properties. | `gemini-3.1-flash-lite` | `invoke_mcp_tool`, `view_file` |
| [`.agents/agents/seo-analyst-prospect.md`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/.agents/agents/seo-analyst-prospect.md) | Third-party SEO intelligence specialist assessing ANY non-owned domain (SE Ranking, FetchSERP, Ahrefs DR, PageSpeed CWV). | `gemini-3.1-flash-lite` | `invoke_mcp_tool`, `run_command`, `web_search` |
| [`.agents/agents/pillar-auditor.md`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/.agents/agents/pillar-auditor.md) | Scoped diagnostic worker that audits exactly **ONE** assigned pillar. Instantiated four times in parallel. | `gemini-3.5-flash-low` | `view_file` |
| [`.agents/agents/business-auditor.md`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/.agents/agents/business-auditor.md) | High-reasoning orchestrator that spawns the four parallel pillar auditors, verifies reasoning scaffolds, and synthesizes roadmaps. | `pro` | `view_file`, `invoke_subagent` |
| [`.agents/agents/report-formatter.md`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/.agents/agents/report-formatter.md) | Formats structured diagnostic JSON into Markdown and compiles local PDFs via Pandoc/ReportLab. | `gemini-3.5-flash-low` | `view_file`, `replace_file_content`, `run_command` |
| [`.agents/agents/report-verifier.md`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/.agents/agents/report-verifier.md) | Quality gatekeeper running 6 automated consistency and evidentiary verification checks. | `gemini-3.5-flash-low` | `view_file` |

### Context Isolation & Scoped Data Passing Architecture
- **Parallel Dispatch**: The four business pillars (Sales & Marketing, Customer Support, Product & Service Delivery, Internal Operations & Infrastructure) are independent domains. `business-auditor` dispatches all four `pillar-auditor` workers **concurrently in a single turn**.
- **Scoped Context Isolation**: Subagents **do not inherit parent conversation history**. Rather than passing full monolithic JSON profiles, the orchestrator injects **domain-scoped slices** under locked prompt cache prefixes (`# CACHE PREFIX` above `---VARIABLE---`), cutting token overhead by up to 60%.

---

## Diagnostic Rigor & Reasoning Scaffold

To prevent generic consulting output, every score (1–10) emitted by a `pillar-auditor` must strictly follow the **4-Step Reasoning Scaffold**:
1. **Step A — Evidence**: Cites specific, observed signals from the company profile.
2. **Step B — Expected State**: Benchmarks the ideal operational standard for an enterprise of this scale and industry.
3. **Step C — Gap Description**: Quantifies the operational distance between observed and expected performance.
4. **Step D — Score**: Derives the numerical 1–10 score directly from the gap magnitude.

---

## Lifecycle Hooks (`.agents/hooks.json`)

Antigravity lifecycle hooks enforce system governance and execution safety:

1. **`paywall-guard` (`PreToolUse`)**:
   - Intercepts web scraping and fetch calls (`read_url_content`, `web_search`, `url_context`).
   - Automatically blocks requests targeting paywalled media (e.g., Bloomberg, Wall Street Journal, Financial Times) or private intranet IPs, returning an immediate denial reason.
2. **`enrichment-logger` (`PostToolUse`)**:
   - Monitors all MCP enrichment calls (`entity_lookup`, `enrich_company_firmographics`, `get_full_dossier`, etc.).
   - Appends audit trail logs to `outputs/enrichment_log.jsonl` with timestamps, tool names, arguments, and success statuses.
3. **`reasoning-reminder` (`PreInvocation`)**:
   - Injects an ephemeral governance reminder before model turns to ensure subagents adhere to the mandatory 4-step reasoning scaffold and context passing rules.

---

## Enrichment & Scraper Ladders

### Enrichment Ladder (Replaces Explorium)
1. **ENTIA MCP Server** (Primary): 11.3M verified business records across 10+ European countries, VAT validation (VIES), LEI codes, and competitive entity discovery. Free TRACE tier (~100 calls/month).
2. **Apify "Company Firmographic Enricher"** (Fallback Rung 2): Structured extraction of employee bands, revenue estimates, headquarters, and industry categories via `$5/mo` free compute.
3. **OpenCorporates MCP** (Fallback Rung 3): Official government registry filings, jurisdiction numbers, and corporate officer records.

### Scraper Ladder (Replaces Tavily)
1. `ai-first-search`
2. `Spectrawl` (stealth multi-engine search aggregator)
3. `Crawl4AI` / Native Antigravity Web Search & URL extraction tools

### Technographic Confidence System
Commercial technographic APIs are paid. To maintain a **100% free stack**, the system uses an active inference protocol:
- Scrapes the target company's careers portal, active engineering job descriptions, engineering blog, and HTML footer script tags.
- Inferred tools are **never presented as verified fact**. Every item is assigned an evidentiary citation and an explicit confidence rating:
  - `high`: Verified from primary technical job specifications or official engineering documentation.
  - `medium`: Inferred from public open-source repos, developer posts, or frontend tracking scripts.
  - `low`: Inferred from general industry standard alignment.

---

## Project Structure

```
ai-business-auditor/
├── skillpack.yaml                 # Pinned skills manifest for reproducible team setups
├── skills.sh.json                 # Skill pack manifest for skills.sh distribution
├── agents.md.legacy               # Preserved legacy monolithic agents document
├── README.md                      # Comprehensive system documentation
├── .agents/
│   ├── mcp_config.json            # MCP registrations (ENTIA, Apify, OpenCorporates, GSC, Places)
│   ├── hooks.json                 # Antigravity lifecycle hooks configuration
│   ├── hooks/
│   │   └── scripts/               # Python hook scripts (paywall guard, logging, reminders)
│   ├── agents/                    # Modular subagent definitions
│   │   ├── company-researcher.md  # Tier: flash | Subagent: true
│   │   ├── seo-analyst-gsc.md     # Tier: flash | Subagent: true (First-party GSC specialist)
│   │   ├── seo-analyst-prospect.md# Tier: flash | Subagent: true (Third-party SEO intelligence)
│   │   ├── pillar-auditor.md      # Tier: flash | Subagent: true (4x parallel)
│   │   ├── business-auditor.md    # Tier: pro   | Subagent: true (orchestrator)
│   │   └── report-formatter.md    # Tier: flash | Subagent: true
│   ├── rules/
│   │   └── audit-standards.md     # Always-on governance, reasoning scaffold, & security rules
│   ├── skills/
│   │   ├── company-research/      # Firmographic & technographic profiling
│   │   │   └── SKILL.md
│   │   ├── places-enrichment/     # Google Places API location & reputation intelligence
│   │   │   └── SKILL.md
│   │   ├── business-audit/        # 4-pillar parallel orchestration & synthesis
│   │   │   └── SKILL.md
│   │   ├── report-export/         # Markdown & PDF report compiler
│   │   │   ├── SKILL.md
│   │   │   └── scripts/
│   │   ├── prospect-finder/       # Local business prospect scraper guidance & scoring
│   │   │   ├── SKILL.md
│   │   │   └── scripts/
│   │   │       └── score_prospects.py # Automated Opportunity Scoring Rubric (0-100)
│   │   ├── find-skills/           # Gateway skill for skills.sh community discovery
│   │   │   └── SKILL.md
│   │   └── skill-security-check/  # Pre-installation automated security audit verifier
│   │       └── SKILL.md
│   └── workflows/
│       └── audit.md               # /audit slash command (with Step 0.5 capability check)
├── mcp/
│   └── enrichment.md              # In-depth MCP documentation & escalation protocols
├── tools/
│   └── free-stack.md              # Free tier limits, setup guide, and throughput limits
└── outputs/
    ├── .gitkeep                   # Directory for generated audits (.md and .pdf)
    └── enrichment_log.jsonl       # Automated audit log of all MCP enrichment calls
```

---

## Skills Ecosystem (skills.sh Integration)

This project integrates directly with **[skills.sh](https://skills.sh/)**, Vercel's open agent skills directory indexing over 600,000+ community skills. Skills are modular packages conforming to the Agent Skills Standard (`SKILL.md`) that dynamically extend agent capabilities.

### 1. Gateway Skill (`find-skills`)
Installed at [`.agents/skills/find-skills/`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/.agents/skills/find-skills/SKILL.md), this gateway skill enables on-demand discovery. When an audit encounters an edge case (e.g., an exotic regional corporate registry, specialized PDF layout engine, or niche scraping requirement), the agent can find and integrate an existing community skill instead of failing.

### 2. Searching & Installing Community Skills
Community skills can be queried and installed using the zero-install `skills` CLI:
```bash
# Search for skills interactively or by keyword
npx skills find [query]

# Install a verified community skill into the project
npx skills add <owner/repo> --skill <skill-name> -y

# List currently installed skills
npx skills list
```

### 3. Pre-Installation Security Audits (`skill-security-check`)
All skills on `skills.sh` undergo automated security analysis across three independent engines:
1. **Agent Trust Hub**: Evaluates prompt safety, behavioral integrity, and tool execution boundaries.
2. **Socket**: Detects supply-chain attacks, obfuscated code, and anomalous network calls.
3. **Snyk**: Scans for known software vulnerabilities and critical CVEs.

Per project governance ([`audit-standards.md`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/.agents/rules/audit-standards.md)), **no skill may be installed without automated audit verification**:
- Run `skill-security-check` to query `https://skills.sh/api/v1/skills/:owner/:repo/:skillId` (or inspect the public detail page at `https://skills.sh/<owner>/<repo>/<skill-name>`).
- Any skill with a **HIGH risk** flag in any category is strictly blocked from installation.

### 4. Reproducibility with `skillpack.yaml`
Installed skills are pinned in [`skillpack.yaml`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/skillpack.yaml) at the project root:
```yaml
agents:
  - antigravity
skills:
  vercel-labs/skills:
    - find-skills
```
Team members can reproduce the exact workspace skill environment with:
```bash
npx skillpack install
```
*(If `skillpack` CLI is not yet globally installed, install via: `npm install -g skillpack` or run via `npx skillpack`).*

### 5. Publishing Project Skills as a Pack
The core auditor skills (`company-research`, `business-audit`, `report-export`) are pre-configured for distribution via [`skills.sh.json`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/skills.sh.json):
```json
{
  "title": "AI Business Auditor",
  "description": "A multi-agent system that audits any business from a URL, scoring four operational pillars and producing a formatted report with roadmaps.",
  "skills": ["company-research", "business-audit", "report-export"]
}
```
Once the pack is registered at [skills.sh/packs](https://skills.sh/packs), users can install the complete AI Business Auditor suite with a single command:
```bash
npx skills add https://skills.sh/p/<pack-id>
```

---

## Google API Integrations

The system integrates with **Google Search Console API** and **Google Places API (New)** to inject empirical search visibility and verified physical footprint intelligence into the diagnostic.

### 1. Google Search Console API

#### What it Provides:
- Live 90-day search performance data: total organic clicks, impressions, average CTR, and average SERP ranking position.
- Dimension breakdowns grouped by `query` and `page`.
- Quick-win query identification (high impressions with low CTR).
- Crawl and indexing health flags via `inspect_url`.

#### What it Does NOT Provide / Scope Limitation:
- **Verified Properties Only**: Search Console telemetry is strictly private. It **cannot audit arbitrary domains** on the web. It only returns data for properties verified under the authenticated Google Account.
- **Graceful Skip**: If an audited domain is not present in `list_sites`, the `seo-analyst` subagent cleanly records `{"skipped": true, "reason": "property not verified for this account"}` and continues without crashing the workflow.

---

### 2. Google Places API (New)

#### What it Provides:
- Physical business location details: verified legal/trade name, formatted street address, telephone, operational hours, and place ID.
- Real-time customer reputation: aggregate Google star rating (1.0–5.0), total review count, and recent review highlights.
- Match confidence scoring (`high`, `medium`, `low`) cross-referenced against the target domain.

#### Billing Requirement:
- **Active Billing Account Required**: While Google Cloud includes a **$200/month recurring credit** (~11,000 text searches free per month), Google **mandates an active billing account** linked to the Cloud project for the Places API (New) to respond.

---

### 3. Manual Google Cloud Setup Steps

To activate these two MCP integrations:

1. **Google Cloud Project**:
   - Navigate to [Google Cloud Console](https://console.cloud.google.com/) and create a project (e.g., `ai-business-auditor`).
   - Enable both APIs:
     - **Google Search Console API**
     - **Places API (New)**
2. **Configure OAuth Consent Screen** (for Search Console):
   - Choose **External** user type.
   - Set app name, user support email, and developer contact info.
   - Add the OAuth scope: `https://www.googleapis.com/auth/webmasters.readonly`.
   - Add your Google account under **Test users**.
   - *(Recommended)* Publish the app to production to avoid 7-day token expiration for test users.
3. **Create OAuth 2.0 Credentials** (for Search Console):
   - Navigate to **APIs & Services > Credentials > Create Credentials > OAuth client ID**.
   - Application type: **Desktop app**.
   - Download the client configuration containing `client_id` and `client_secret`.
4. **Obtain the Search Console Refresh Token**:
   - Run the bundled OAuth helper:
     ```bash
     npx -y -p google-search-console-mcp-server google-search-console-mcp-setup
     ```
   - Follow the browser prompt to log in and authorize Search Console read-only access.
   - Copy the generated `refresh_token`.
5. **Create & Restrict Places API Key**:
   - Under **Credentials > Create Credentials > API Key**.
   - Click **Edit API key**, restrict the key to **Places API (New)**, and copy the key string.
   - Ensure an active billing account is linked to the project under **Billing**.

---

### 4. Credential Storage & Environment Variables

Credentials are read from your local environment and declared in [`.agents/mcp_config.json`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/.agents/mcp_config.json):

```bash
# In your shell or .env file:
export GOOGLE_CLIENT_ID="your-client-id.apps.googleusercontent.com"
export GOOGLE_CLIENT_SECRET="your-client-secret"
export GOOGLE_REFRESH_TOKEN="your-refresh-token"
export GOOGLE_PLACES_API_KEY="your-restricted-api-key"
```

---

### 5. How to Test Each Integration Independently

Test Google Search Console MCP:
```bash
# Verify the MCP server starts and reads credentials
npx -y -p google-search-console-mcp-server google-search-console-mcp
```

Test Google Places API directly:
```bash
# Test direct Places text search endpoint via curl
curl -X POST "https://places.googleapis.com/v1/places:searchText" \
  -H "Content-Type: application/json" \
  -H "X-Goog-Api-Key: $GOOGLE_PLACES_API_KEY" \
  -H "X-Goog-FieldMask: places.id,places.displayName,places.formattedAddress,places.rating" \
  -d '{"textQuery": "Linear Software San Francisco"}'
```

---

## SEO Data for Prospects (Non-Owned Domains)

### 1. Why Google Search Console Cannot Be Used for Prospects
Google Search Console is strictly a **first-party verified diagnostic tool**. Google's API returns an HTTP 403 Forbidden error for any domain that has not completed ownership verification via DNS TXT records or HTML file uploads. For competitive intelligence, market audits, and cold business development, **first-party access does not exist**.

To audit cold prospects and competitors, the system routes queries through **third-party search intelligence providers** that maintain independent web crawlers and index public SERP results.

---

### 2. The Third-Party SEO Data Ladder

When auditing non-owned domains, `seo-analyst-prospect` executes the following fallback ladder:

1. **Rung 1 — SE Ranking SEOIntel**:
   - Primary domain intelligence engine providing top 20 keywords, near-page-one opportunities (positions 11–20), domain authority, estimated monthly organic traffic, and backlink summaries.
   - Falls back gracefully to hosted demo mode if `SE_RANKING_API_KEY` is not present.
2. **Rung 2 — FetchSERP MCP Server** (`fetchserp`):
   - Local stdio MCP server providing 250 free monthly credits for keyword volumes, live SERP positions, indexation status, and domain profiling.
3. **Rung 3 — Ahrefs Public API (Domain Rating)**:
   - Queries `https://api.ahrefs.com/v3/public/domain-rating-free?target=<domain>` to extract a free, unauthenticated Domain Rating (DR 0–100) benchmark.
4. **Rung 4 — Google PageSpeed Insights API**:
   - Queries `https://www.googleapis.com/pagespeedonline/v5/runPagespeed`.
   - **Crucial Advantage**: The **only** Google API that functions on any public URL without ownership verification. Provides empirical Core Web Vitals (LCP, CLS, TBT) and Lighthouse technical SEO scores (0–100).
5. **Rung 5 — Common Crawl Backlink Audit**:
   - Queries open-source Common Crawl CDX indices to estimate referring domain footprint and external backlink presence with zero cloud cost.

---

### 3. Estimated (Third-Party) vs. Actual (GSC) Data

| Metric Dimension | Verified Client Path (`seo-analyst-gsc`) | Prospect Path (`seo-analyst-prospect`) |
| :--- | :--- | :--- |
| **Data Nature** | Empirical server logs & actual Google clicks/impressions | Statistical crawler models & sampled SERP rankings |
| **Accuracy** | 100% ground truth | Directional estimate (wider confidence interval) |
| **Scope** | Only properties verified under your Google account | **Any public website on the internet** |
| **Key Insights** | Exact queries, true CTR, internal canonical leaks | Near-page-one keywords (pos. 11-20), DR, Core Web Vitals |
| **Reporting Standard** | Cites exact GSC numbers | Attributed to `data_source_tier` with estimation notice |

---

### 4. Provider Setup & Environment Variables

Add keys to your `.env` file to unlock paid or higher-tier capabilities:

```bash
# FetchSERP: 250 free requests from https://fetchserp.com
FETCHSERP_API_TOKEN="your_fetchserp_token"

# SE Ranking: Optional API key from https://seranking.com
SE_RANKING_API_KEY="your_se_ranking_key"
```

*(Note: If neither key is provided, the system automatically uses Rung 3 [Ahrefs DR] + Rung 4 [PageSpeed Insights] + Rung 5 [Common Crawl] to generate a complete assessment without any API costs).*

---

### 5. When to Use Which Path

- **Use Verified Path (`seo-analyst-gsc`)**: Automatically selected when auditing domains where you are a verified owner in Search Console (e.g., your portfolio companies or paying clients).
- **Use Prospect Path (`seo-analyst-prospect`)**: Automatically triggered whenever auditing external URLs, cold sales prospects, or competitor domains.

---

## How to Trigger an Audit

To run a complete business diagnostic audit on any company:

```
/audit <company URL>
```

**Example**:
```
/audit https://www.linear.app
```

### Audit Lifecycle:
1. **Normalization (Step 0)**: Sanitizes URL to canonical domain (e.g., `linear.app`).
2. **Capability Check (Step 0.5)**: Dynamic search and installation of community skills if specialized capabilities are needed.
3. **Research (`company-researcher` - Step 1)**: Queries ENTIA MCP -> Apify -> Scrapes careers page for technographics.
4. **Diagnostic (`business-auditor` - Step 2)**: Spawns **four `pillar-auditor` subagents in parallel** (Sales, Support, Product, Ops) with full profile context and reasoning scaffolds; synthesizes roadmaps.
5. **Formatting (`report-formatter` - Step 3)**: Generates local Markdown and PDF in `outputs/`.
6. **Human Review Checkpoint (Step 4)**: Pauses and presents the summary table and PDF link in chat.
7. **Approval (Step 5)**: Upon your confirmation, confirms finalization (or publishes to Notion if credentials are provided).

---

## Output Structure

The system employs a **hybrid flat + per-client directory architecture** under `outputs/`:

```
outputs/
├── pipeline.md                    # Master commercial pipeline dashboard
├── prospects_all.csv              # Master list of all sourced & scored prospects
├── outreach_outcomes.csv          # Master chronological log of all outreach touches
├── audit_log.csv                  # Master record of completed diagnostic runs
├── enrichment_log.jsonl           # Master MCP tooling audit trail (from lifecycle hook)
├── customized_outreach_copy.md    # Master batch copy review file
├── insights/
│   └── outreach_insights.md       # Master weekly outreach pattern analysis
└── clients/
    └── <company-slug>/
        ├── profile.json           # Raw company intelligence & technographics dossier
        ├── audit_<date>.json      # Scored 4-pillar diagnostic JSON
        ├── audit_<date>.md        # Comprehensive diagnostic report in Markdown
        ├── audit_<date>.pdf       # Formatted PDF deliverable (Pandoc / ReportLab)
        ├── walkthrough.mp4        # Narrated video walkthrough (if --video was passed)
        ├── call_script.md         # Custom branching phone call decision tree
        ├── proposal.md            # Client-ready proposal & pricing tier
        ├── proposal.pdf           # Compiled PDF proposal
        ├── conversation_log.md    # Manual interaction notes & history
        ├── outreach.md            # Customized multi-channel outreach copy
        ├── outreach.pdf           # Outreach PDF summary
        └── outreach_log.csv       # Per-client touch sequence & response log
```

### Why a Hybrid Structure?
- **Master Files Stay Flat**: Cross-prospect ledgers (`pipeline.md`, `prospects_all.csv`, `outreach_outcomes.csv`, `audit_log.csv`) must be queried as unified datasets for pattern analysis, weekly conversion metrics, and pipeline dashboarding without requiring multi-directory recursive joins.
- **Per-Prospect Files Go into Dedicated Client Folders**: Keeps all artifacts, audits, proposals, video files, call scripts, and specific interaction notes for a single company isolated in one clean workspace.

### Slug Naming Convention
Client folder names follow strict normalization rules:
- Lowercase only.
- Spaces and ampersands (`&`) are converted to hyphens (`-`).
- Punctuation (apostrophes, commas, periods, quotes) is stripped.
- Consecutive hyphens are collapsed into a single hyphen.
- City slugs are appended only if necessary to resolve naming collisions (e.g., `mikes-plumbing-austin` vs. `mikes-plumbing-dallas`).

### When Client Folders Get Created
Client folders under `outputs/clients/<company-slug>/` are initialized automatically:
- During **Step -1 (Client Folder Setup)** when `/audit <url>` is triggered.
- When an audit is requested for a specific lead from `prospect-finder`.
- Initialized with `conversation_log.md` (from `.agents/templates/conversation-log.md`) and a blank `outreach_log.csv` if missing. Existing files are preserved and never overwritten.

---

## Prospect Sourcing

The system includes automated local lead generation via the `/find-prospects` workflow and `prospect-finder` skill to identify, score, and rank local service businesses by service opportunity.

### 1. Dual Sourcing Paths
- **Path 1: `gmaps-mcp` (Primary)**: Directly scrapes Google Maps via the `gmaps-mcp` stdio MCP server without requiring browser extensions or Google Maps API keys. Returns structured Place ID, business name, address, phone, website URL, coordinates, star rating, and review count.
- **Path 2: CSV Import (Fallback)**: If `gmaps-mcp` is offline, unreachable, or returns 0 results, the system prompts the user to export `prospects.csv` using a free Chrome browser extension (e.g., Instant Data Scraper, GeoLeadScraper, LeadGrabber) into the project root.

### 2. Prerequisites: Installing `uvx`
`gmaps-mcp` runs via `uvx` (from Astral's `uv` toolchain). If not present on your system:
- **Windows (PowerShell)**:
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
  *(Or via pip: `pip install uv`)*
- **macOS / Linux**:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

Verify installation:
```bash
uvx --version
```

### 3. MCP Server Configuration
In `.agents/mcp_config.json`:
```json
"gmaps": {
  "command": "uvx",
  "args": [
    "--from",
    "git+https://github.com/devsanthoshmk/gmaps-mcp.git",
    "gmaps-mcp",
    "serve"
  ]
}
```
**Verification**: Check the Antigravity IDE **MCP Servers** panel to confirm `gmaps` is connected and exposing `search_google_maps`.

### 4. Security Note (Stdio Transport Exclusively)
A disclosed security advisory affects HTTP-transport implementations of Google Maps MCP servers where unauthenticated callers can trigger billed API calls. This project exclusively uses the **stdio-based** `devsanthoshmk/gmaps-mcp` server running locally. Never expose this server over HTTP or a public URL, and never configure an HTTP transport entry without strict token authentication.

### 5. CSV Fallback Preparation
The CSV fallback activates automatically if `gmaps-mcp` encounters rate limits or returns 0 records:
1. Search Google Maps for your target trade and city (e.g., `"plumbers in Austin, TX"`).
2. Open a free browser scraper extension (such as **Instant Data Scraper**).
3. Export the table as CSV and save to workspace root as `prospects.csv`.
4. Confirm to the agent to resume automated scoring, filtering, and compliance checks.

---

## Call Scripts

Generate a customized, branching phone call decision tree for any audited prospect:

```bash
/call-script "<prospect name>"
```

### Branching Architecture:
- **Section A — Opening (0:00–0:30)**: Conversational greeting, permission-based opener ("Do you have 60 seconds?"), and context.
- **Section B — The Hook (0:30–1:30)**: Observation-based citation of audit finding #1 with business consequences.
- **Section C — The Branch Point (1:30–2:00)**: Splitting questions leading to Engaged, Skeptical, or Neutral paths.
- **Section D — 10 Prepared Objection Branches**: Acknowledged, reframed, and concluding with momentum:
  1. "Too busy"
  2. "No budget"
  3. "Already have someone"
  4. "Tried marketing before"
  5. "Need to think about it"
  6. "Send an email"
  7. "How much does it cost?"
  8. "Who are you / How did you get my number?"
  9. "Is this a sales call?"
  10. "Not interested"
- **Section E — Close Paths**: Soft close (send report), Medium close (15-min call), Hard close (initiate onboarding).
- **Section F — What NOT to Say**: Prospect-specific warnings (no jargon, no unprompted competitor mentions, no pricing before value).
- **Storage Location**: Saved to `outputs/call_scripts/{prospect_name}_call.md`.
- **Governance**: High-pressure tactics, artificial scarcity, and dead-end responses are strictly prohibited.

---

## Outreach Outcomes Feedback Loop

Track every outreach touch and analyze reply patterns across channels:

```bash
/outcome-analysis
```

- **Recording Mode**: Appends every touch to `outputs/outreach_outcomes.csv` with date, prospect name, channel, touch number, message excerpt, and status (`replied`, `booked`, `no_reply`, `closed`).
- **Analysis Mode**: Groups data by channel, touch number, and message angle to calculate reply rates, identify top 3 converting hooks, highlight bottom 3 friction points, and export recommendations to `outputs/outreach_insights.md`.

---

## Report Verifier Quality Gate

Before any audit deliverable is formatted into PDF or reaches human review, it is inspected by the `report-verifier` subagent (`model: pro`):
- **Consistency**: Confirms no cross-pillar contradictions.
- **Sourcing**: Validates all factual claims against `data_sources_used`.
- **Rationale**: Rejects generic consulting boilerplate in favor of profile-specific evidence.
- **Reasoning Scaffold**: Enforces the 4-step framework (Evidence → Expected State → Gap → Score).
- **Technographics**: Ensures all inferred tools have explicit confidence ratings and citations.
- **Numeric Integrity**: Verifies metrics against primary profile telemetry.
- **Correction Loop**: Up to 2 automated correction cycles with `business-auditor` before staging.

---

## ICP Qualification & Composite Ranking

Prospects discovered via `prospect-finder` are evaluated against [`.agents/rules/icp-definition.md`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/.agents/rules/icp-definition.md):
- **Must-Have Gates**: Physical location, 10+ reviews, callable business line.
- **Disqualifiers**: Franchises, in-house marketing/tech teams, closed/dormant entities.
- **Composite Score Formula**:
  $$\text{combined\_score} = (\text{opportunity\_score} \times 0.6) + (\text{icp\_fit\_score} \times 0.4)$$
- Ensures high-opportunity leads also match realistic engagement and service fit.

---

## Competitor Benchmarking

Every audit incorporates local competitive intelligence via the `competitor-benchmark` skill:
- Automatically discovers 2–3 active local market leaders via `gmaps-mcp`.
- Collects Google ratings, review counts, Domain Rating (DR), and organic search traffic.
- Calculates `benchmark_averages` embedded in `competitor_benchmark` within the company profile.
- Downstream diagnostic agents (`pillar-auditor`) calibrate expected operational standards directly against local competitor performance.

---

## Proposal Generation

Turn completed audits into client-ready service proposals and PDF agreements:

```bash
/proposal "<prospect name>"
```

- **Standardized Pricing Tiers** (from [`.agents/rules/pricing.md`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/.agents/rules/pricing.md)):
  - **Starter ($750/mo)**: GBP optimization, citation synchronization, automated review collection.
  - **Standard ($1,750/mo)**: High-speed landing page/redesign, 10 local keywords, review management, monthly content.
  - **Premium ($3,500/mo)**: 24/7 AI lead receptionist bot, full SEO & schema, competitor monitoring, CRM field automation.
- Outputs executive Markdown and compiled PDF to `outputs/proposals/{company_name}_proposal_{date}.pdf`.

---

## Commercial Pipeline Dashboard

Generate a real-time Markdown overview of all prospects, audit statuses, and outreach touches:

```bash
/pipeline
```

- Ingests `outputs/prospects_*.csv`, `outputs/audit_log.csv`, and `outputs/outreach_outcomes.csv`.
- Merges data into a consolidated table: `Prospect | Tier | Opportunity Score | ICP Fit | Last Touch | Status | Next Action`.
- Automatically calculates next steps and highlights **overdue follow-ups in bold**.
- Saved to `outputs/pipeline.md` and presented in chat.

---

## Scheduled Automation

Antigravity 2.0 scheduled automation handles all time-consuming intelligence and deliverable preparation overnight or off-hours, ensuring client dossiers are fully prepared before the consultant begins outreach:

### 1. Automated vs. Manual Phases
- **Automated (Scheduled Runs)**:
  - Local prospect sourcing & ICP scoring
  - Firmographic & technographic enrichment
  - Parallel 4-pillar diagnostics
  - Report quality verification
  - Executive Markdown, PDF, and walkthrough video rendering
  - Phone call script generation
  - Commercial pipeline and daily brief compilation
- **Manual (Human Consultant Only — Never Scheduled)**:
  - Reviewing and approving audit reports before dispatch
  - Transmitting emails, LinkedIn messages, or DMs
  - Making cold calls or conducting discovery meetings
  - Closing deals and finalizing service agreements

### 2. Configuring Schedules via `/schedule`
To schedule recurring background tasks:

```bash
/schedule "0 7 * * 1-5" "Run /pursue-top-prospects --count 20"
/schedule "0 16 * * 5" "Run /outcome-analysis"
```

### 3. Managing & Disabling Schedules
List active background tasks and timers:
```bash
/schedule list
```
Cancel or disable a schedule immediately:
```bash
/schedule cancel <task_id>
```

### 4. The Daily Brief
Every morning, scheduled runs compile a scannable executive brief to:
```
outputs/daily_brief.md
```
Provides a 5-minute overview of newly audited prospects, top 3 opportunities, ready-to-send dossiers, and immediate recommended actions.

---

## Top-N Batch Pursuit

Automatically source, score, and batch-audit the top $N$ prospects without making external contact:

```bash
/pursue-top-prospects --count 20 --category "plumber" --location "Austin, TX"
```

- **Meaning of "Pursue"**: Deep research, diagnostic auditing, quality verification, and dossier preparation. **Zero automated human contact**.
- **Iteration Cap**: Enforces a strict upper bound equal to `--count`.
- **Graceful Throttling**: If external scraping endpoints or MCP servers hit rate limits (HTTP 429), the batch halts immediately, reports progress, and saves all completed client dossiers into `outputs/clients/<company-slug>/`.

---

## Token Efficiency & Caching Architecture

The system incorporates rigorous token-optimization strategies designed to minimize inference costs and stay well within API quotas:

### 1. Granular Model Tiering
- **Orchestration / Synthesis (`pro`)**: `business-auditor` handles strategic synthesis, executive narrative development, and roadmaps.
- **Workers & Formatters (`gemini-3.5-flash-low` with `flash` fallback)**: `pillar-auditor`, `report-formatter`, `report-verifier`.
- **Fast Telemetry & Scoring (`gemini-3.1-flash-lite` with `flash` fallback)**: `seo-analyst-gsc`, `seo-analyst-prospect`, `prospect-finder`, `outcome-tracker`.

### 2. Prompt Cache Prefix Locking
Every repetitive subagent instruction set is separated by a `# CACHE PREFIX` block and `---VARIABLE---` marker. Static behavioral rules and schemas are cached by Gemini, avoiding duplicate processing on recurring turns.

### 3. Scoped Context Isolation
Rather than passing monolithic company profiles to all subagents, parent orchestrators pass **domain-scoped slices** (e.g., Sales receives Places and SEO; Support receives sentiment and review counts).

### 4. Local Prefetch Cache & Optimizers
- Telemetry prefetch stores `benchmark.json`, `places.json`, and `seo.json` locally in `outputs/clients/<company-slug>/` to avoid redundant calls.
- Registered optimizer MCP servers: `Antigravity-Cheaper` (Python) and `@ai-optimizer/core` (Node.js) monitor and streamline payload sizes.

---

## Google Sheets Live Pipeline Integration

Connects automated audit intelligence to a live Google Sheet for interactive human sales management:

### 1. Sheet Structure ("Outreach Pipeline")
- **Columns A–K (Automated Agent Zone — Written Contiguously)**:
  - `A`: Business Name
  - `B`: Location
  - `C`: Opportunity Score (1–100)
  - `D`: Tier (`Tier A` | `Tier B` | `Tier C` | `Tier D`)
  - `E`: Audit PDF Link
  - `F`: Video Walkthrough Link
  - `G`: Call Script Link
  - `H`: Suggested Opening Line
  - `I`: Contact Name
  - `J`: Contact Title
  - `K`: LinkedIn Profile URL (left blank if null)
- **Columns L–R (User-Managed Outreach Zone — NEVER TOUCHED BY AGENTS)**:
  - `L`: Outreach Status (`Not Contacted`, `Email Sent`, `Called`, `Replied`, `Meeting Booked`, `Closed`, `Lost`)
  - `M`: Touch 1 Date
  - `N`: Touch 2 Date
  - `O`: Touch 3 Date
  - `P`: Last Touch Result
  - `Q`: Next Action
  - `R`: Notes

### 2. Bidirectional Reconciliation (`/sync-pipeline`)
- **Writing**: `sheet-writer` writes a single contiguous range `A:K`. Columns L–R are never included in any write range.
- **Reading / Syncing**: Run `/sync-pipeline` to pull manual user edits (status changes, follow-up dates, call notes) from columns L–R back into local client dossiers (`conversation_log.md` and `outreach_log.csv`).
- **Resilience**: If the Google Sheets API is offline or unauthenticated, the local audit pipeline proceeds without interruption.

---

## LinkedIn Profile Self-Audit

The **Profile Self-Audit** capability allows consultants and agency operators to audit their **own** LinkedIn profile against the Ideal Customer Profile (ICP) defined in `.agents/rules/icp-definition.md`. It identifies positioning gaps through the eyes of ICP decision-makers (e.g., trade contractor owners, asset advisory principals) and delivers prioritized, copy-paste rewrites.

### 1. How to Run
1. Ensure your public LinkedIn URL is set in `.agents/rules/user-profile.md` (`linkedin_url: "https://www.linkedin.com/in/yourname"`).
2. In the AI Business Auditor chat or terminal, type:
   ```bash
   /audit-my-profile
   ```
   *(If your URL is not configured yet, the workflow will prompt you for it and save it automatically).*

### 2. What It Audits (The Nine Components)
The self-audit systematically inspects and evaluates nine core components of your profile:
1. **Headline**: Keyword density, target role positioning, and quantifiable outcome statements (under 220 characters).
2. **About Section**: Above-the-fold hook (first 265–275 characters), career narrative, proof points, and call to action.
3. **Featured Section**: Lead magnet, case study with metrics, and meeting booking links.
4. **Experience Section**: Action verbs, quantifiable metrics, and tagged/pinned skills per role.
5. **Skills Section**: Top 3 pinned skills matching ICP decision-maker search queries (5+ total).
6. **Custom URL**: Clean vanity handle (`linkedin.com/in/firstnamelastname`).
7. **Profile Photo & Banner**: Professional headshot framing (~60% face) and branded banner with a clear value proposition.
8. **Recommendations**: Minimum of 2 verified recommendations validating operational results.
9. **Recent Activity / Posts**: Insight-driven posts in the last 30 days demonstrating domain authority.

### 3. Deliverable Output
- **Diagnostic Scorecard**: A component-by-component `pass` / `needs-work` / `fail` table with concise diagnostic rationale.
- **Prioritized Fix List**: Actionable findings ranked by leverage:
  - **HIGH**: Headline & About Section (drives search click-through and connection acceptance).
  - **MEDIUM**: Skills, Featured Section, Experience Section (validates credibility).
  - **LOW**: Photo, Banner, Custom URL, Recommendations, Activity.
- **Copy-Paste Rewrites**:
  - 3 alternative headline formulations matching `[Target Role] | [Skill 1] | [Skill 2] | [Outcome Statement]`.
  - Complete 4-part About section draft with positioning hook, narrative, focus areas, and CTA.
  - Top 3 recommended skills to pin.
- **Time-Boxed Action Plan**: Categorized into Quick Wins (< 10 minutes) and Deeper Work (< 1 hour).
- **Optional File Export**: Prompt to save as `outputs/my_profile_audit_{date}.md`.

### 4. Strict Read-Only Governance
- The `profile-self-audit` skill is strictly **READ-ONLY**.
- It **never** invokes any write, message, connection, or profile update tool.
- All recommendations are applied manually by the user via copy-paste.






