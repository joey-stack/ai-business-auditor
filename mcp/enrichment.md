# MCP Server Documentation & Escalation Protocol

This document outlines the Model Context Protocol (MCP) servers integrated into the AI Business Auditor system, detailing their operational roles, exposed tools, escalation triggers, and verification procedures.

---

## The Enrichment Ladder (Replaces Explorium)

```
                    +------------------------------------------+
                    |       Rung 1: ENTIA MCP Server           |
                    |   (Official Registries, VAT, LEI)        |
                    +------------------------------------------+
                                         |
                       [Entity Miss / Thin Dossier / Rate-Limit]
                                         |
                                         v
                    +------------------------------------------+
                    |       Rung 2: Apify Firmographic         |
                    |      (Domain Meta, Revenue, Bands)       |
                    +------------------------------------------+
                                         |
                             [No Records / Missing]
                                         |
                                         v
                    +------------------------------------------+
                    |       Rung 3: OpenCorporates MCP         |
                    |    (Global Incorporation, Officers)      |
                    +------------------------------------------+
                                         |
                         [Total Failure of Structured APIs]
                                         |
                                         v
                    +------------------------------------------+
                    |             SCRAPER LADDER               |
                    | (Careers, Blog, Docs, Headless Crawler)  |
                    +------------------------------------------+
```

---

### Rung 1: ENTIA MCP Server (Primary)

- **Provider**: PrecisionAI Marketing OÜ (`entia.systems`).
- **Transport**: Remote SSE / HTTP MCP (`https://mcp.entia.systems/mcp`).
- **Free Tier Policy**: TRACE tier (~100 calls/month free, no credit card required).
- **Authentication**: `x-entia-key: <key>`. Self-serve key generation via `POST https://api.entia.systems/api/v1/mcp/register` with `{"email": "...", "source": "self_serve_machine"}`.
- **Tools Exposed**:
  - `entity_lookup`: Resolves canonical business identity, Trust Score, VAT validation, and legal registration numbers across 10+ countries.
  - `get_full_dossier`: Aggregates entity verification, registry corroboration, corporate status, and official metadata in a single call.
  - `verify_vat`: Real-time European VIES VAT number validation across 27 EU member states.
  - `search_entities`: Discovers businesses filtered by sector code, geography, and name.
  - `get_competitors`: Retrieves verified local/sector competitors with contact indicators.
  - `zone_profile`: Demographic and economic context based on postal code.
  - `run_risk_audit`: Corporate risk signals, compliance checks, and registry discrepancy alerts.
- **Usage Pattern**:
  1. Primary call: `entity_lookup(q="target-domain.com")` or `get_full_dossier(q="Company Name")`.
  2. Call `get_competitors` to extract 2-3 named competitors for the audit's competitive benchmarking requirement.
- **Escalation Trigger to Rung 2**:
  - The domain fails to resolve to a recognized corporate entity.
  - The target business is outside covered registry jurisdictions (e.g., regional US LLCs not in global GLEIF).
  - The monthly 100-request TRACE quota is reached (HTTP 429).

---

### Rung 2: Apify "Company Firmographic Enricher" (Fallback Rung 2)

- **Provider**: Mamba Labs (`@mambalabsdev/mcp-company-firmographic-enricher`).
- **Transport**: Local Stdio via `npx` wrapper.
- **Free Tier Policy**: Utilizes Apify's monthly free platform compute tier ($5/month).
- **Authentication**: `APIFY_TOKEN` environment variable.
- **Tools Exposed**:
  - `enrich_company_firmographics`: Ingests a domain name and parses website `schema.org/Organization` JSON-LD, OpenGraph tags, and meta records.
- **Data Returned**:
  - Estimated revenue bracket.
  - Employee headcount band.
  - Headquarters city and country.
  - Founded year and industry category.
  - Data completeness score and signal provenance.
- **Usage Pattern**:
  - Invoke when ENTIA provides strong legal entity verification but lacks estimated revenue brackets or granular employee headcount bands.
- **Escalation Trigger to Rung 3**:
  - Apify returns `data_completeness < 0.3` or fails to locate `schema.org` organization tags on the company website.
  - Apify monthly free compute credits are exhausted.

---

### Rung 3: OpenCorporates MCP (Fallback Rung 3)

- **Provider**: OpenCorporates global database via `pipeworx-io/mcp-open-corporates`.
- **Transport**: Remote MCP gateway (`https://mcp.pipeworx.io/opencorporates`).
- **Free Tier Policy**: Free API token with strict per-minute and monthly rate-limiting.
- **Authentication**: `Authorization: Bearer <OPENCORPORATES_API_KEY>`.
- **Tools Exposed**:
  - `search_companies`: Global entity lookup by registered legal name across 140+ jurisdictions.
  - `get_company_details`: Extracts incorporation date, registered agent, filing status, and official address.
  - `search_officers`: Identifies registered directors and corporate officers.
- **Escalation Trigger to Scraper Ladder**:
  - Legal records do not contain operational information (no employee estimates, no tech stack indicators, no revenue data).

---

## The Scraper Ladder (Replaces Tavily)

The Scraper Ladder is triggered automatically when:
1. Structured MCP enrichment fails or produces an incomplete profile.
2. Technographic data is needed (since **no free MCP server provides technographics**).

### Rungs & Tooling
1. **Rung 1 — `ai-first-search`**:
   - Lightweight search pattern designed to extract clean Markdown without tracking or session state.
2. **Rung 2 — `Spectrawl` (`@iflow-mcp/fayandxan-spectrawl`)**:
   - Self-hosted multi-engine search aggregator (SearXNG + Brave Search 2,000/mo free API). Handles anti-bot protection and extracts markdown text from dynamic single-page apps.
3. **Rung 3 — `Crawl4AI` / Native Environment Tools**:
   - Headless crawler using Playwright and BeautifulSoup4.
   - Built-in Fallback: Native `search_web` and `read_url_content` tools provide zero-configuration extraction of careers pages, engineering blogs, and public repositories.

### Technographic Extraction Pattern
To infer the technology stack without paid tools (e.g. BuiltWith, Wappalyzer):
1. **Target URLs to Scrape**:
   - `domain.com/careers` or `domain.com/jobs`
   - Company profiles on public job boards (LinkedIn, Greenhouse, Lever, Ashby, Workable)
   - `domain.com/engineering` or company engineering blogs on Medium / Substack
   - Company public GitHub / GitLab organizations
   - HTML footer credits, cookie consent vendors, and script tags
2. **Inference & Confidence Scoring**:
   - Mentioned in active job requirements (e.g., "5+ years with PostgreSQL and Kubernetes") -> **`confidence: high`**
   - Sourced from engineering blog posts or public GitHub repositories -> **`confidence: medium`**
   - Inferred from industry standard or general integrations -> **`confidence: low`**
3. **Citation Requirement**:
   - Every detected technology must explicitly reference its origin URL or listing.

---

## How to Verify MCP Servers in Antigravity

To verify that the MCP servers configured in `.agents/mcp_config.json` are active and recognized by Antigravity:

1. **Via the User Interface**:
   - Click the `…` (Additional Options) menu in the top or side pane.
   - Select **MCP Servers**.
   - Confirm that `entia`, `company-firmographic-enricher`, and `opencorporates` appear in the server list with their registered tools.
2. **Via Command Palette / Chat**:
   - Check the active tool list in any agent turn; discovered MCP tools will be visible in the agent's callable tool declarations.
