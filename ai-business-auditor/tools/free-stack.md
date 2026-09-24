# Free & Open-Source Tooling Stack Reference

This document catalogs every component of the 100% free and open-source architecture underpinning the AI Business Auditor, detailing replacements of commercial SaaS, exact tier caps, configuration steps, known failure modes, and throughput ceilings.

---

## Architectural Replacements Matrix

| Functional Role | Original Paid Tool | Free Stack Replacement | Free Tier Quota / Limits | Primary Failure Mode | Fallback Strategy |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Entity Verification & VAT** | Explorium / ZoomInfo | **ENTIA MCP Server** | 100 calls/month (TRACE tier, 0€, no CC) | Out-of-region entity or 429 quota exhaustion | Escalate to Apify Firmographics |
| **Firmographics & Revenue** | Explorium / Clearbit | **Apify "Company Firmographic Enricher"** | $5/month free platform compute | `schema.org` meta missing on site | Escalate to OpenCorporates / Scrapers |
| **Legal Registration & Officers** | Dun & Bradstreet | **OpenCorporates MCP** | Free token (rate-limited per-minute) | Token rate limit / missing revenue | Escalate to Scraper Ladder |
| **Search & Web Extraction** | Tavily Search API | **Spectrawl / Crawl4AI / Native Tools** | Self-hosted (2,000 Brave queries/mo free; unlimited local) | Dynamic JS rendering / anti-bot blocks | Native Antigravity headless scraper |
| **Report Export & Typography** | Google Workspace / Docs | **Local Pandoc / Python ReportLab** | Unlimited local execution (0 cloud egress) | Pandoc binary not in PATH | Bundled local Python ReportLab script |
| **Shareable Client Link** | Google Drive / Box | **Notion API (Free Personal Plan)** | Free unlimited personal pages & blocks | API key unconfigured | Local PDF serves as final deliverable |

---

## Detailed Tool Specifications

### 1. ENTIA MCP Server (Replaces Explorium / ZoomInfo)
- **Role**: Primary business identity corroboration, legal name resolution, European VAT validation (VIES), and risk signals.
- **Free Tier Caps**: 100 requests per calendar month on the TRACE tier.
- **Setup Steps**:
  1. Visit `https://entia.systems/mcp-setup` to obtain an API key, or use the machine registration API:
     ```bash
     curl -X POST https://api.entia.systems/api/v1/mcp/register \
       -H "Content-Type: application/json" \
       -d '{"email": "your_email@example.com", "source": "self_serve_machine"}'
     ```
  2. Set the `ENTIA_API_KEY` environment variable or place it directly in `.agents/mcp_config.json`.
- **Known Failure Modes**:
  - Unregistered or early-stage regional startups might not be indexed in European mercantile gazettes or GLEIF.
  - Hitting the 100 calls/month TRACE limit returns an HTTP 429 response.
- **Escalation**: Log to `failed_sources` and proceed to Apify.

---

### 2. Apify "Company Firmographic Enricher" (Replaces Clearbit)
- **Role**: Secondary enrichment for estimated revenue bracket, employee headcount, headquarters, and industry.
- **Package**: `@mambalabsdev/mcp-company-firmographic-enricher`.
- **Free Tier Caps**: Apify provides $5.00/month in free platform credits (approx. 250-500 domain lookups).
- **Setup Steps**:
  1. Sign up for a free Apify account at `apify.com`.
  2. Copy your API token from **Settings > Integrations > API Tokens**.
  3. Export `APIFY_TOKEN=apify_api_...` in your shell or IDE environment.
- **Known Failure Modes**:
  - Websites built strictly with obfuscated single-page applications lacking `schema.org/Organization` JSON-LD will return low completeness scores.
- **Escalation**: Proceed to OpenCorporates or trigger career-page scraping.

---

### 3. OpenCorporates MCP (Replaces Dun & Bradstreet)
- **Role**: Legal entity registration, jurisdiction, corporate number, and officer records.
- **Free Tier Caps**: Non-commercial developer account with strict rate limiting.
- **Setup Steps**:
  1. Register for an API key at `opencorporates.com`.
  2. Set `OPENCORPORATES_API_KEY` in environment variables.
- **Known Failure Modes**:
  - Strictly limited to incorporation filings; provides zero technographics or marketing data.
- **Escalation**: Escalate directly to the Scraper Ladder.

---

### 4. Scraper Ladder: Spectrawl & Crawl4AI (Replaces Tavily)
- **Role**: Scraping target company career portals, engineering blogs, documentation, and HTML footers to infer technographics and identify friction points.
- **Free Tier Caps**: Unlimited local execution; Brave Search API offers 2,000 free queries/month if using Spectrawl's search aggregator.
- **Setup Steps**:
  - Native tools are available immediately in Antigravity.
  - Python crawler dependencies are already installed: `python -m pip install beautifulsoup4 playwright requests`.
- **Known Failure Modes**:
  - Aggressive Cloudflare Turnstile or CAPTCHA challenges on career portals.
- **Escalation**: Fall back to native Antigravity `read_url_content` and `search_web`.

---

### 5. Local PDF Engine: Pandoc & ReportLab (Replaces Google Workspace)
- **Role**: Compiling the Markdown audit report into an executive-ready PDF deliverable.
- **Free Tier Caps**: 100% free and open-source. Runs entirely on local CPU with zero network egress.
- **Setup Steps**:
  - Optional Pandoc installation on Windows:
    ```powershell
    winget install --id JohnMacFarlane.Pandoc -e
    ```
  - Bundled fallback script (`.agents/skills/report-export/scripts/md_to_pdf.py`) requires only Python with `reportlab`, which is already installed in this environment.
- **Known Failure Modes**:
  - Missing Pandoc binary -> Automatically handled by transparent fallback to the bundled Python ReportLab script.

---

### 6. Notion API (Optional Cloud Share)
- **Role**: Producing an interactive web link for clients who request an online version of the report.
- **Free Tier Caps**: Unlimited personal workspace pages and blocks.
- **Setup Steps**:
  1. Create an internal integration at `notion.so/my-integrations`.
  2. Set `NOTION_API_KEY` and grant access to a parent page (`NOTION_PARENT_PAGE_ID`).
- **Known Failure Modes**:
  - If unconfigured, the system automatically skips cloud sharing without throwing an error.

---

## Throughput & Scaling Analysis

> [!NOTE]
> **Throughput Realities for Low-Volume vs High-Volume Production**
>
> This free-and-open-source stack is engineered for **boutique, low-volume consultancy operations**:
> - **Optimal Capacity**: 5 to 15 full corporate audits per week.
> - **Bottlenecks**: At this volume, all requests remain well beneath ENTIA's 100 req/month cap, Apify's $5 free tier, and local system resources.
>
> **Scaling Path (Without Architectural Redesign)**:
> If audit throughput exceeds 50 audits per week, the external free tiers will be exhausted. The architectural fix does **not** require rewriting agents or changing tools:
> 1. Deploy `Spectrawl` and `SearXNG` onto a single $5/month Linux VPS (Hetzner, DigitalOcean, or Linode) to handle unlimited concurrent headless scraping.
> 2. Upgrade the ENTIA tier or route high-volume registry lookups directly through regional government open data mirrors (e.g., UK Companies House free public API, SEC EDGAR free API, EU VIES public SOAP/REST).
> The agent contracts, scoring matrix, and output formats remain completely identical.
