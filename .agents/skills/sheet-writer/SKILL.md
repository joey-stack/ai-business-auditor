---
name: sheet-writer
description: "Writes audit results, scores, and outreach-ready data to a Google Sheet. Reads the sheet to find the next empty row, then appends one row per prospect. Use after an audit completes and before the daily brief is generated."
---

# Sheet Writer Skill (`sheet-writer`)

This skill synchronizes completed audit results, opportunity scores, and prepared outreach collateral directly to a live Google Sheet ("Outreach Pipeline"), creating a shared interface for tracking and manual outreach execution.

---

## 1. Purpose

Persist high-leverage pipeline output to a live Google Sheet where the human consultant conducts and logs manual outreach.

---

## 2. Input Specification

- **`audit_json`** (`object`, required): Scored audit findings, business metadata, and scores.
- **`client_folder_path`** (`string`, required): Local absolute or relative path to `outputs/clients/<company-slug>/`.
- **`enrichment_data`** (`object`, optional): LinkedIn decision-maker details and `approach_strategy` hooks.

---

## 3. Step-by-Step Execution Process

1. **Read Configuration**:
   - Read the target Spreadsheet ID and sheet name from [`.agents/rules/sheet-config.md`](file:///c:/Users/user/Desktop/AI%20BUSINESS%20AUDITOR/.agents/rules/sheet-config.md).
   - If the Sheet ID is not yet configured, log a notice and gracefully skip spreadsheet synchronization.

2. **Inspect Sheet & Locate Insertion Point**:
   - Call the Sheets MCP `read-values` tool to inspect the "Outreach Pipeline" sheet and locate the next available empty row.

3. **Compose Data Row (Columns A–K Contiguous Block)**:
   - Compose the single values array for columns A through K:
     - **Column A**: Business Name
     - **Column B**: Location (City, State/Country)
     - **Column C**: Opportunity Score (or Combined Score)
     - **Column D**: Tier (`Tier A` | `Tier B` | `Tier C` | `Tier D`)
     - **Column E**: Audit PDF Link (local path or shareable Drive link)
     - **Column F**: Video Walkthrough Link (path to `walkthrough.mp4` or blank)
     - **Column G**: Call Script Link (path to `call_script.md`)
     - **Column H**: Suggested Opening Line (from `approach_strategy.opening_line`)
     - **Column I**: Contact Name (verified decision-maker name from LinkedIn, or blank)
     - **Column J**: Contact Title (verified title, or blank)
     - **Column K**: LinkedIn Profile URL (or `""` if null / none found)

4. **Append Row (Single Contiguous Write)**:
   - Call the Sheets MCP `append-rows` tool targeting range **`"Outreach Pipeline!A:K"`**.
   - If the LinkedIn URL is null, leave Column K blank (as an empty string `""` within the `A:K` array).
   - Return confirmation including the appended row index.

---

## 4. Hard Constraints & Resilience

- **Single Contiguous Write (A–K Only)**: All agent writes are strictly confined to columns A through K in a single atomic call.
- **NEVER Include L–R in Any Write Range**: Columns L–R are exclusively reserved for human sales management (Outreach Status, Touch 1 Date, Touch 2 Date, Touch 3 Date, Last Touch Result, Next Action, Notes). Agents must never include columns L–R in any write, append, or update call under any circumstance.
- **Append Only**: Never overwrite existing data rows in columns A–K. Always append below existing entries.
- **Non-Blocking Fault Tolerance**: If the Google Sheets MCP server is unreachable, returns an authorization error, or is offline, log the event to `outputs/daily_brief.md` and continue cleanly. A spreadsheet error must never crash or block the local audit pipeline.
