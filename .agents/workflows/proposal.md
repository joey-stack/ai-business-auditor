---
name: proposal
description: "Generates a structured, client-ready proposal document and PDF deliverable for a specific prospect based on completed audit findings and standardized pricing tiers."
---

# /proposal — Client Proposal Generation Workflow

This workflow transforms diagnostic audit findings into an executive proposal outlining recommended packages, implementation timelines, and exact pricing.

---

## Trigger
The user types:
```
/proposal "<prospect name>"
```

---

## Steps

### Step 1 — Locate Completed Audit
1. Compute the prospect's client slug using the canonical slug algorithm.
2. Search `outputs/clients/{slug}/` for the audit Markdown file:
   ```
   outputs/clients/{slug}/audit_*.md
   ```
3. If no completed audit is found, alert the user:
   > *"No completed audit found for '{prospect name}'. Please run `/audit <website_url>` first before generating a proposal."*
   and halt execution.

### Step 2 — Pricing Tier Recommendation & Selection
1. Evaluate the prospect scale and audit score:
   - Tier D / Low Review Count (< 20) → Recommend **Starter Tier** ($750/mo).
   - Tier C / Moderate Scale (10–25 employees, outdated web) → Recommend **Standard Tier** ($1,750/mo).
   - Tier A/B / High Volume (> 25 employees, multiple locations) → Recommend **Premium Tier** ($3,500/mo).
2. Present the recommended tier and confirm tier selection with the user.

### Step 3 — Invoke Proposal Generator
1. Invoke the **`proposal-generator`** skill with:
   - `company_name`: Resolved prospect name
   - `audit_json`: Audit findings and gap analysis
   - `pricing_tier`: Confirmed pricing tier
2. Generate Markdown proposal at `outputs/clients/{slug}/proposal.md`.
3. Compile PDF deliverable at `outputs/clients/{slug}/proposal.pdf`.

### Step 4 — Presentation & Approval Checkpoint
1. Display the proposal summary in chat along with links to the generated Markdown and PDF artifacts.
2. Ask the user:
   > *"Want me to edit anything, or is this ready to send to the client?"*

Do NOT transmit or share the proposal until the human consultant confirms.
