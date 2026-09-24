---
name: business-audit
description: Orchestrates four parallel pillar auditors and synthesizes their findings into an executive summary, scoring matrix, deep dives, and roadmaps for a complete business audit. Use after a company profile has been built.
---

# Business Audit Orchestration Skill

This skill orchestrates the multi-agent diagnostic process by spawning four concurrent `pillar-auditor` subagents and synthesizing their findings into an executive-ready audit deliverable.

---

## 1. Input Specification
- **Input Parameter**: Complete `company-research` JSON profile.
- **Context Isolation Rule**: Because subagents execute in isolated context windows without inheriting the parent's conversation history, this skill requires passing the **entire company profile JSON explicitly** to each child subagent.

---

## 2. Orchestration Process

### Step 1: Concurrent Subagent Dispatch
Spawn **FOUR `pillar-auditor` subagents concurrently in parallel** using `invoke_subagent`.
Do NOT execute them sequentially.

Each subagent prompt must contain:
1. The **complete company profile JSON**.
2. The specific assigned pillar name:
   - Worker 1: `Sales & Marketing`
   - Worker 2: `Customer Support`
   - Worker 3: `Product & Service Delivery`
   - Worker 4: `Internal Operations & Infrastructure`
3. The instruction to walk the mandatory 4-step reasoning scaffold (`Evidence → Expected State → Gap → Score`) before returning.

*(Note: Detailed diagnostic criteria and evaluation dimensions for each individual pillar are maintained inside the [pillar-auditor](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/.agents/agents/pillar-auditor.md) subagent).*

### Step 2: Await & Validate Child Deliverables
Wait for all four parallel `pillar-auditor` subagents to complete execution.
Verify that each returned deliverable includes:
- `pillar`
- `current_state`
- `gaps` (list of strings)
- `ai_leverage` (list of strings)
- `score` (integer 1-10)
- `rationale` (written explanation)
- `reasoning_scaffold` (`evidence`, `expected_state`, `gap_description`)

### Step 3: Synthesis, Financialization & Roadmap Architecture
Merge the four independent evaluations into the final consolidated audit deliverable:
1. **Scoring Matrix**: Combine the 4 scores, rationales, and reasoning scaffolds.
2. **Economic Leakage Modeling**: Synthesize the estimated annual and monthly financial leakage across all 4 pillars using observable volume, conversion loss, and average deal sizes.
3. **Domain Deep Dives**: Consolidate Current State, Identified Gaps, Financial Impact, and Proposed AI Leverage for all 4 pillars using Minto Pyramid Action Titles.
4. **Executive Summary**: Synthesize an overarching strategic narrative, identifying top unforced errors, estimated total financial leakage, and the top 3 high-leverage AI opportunities.
5. **Actionable Roadmaps & Deloitte Payback Matrix**:
   - *Effort vs. Impact Matrix*: Table detailing Implementation Effort, Estimated Cost ($), 90-Day Gross Value Recovery ($), and Estimated Payback Period.
   - *Quick Wins*: High-ROI interventions deployable in **under 2 weeks**.
   - *Strategic Initiatives*: Transformative projects spanning **3 to 6 months**.
   - *Phased 30-60-90 Day Plan*: Structured milestones broken down into Day 30, Day 60, and Day 90 execution goals.

---

## 3. Output JSON Schema

```json
{
  "company_name": "Acme Corporation",
  "audit_date": "2026-09-15",
  "executive_summary": "High-level strategic narrative...",
  "financial_leakage_summary": {
    "estimated_monthly_leakage_usd": 68000,
    "estimated_annual_leakage_usd": 816000,
    "methodology_summary": "Derived from 52% mobile bounce rate penalty, after-hours emergency call abandonment, and manual dispatch friction."
  },
  "deloitte_payback_matrix": [
    {
      "initiative": "Automated Post-Service Review Engine",
      "pillar": "Sales & Marketing",
      "effort_complexity": "Low (3 days)",
      "estimated_setup_cost_usd": 500,
      "projected_90_day_recovery_usd": 22500,
      "payback_horizon": "< 14 Days"
    },
    {
      "initiative": "LiteSpeed Cache & Frontend Speed Overhaul",
      "pillar": "Sales & Marketing",
      "effort_complexity": "Low (1 day)",
      "estimated_setup_cost_usd": 750,
      "projected_90_day_recovery_usd": 18000,
      "payback_horizon": "< 7 Days"
    },
    {
      "initiative": "24/7 AI Emergency Call & Chat Triage",
      "pillar": "Customer Support",
      "effort_complexity": "Medium (2 weeks)",
      "estimated_setup_cost_usd": 3000,
      "projected_90_day_recovery_usd": 43500,
      "payback_horizon": "< 21 Days"
    }
  ],
  "scoring_matrix": [
    {
      "pillar": "Sales & Marketing",
      "score": 6,
      "rationale": "Evidentiary rationale from pillar auditor"
    },
    {
      "pillar": "Customer Support",
      "score": 4,
      "rationale": "Evidentiary rationale from pillar auditor"
    },
    {
      "pillar": "Product & Service Delivery",
      "score": 7,
      "rationale": "Evidentiary rationale from pillar auditor"
    },
    {
      "pillar": "Internal Operations & Infrastructure",
      "score": 6,
      "rationale": "Evidentiary rationale from pillar auditor"
    }
  ],
  "deep_dives": [
    {
      "pillar": "Sales & Marketing",
      "action_title": "Suppressed Review Velocity & 7-Second Mobile Latency Cede $54k/Mo to Metro Competitors",
      "current_state": "...",
      "gaps": ["..."],
      "financial_impact": "Estimated $54,000/mo in lost emergency dispatch bookings due to 6.9s mobile TTFB and sub-50 review volume.",
      "ai_leverage": ["..."]
    },
    {
      "pillar": "Customer Support",
      "action_title": "Absence of 24/7 Voice/SMS AI Triage Diverts 10+ High-Margin After-Hours Calls Monthly",
      "current_state": "...",
      "gaps": ["..."],
      "financial_impact": "Estimated $14,500/mo in forfeited emergency plumbing jobs abandoned during peak evening hours.",
      "ai_leverage": ["..."]
    },
    {
      "pillar": "Product & Service Delivery",
      "action_title": "Single-Item Estimate Formatting Suppresses Average Ticket Size by 20% to 30%",
      "current_state": "...",
      "gaps": ["..."],
      "financial_impact": "Estimated $18,000/mo in unrealized upsell margin across major water heater and whole-home filtration replacements.",
      "ai_leverage": ["..."]
    },
    {
      "pillar": "Internal Operations & Infrastructure",
      "action_title": "Misconfigured SPF/DMARC Infrastructure Puts Corporate Invoices and Estimates at Spam Risk",
      "current_state": "...",
      "gaps": ["..."],
      "financial_impact": "Delayed payment collections and quote decay due to strict p=quarantine mail server rejection.",
      "ai_leverage": ["..."]
    }
  ],
  "roadmaps": {
    "quick_wins": [
      "Intervention deployable in < 2 weeks"
    ],
    "strategic_3_to_6_months": [
      "Medium term initiative"
    ],
    "phased_30_60_90": {
      "day_30": ["Foundational milestone"],
      "day_60": ["Process integration milestone"],
      "day_90": ["Scaling and metrics milestone"]
    }
  }
}
```
