---
name: competitor-benchmark
description: "Identifies 2-3 local competitors for a prospect and collects their key metrics (review count, rating, website presence, estimated traffic, Domain Rating) to establish a benchmark for the audit. Use before the pillar audits run."
---

# Competitor Benchmark Skill (`competitor-benchmark`)

This skill identifies active market leaders and sector competitors in the prospect's operating trade and municipal market, extracting quantitative performance metrics to establish empirical benchmarks for downstream pillar diagnostics.

---

## 1. Purpose

Establish a realistic local competitive benchmark for the target business, identifying standard operational and visibility levels achieved by top-ranking peers in the same market.

---

## 2. Input Specification

- **`business_name`** (`string`, required): Name of the target prospect business.
- **`category`** (`string`, required): Business trade or sector (e.g., `"plumbing"`, `"HVAC contractor"`, `"asset management"`).
- **`location`** (`string`, required): Operating city or region (e.g., `"Austin, TX"`, `"Abuja, Nigeria"`).

---

## 3. Step-by-Step Execution Process

1. **Discover Local Market Leaders**:
   - Query Google Maps via `gmaps-mcp` (`search_google_maps`) with `"{category} in {location}"`.
   - Exclude the prospect business itself.
   - Filter and select **2 to 3 competitors** with the highest review counts and active presence (the recognized local leaders).

2. **Collect Competitor Telemetry**:
   For each selected competitor:
   - Extract: `name`, `rating`, `review_count`, and `website_url`.
   - Inquire SEO authority:
     - Estimate Domain Rating (DR) via Ahrefs / PageSpeed / public metrics.
     - Estimate monthly organic search traffic via FetchSERP or SE Ranking.
   - If traffic or DR cannot be fetched for a competitor, note estimation tier or fallback.

3. **Compute Benchmark Averages**:
   - Calculate mathematical averages across the 2–3 competitors:
     - Average Google star rating.
     - Average total review count.
     - Average Domain Rating (DR).
     - Average monthly organic search visits.

4. **Compile Benchmark Deliverable**:
   Structure the outputs into the standard benchmark JSON schema.

---

## 4. Output JSON Schema

```json
{
  "category": string,
  "location": string,
  "competitors": [
    {
      "name": string,
      "rating": number,
      "review_count": number,
      "has_website": boolean,
      "website_url": string | null,
      "domain_rating": number,
      "estimated_traffic": number
    }
  ],
  "benchmark_averages": {
    "rating": number,
    "review_count": number,
    "domain_rating": number,
    "estimated_traffic": number
  }
}
```

---

## 5. Constraints & Governance

- Competitors must be active, real entities operating in the exact same market.
- Benchmarks must reflect factual observed data; never fabricate competitor review volumes or ratings.
- Competitor findings are passed into the company profile JSON under `competitor_benchmark` for consume by `pillar-auditor` and `business-auditor`.
