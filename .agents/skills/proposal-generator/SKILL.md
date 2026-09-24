---
name: proposal-generator
description: "Generates a one-page proposal PDF from a completed audit, including findings, recommended engagement, timeline, and pricing. Use after a prospect has expressed interest."
---

# Proposal Generator Skill (`proposal-generator`)

This skill converts diagnostic audit findings into a polished, client-ready proposal document and PDF deliverable, mapping observed friction points to structured pricing tiers.

---

## 1. Purpose

Produce an executive, client-ready proposal for a specific prospect, clearly detailing the situation, 3 key findings, proposed solution package, 30-60-90 day timeline, investment terms, and concrete next steps.

---

## 2. Input Specification

- **`company_name`** (`string`, required): Name of the prospect business.
- **`audit_json`** (`object`, required): The completed audit record containing scores, evidence, and gaps.
- **`pricing_tier`** (`"starter" | "standard" | "premium"`, required): Selected pricing tier from [`.agents/rules/pricing.md`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/.agents/rules/pricing.md).

---

## 3. Step-by-Step Execution Process

1. **Extract Core Findings**:
   - Analyze the audit findings and select the **3 most critical operational or commercial bottlenecks** (e.g., missed inbound leads, zero mobile booking, low review velocity compared to local benchmark).

2. **Map to Engagement Tier**:
   - Reference [`.agents/rules/pricing.md`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/.agents/rules/pricing.md) to extract deliverables, monthly investment amount, and scope for the designated `pricing_tier`.

3. **Draft Structured Proposal**:
   Generate a clear Markdown proposal document containing:
   - **Situation Summary**: 2–3 sentences contextualizing the prospect's current local position.
   - **Key Findings**: The 3 prioritized findings framed as high-leverage growth opportunities.
   - **Recommended Engagement**: Plain-language description of systems to be deployed.
   - **Timeline (30-60-90 Days)**:
     - *Days 1–30*: Immediate setup, GBP optimization, review engine deployment, foundational fixes.
     - *Days 31–60*: Modern landing page/site deployment, keyword targeting, lead capture automation.
     - *Days 61–90*: AI inquiry triage integration, ongoing optimization, competitor displacement.
   - **Investment**: Explicit pricing from `.agents/rules/pricing.md`, clearly stating what is included.
   - **Next Steps**: Exact onboarding path to initiate the engagement.

4. **Persistence & PDF Compilation**:
   - Save Markdown to `outputs/clients/{slug}/proposal.md`.
   - Compile PDF via Pandoc:
     ```bash
     pandoc outputs/clients/{slug}/proposal.md -o outputs/clients/{slug}/proposal.pdf
     ```

---

## 4. Governance Constraints

- All proposals must draw pricing and deliverables exclusively from [`.agents/rules/pricing.md`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/.agents/rules/pricing.md). Never improvise pricing figures.
- Findings must be grounded in the verified audit data.
- The proposal deliverable must be reviewed and approved by the human consultant before transmission to the prospect.
