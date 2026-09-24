---
name: call-script
description: "Generates a branching call script for a specific prospect based on their audit findings."
---

# /call-script — Prospect Call Script Workflow

This workflow produces a spoken-word, branching phone decision tree tailored to a specific audited prospect.

---

## Trigger
The user types:
```
/call-script "<prospect name>"
```

---

## Steps

### Step 1 — Locate Completed Audit
1. Compute the prospect's client slug using the canonical slug algorithm.
2. Verify the client folder exists at `outputs/clients/{slug}/`.
3. Check for the completed audit Markdown:
   - `outputs/clients/{slug}/audit_*.md`
4. If missing, alert the user:
   > *"No completed audit found for '{prospect name}'. Please run `/audit <website_url>` first."*
   and halt.

### Step 2 — Invoke Call Script Generator
1. Invoke the **`call-script`** skill with the client audit data and approach strategy.
2. Build the structured decision tree covering Opening, Hook, Branch Point, 10 Objections, and Close Paths.

### Step 3 — Save Script Deliverable
1. Save the generated Markdown to `outputs/clients/{slug}/call_script.md`.

### Step 4 — Presentation & Tone Calibration
1. Display the formatted script in chat.
2. Ask: *"Want me to adjust the tone, or is this ready to use?"*
