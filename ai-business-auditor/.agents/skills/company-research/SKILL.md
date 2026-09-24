---
name: company-research
description: Builds a firmographic and technographic profile for a business from its domain, using MCP enrichment tools with a web-scraping fallback. Use when the user provides a company URL and needs company size, revenue, industry, locations, or tech stack data.
---

# Company Research Skill

This skill executes a multi-source firmographic investigation and technographic inference on a target company domain, walking an escalation ladder of free-tier tools to construct an intelligence profile.

---

## 1. Input Specification

- **Input Parameter**: `domain` (Clean, normalized domain string, e.g., `stripe.com`, `linear.app`).
- **Prerequisite**: URL normalization (stripping `http://`, `https://`, `www.`, paths, and tracking queries).

---

## 2. Step-by-Step Execution Workflow

### Step 1: Query Enrichment Rung 1 (ENTIA MCP)
1. Attempt corporate entity resolution using `entity_lookup(q=domain)` or `get_full_dossier(q=company_name)`.
2. Extract official registered entity name, country of incorporation, European VAT/VIES status, GLEIF LEI code, and registry corroboration.
3. Query `get_competitors` to retrieve 2-3 named industry competitors.
4. If successful, record `"ENTIA MCP Server"` in `data_sources_used`.
5. If entity resolution fails, the domain is not in the database, or an HTTP 429 quota error occurs:
   - Record the event in `failed_sources` or `rate_limit_events`.
   - Escalate directly to Step 2.

### Step 2: Augment with Rung 2 (Apify Firmographic Enricher)
1. Invoke `enrich_company_firmographics(domain=domain)`.
2. Extract:
   - Estimated revenue range (e.g., `"$10M - $50M"`).
   - Headcount band (e.g., `"100-250"`).
   - Headquarters city and country.
   - Primary industry classification.
3. If successful, record `"Apify Company Firmographic Enricher"` in `data_sources_used`.
4. If Apify credits are depleted or the actor cannot parse the target site:
   - Record in `failed_sources`.
   - Escalate to Rung 3 (OpenCorporates MCP) or the Scraper Ladder.

### Step 3: Scraper Ladder Fallback (For Sparse Firmographics)
1. If structured MCP tools failed or returned incomplete firmographics, trigger the scraper ladder:
   - Query company `/about`, `/contact`, and `/press` pages.
   - Run web searches for official press releases, Crunchbase profiles, or LinkedIn company directory listings.
   - Extract company size, founding year, and office locations from verified public statements.

### Step 3b: Google Places Reputation & Location Enrichment
1. Once company name and location are resolved, invoke the `places-enrichment` skill.
2. Pull physical address, phone number, Google star rating, review count, and sentiment summary.
3. Record `match_confidence` (`high`, `medium`, `low`) and save to `places_data`.

### Step 3c: Google Search Console SEO Telemetry (Conditional)
1. Invoke the `seo-analyst` subagent with the normalized domain.
2. If the domain is not verified under the authenticated account, record `skipped: true` and the reason.
3. If verified, pull 90-day search performance, quick wins, and indexing flags into `seo_data`.

### Step 4: Technographic Inference Protocol (Mandatory)
*Notice: Free MCP servers do not provide automated technographics. You must perform active inference.*

1. **Target Inspection Points**:
   - Company Careers Page (e.g., `domain/careers`, `domain/jobs`).
   - Active Job Listings (look for software engineer, marketing ops, customer support, and sales ops postings).
   - Engineering Blog / Technical Documentation.
   - Public GitHub / GitLab Repositories or Open Source contributions.
   - Client-side scripts, analytics tags, cookie banners, and footer credits.
2. **Inference & Confidence Scoring**:
   - `high`: Directly listed in active job posting requirements (e.g., "Must have 3+ years experience with Snowflake, dbt, and React") or declared in official engineering documentation.
   - `medium`: Inferred from public open-source repos, employee developer posts, or visible frontend tracking scripts.
   - `low`: Inferred from standard industry integrations or indirect partner badges.
3. **Citation Requirement**:
   - For every tool discovered, write an explicit evidentiary source (e.g., `"source": "Staff DevOps Engineer job listing on Lever"`). Never omit the source. Never state an inferred tool as an absolute verified fact.

### Step 5: Synthesize and Validate Dossier JSON
Assemble all extracted intelligence into a single JSON object strictly matching the schema below.

---

## 3. Output JSON Schema

```json
{
  "company_name": "Acme Corporation",
  "domain": "acme.com",
  "revenue_range": "$10M - $25M",
  "employee_count": "50-100",
  "locations": [
    "Austin, TX, USA",
    "London, UK"
  ],
  "industry": "B2B SaaS / Workflow Automation",
  "technographics": [
    {
      "tool": "PostgreSQL",
      "confidence": "high",
      "source": "Senior Backend Engineer job posting on /careers"
    },
    {
      "tool": "HubSpot CRM",
      "confidence": "medium",
      "source": "Tracking script header and marketing operations job listing"
    },
    {
      "tool": "AWS (ECS/Fargate)",
      "confidence": "high",
      "source": "Infrastructure Lead job listing on LinkedIn"
    },
    {
      "tool": "Zendesk",
      "confidence": "medium",
      "source": "Public support portal subdomain support.acme.com"
    }
  ],
  "places_data": {
    "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4",
    "matched_name": "Acme Corporation",
    "formatted_address": "123 Market St, Suite 400, Austin, TX 78701",
    "phone": "+1 512-555-0199",
    "website": "https://acme.com",
    "rating": 4.6,
    "review_count": 128,
    "opening_hours": ["Monday-Friday: 9:00 AM – 6:00 PM"],
    "recent_reviews_summary": "Strong feedback on enterprise onboarding; minor complaints regarding response times during weekends.",
    "match_confidence": "high"
  },
  "seo_data": {
    "property": "sc-domain:acme.com",
    "date_range": "2026-06-15 to 2026-09-15",
    "skipped": false,
    "skip_reason": null,
    "top_queries": [
      { "query": "workflow automation platform", "clicks": 4200, "impressions": 58000, "ctr": 0.072, "position": 3.4 }
    ],
    "quick_win_queries": [
      { "query": "b2b integration tools", "impressions": 12500, "ctr": 0.012, "opportunity": "High impressions on page 2; title optimization could 3x clicks." }
    ],
    "declining_pages": [],
    "indexing_issues": [],
    "score": 8,
    "rationale": "Solid topical authority in workflow automation with healthy CTR on core commercial terms.",
    "reasoning_scaffold": {
      "evidence": ["Rank 3.4 for primary head term with 7.2% CTR"],
      "expected_state": "Top 3 rankings with >5% CTR for category leaders",
      "gap_description": "Secondary long-tail queries under-indexed on page 2"
    }
  },
  "data_sources_used": [
    "ENTIA MCP Server (entity_lookup)",
    "Apify Company Firmographic Enricher",
    "Google Places API",
    "Google Search Console API",
    "Native Scraper (/careers, /about)"
  ],
  "failed_sources": [],
  "rate_limit_events": []
}
```
