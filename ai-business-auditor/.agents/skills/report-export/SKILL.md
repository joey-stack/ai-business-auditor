---
name: report-export
description: Converts a completed business audit JSON into a Markdown report, renders it to PDF via Pandoc, and optionally publishes it to Notion. Use after the business-audit skill has produced a scored report.
---

# Report Export Skill

This skill formats the structured diagnostic intelligence into an executive-ready Markdown document, compiles a local PDF deliverable via Pandoc (or bundled local Python renderer), and optionally publishes a shareable page to Notion.

---

## 1. Input Specification

- **Input Parameter**: Complete `business-audit` JSON output (alongside data sources and technographics from `company-research`).

---

## 2. Formatting & Assembly Workflow

### Step 1: Render JSON into Structured Markdown
Construct a clean, professional Markdown report with the following exact structural hierarchy:

```markdown
# AI Business Diagnostic Audit: {company_name}
**Audit Date**: {audit_date} | **Scope**: 4-Pillar Executive Diagnostic

---

## 1. Executive Summary
{executive_summary}

### Key Unforced Errors
- ...

### Top High-Leverage AI Interventions
1. ...
2. ...
3. ...

---

## 2. Four-Pillar Scoring Matrix

| Pillar | Score (1-10) | Evidentiary Written Rationale |
| :--- | :---: | :--- |
| **Sales & Marketing** | {score} | {rationale} |
| **Customer Support** | {score} | {rationale} |
| **Product & Service Delivery** | {score} | {rationale} |
| **Internal Operations & Infrastructure** | {score} | {rationale} |

---

## 3. Domain Deep Dives

### Pillar 1: Sales & Marketing
- **Current Operational State**: ...
- **Identified Friction Points & Gaps**:
  - ...
- **Targeted AI Leverage**:
  - ...

### Pillar 2: Customer Support
- **Current Operational State**: ...
- **Identified Friction Points & Gaps**:
  - ...
- **Targeted AI Leverage**:
  - ...

### Pillar 3: Product & Service Delivery
- **Current Operational State**: ...
- **Identified Friction Points & Gaps**:
  - ...
- **Targeted AI Leverage**:
  - ...

### Pillar 4: Internal Operations & Infrastructure
- **Current Operational State**: ...
- **Identified Friction Points & Gaps**:
  - ...
- **Targeted AI Leverage**:
  - ...

---

## 4. Transformation Roadmaps

### Quick Wins (< 2 Weeks)
- ...

### Strategic Initiatives (3 to 6 Months)
- ...

### Phased 30-60-90 Day Plan
- **Day 30**: ...
- **Day 60**: ...
- **Day 90**: ...

---

## 5. Technographic Profile (Inferred Stack)

| Technology / Tool | Confidence Level | Evidentiary Source |
| :--- | :---: | :--- |
| {tool} | `{confidence}` | {source} |

*Notice: Technographics are inferred from public job descriptions, engineering documentation, and repository footprints; never presented as absolute verified fact.*

---

## 6. Audit Governance & Sources
- **Data Sources Utilized**: ...
- **Failed Data Sources / Outages**: ...
- **Rate Limit & Throttling Events**: ...
```

### Step 2: Save Local Markdown File
- Target filepath: `outputs/{clean_company_name}_audit_{YYYY-MM-DD}.md`
- Ensure all spaces in the company name are converted to underscores.

### Step 3: Render Local PDF via Pandoc (with Local Script Fallback)
1. Execute the rendering pipeline:
   - Primary: `pandoc outputs/{file}.md -o outputs/{file}.pdf`
   - Automated Fallback: If `pandoc` is not found on the host system, invoke the bundled local Python script:
     `python .agents/skills/report-export/scripts/md_to_pdf.py outputs/{file}.md outputs/{file}.pdf`
2. Verify that the output PDF exists on disk and is non-empty.

### Step 4: Optional Notion Publication
1. Check if `NOTION_API_KEY` and `NOTION_PARENT_PAGE_ID` are configured in the environment.
2. If configured:
   - Transform the markdown report into Notion Block objects.
   - Create a child page under the designated parent page.
   - Retrieve and return the shareable page URL.
3. If not configured:
   - Silently skip cloud publishing and conclude with the local PDF deliverable.

---

## 3. Output Format

```json
{
  "markdown_path": "outputs/acme_audit_2026-09-15.md",
  "pdf_path": "outputs/acme_audit_2026-09-15.pdf",
  "notion_url": null,
  "status": "ready_for_human_review"
}
```
