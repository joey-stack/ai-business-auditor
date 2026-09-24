---
name: audit-my-profile
description: "Runs the profile self-audit and presents a prioritized improvement plan."
---

# /audit-my-profile Workflow

Runs a complete self-audit of the user's personal LinkedIn profile against the project's Ideal Customer Profile (ICP) definition, scores nine core profile components, and provides ready-to-use copy rewrites.

---

## Trigger

User types `/audit-my-profile` or requests a self-audit of their personal LinkedIn profile.

---

## Workflow Steps

### Step 1: Resolve Profile URL
1. Read `.agents/rules/user-profile.md` and check the `linkedin_url` setting.
2. If `linkedin_url` is missing, placeholder, or empty:
   - Prompt the user: *"Please provide your public LinkedIn profile URL (e.g., https://www.linkedin.com/in/yourname) so I can audit your profile."*
   - Once provided, update `.agents/rules/user-profile.md` with the verified URL.

### Step 2: Load Target ICP Criteria
1. Read `.agents/rules/icp-definition.md`.
2. If the ICP definition is absent or unpopulated, prompt the user to define their target industries and decision-maker roles before proceeding.

### Step 3: Invoke Profile Self-Audit Skill
1. Invoke the `profile-self-audit` skill using:
   - `my_linkedin_url` from `user-profile.md`.
   - ICP parameters from `icp-definition.md`.
2. Retrieve profile sections via the LinkedIn MCP server (`get_person_profile` or `get_my_profile`).
3. Evaluate the nine profile components:
   - Headline
   - About section
   - Featured section
   - Experience entries
   - Skills (top 3 pinned)
   - Custom URL
   - Photo & Banner
   - Recommendations
   - Recent Activity / Posts

### Step 4: Present Scorecard & Priority Fixes
Display the diagnostic scorecard in the conversation, highlighting:
1. The 9-component pass / needs-work / fail table.
2. High-priority copy-paste rewrites for the Headline, About section, and pinned Skills.
3. Quick wins (< 10 minutes) and deeper work (< 1 hour).
4. Strategic impact summary on search discoverability and outreach conversion.

### Step 5: Interactive Feedback Checkpoint
Prompt the user:
> *"Would you like me to save this audit deliverable to a file, or refine any specific section (e.g., test alternative headline angles)?"*

### Step 6: Artifact Export (Optional)
If the user confirms or requests a file export:
- Save the complete audit report to:
  `outputs/my_profile_audit_{YYYY-MM-DD}.md`
- Report the saved file path with a clickable link.
