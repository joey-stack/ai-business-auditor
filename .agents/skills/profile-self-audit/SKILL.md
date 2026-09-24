---
name: profile-self-audit
description: "Audits the user's OWN LinkedIn profile against their ICP definition. Scores nine components, identifies gaps, and generates copy-paste rewrites for the headline, About section, and skills. READ-ONLY: never edits the profile."
---

# LinkedIn Profile Self-Audit Skill (`profile-self-audit`)

This skill audits the consultant's own LinkedIn profile against the Ideal Customer Profile (ICP) defined in `.agents/rules/icp-definition.md`. It systematically scores nine essential profile components, identifies positioning and discoverability gaps, and produces copy-paste rewrites to optimize the profile for high-ticket client acquisition.

---

## 1. Purpose

Score the user's personal LinkedIn profile through the eyes of an ICP decision-maker (e.g., HVAC/Plumbing owner-operators, asset managers, healthcare practice principals) and produce a high-impact, prioritized improvement roadmap.

---

## 2. Input Specification

- **`my_linkedin_url`** (`string`, required): The user's public LinkedIn profile URL (sourced from `.agents/rules/user-profile.md`).
- **`icp_definition`** (`object` or path, required): Target criteria from `.agents/rules/icp-definition.md`.
- **`competitor_linkedin_urls`** (`string[]`, optional): Benchmark profiles from previous competitor analyses.

---

## 3. Step-by-Step Execution Process

### Step 1: Read Profile Data
1. Retrieve the target profile URL from `.agents/rules/user-profile.md`.
2. Invoke the LinkedIn MCP tool `get_person_profile` using `profile_url` with `sections=["posts"]` (or `get_my_profile` if authenticated locally).
3. Extract:
   - Full Name & Current Headline
   - About / Summary narrative
   - Featured items (links, media, documents)
   - Experience entries (bullet points, metrics, skills tagged)
   - Skills list & pinned top skills
   - Custom URL vanity handle
   - Photo & Background Banner status
   - Recommendations count & recency
   - Recent activity & posts (last 30 days)

### Step 2: Extract Target Keywords from ICP
Read `.agents/rules/icp-definition.md` and extract the core alignment vocabulary:
- **Target Industries**: High-ticket local service contractors (Commercial/Residential Plumbing, HVAC, Roofing, Electrical), Professional services & advisory (Independent Asset Handlers, Wealth Managers, Property Developers), Multi-chair private practices.
- **Decision-Maker Search Queries**: Terms used by Owners, Founders, CEOs, Managing Directors, and Operations Directors looking for workflow automation, AI diagnostics, or conversion rate optimization.
- **Core Problems Solved**: Lead leakage, emergency triage failure, slow page speeds, manual quoting friction, missing review collection pipelines, software silos.

### Step 3: Score the Nine Components
Assign `pass`, `needs-work`, or `fail` to each component with a single-line reasoning rationale:

1. **Headline**:
   - `PASS`: Contains target role + 2–3 role-specific keywords + one quantifiable value statement. Under 220 characters. Leads with the primary searched keyword.
   - `NEEDS-WORK`: Has keywords but lacks quantifiable outcome statement or exceeds character limits.
   - `FAIL`: Just a generic job title (e.g., "Founder", "Consultant"), no keywords, or no value statement.
2. **About Section**:
   - `PASS`: First 265–275 characters (before "see more") contain a hook stating who you help and the outcome delivered. Full section is 200–400 words, highly skimmable, with clear proof points and CTA.
   - `NEEDS-WORK`: Good content but buries the hook below the fold, or lacks concrete proof metrics.
   - `FAIL`: Opens with "I'm passionate about...", reads like a resume summary, or is blank.
3. **Featured Section**:
   - `PASS`: Contains 3 items aligned with client acquisition (e.g., a lead magnet audit example, a case study with metrics, and a calendar booking link).
   - `NEEDS-WORK`: Contains 1–2 items or outdated media.
   - `FAIL`: Completely empty or contains unrelated personal achievements.
4. **Experience Section**:
   - `PASS`: Role bullets use Action Verb + Context + Quantifiable Metric. 5+ skills tagged per role. Top 3 skills pinned.
   - `NEEDS-WORK`: Clear responsibilities but missing numerical outcomes.
   - `FAIL`: Passive task lists with zero metrics, or outdated entries.
5. **Skills Section**:
   - `PASS`: Top 3 pinned skills match the exact search terms ICP decision-makers use (e.g., "AI Business Automation", "Operational Efficiency", "Workflow Optimization"). 5+ skills total.
   - `NEEDS-WORK`: Relevant skills present but generic items are pinned in top 3.
   - `FAIL`: Generic skills ("Communication", "Leadership") or fewer than 5 skills total.
6. **Custom URL**:
   - `PASS`: Clean vanity handle (`linkedin.com/in/firstnamelastname`).
   - `FAIL`: Default URL with trailing random numbers/characters.
7. **Profile Photo & Banner**:
   - `PASS`: High-resolution, professional headshot where face occupies ~60% of frame. Background banner has clean brand positioning and a clear, subtle call-to-action.
   - `NEEDS-WORK`: Good photo but blank default banner.
   - `FAIL`: Blurry or informal photo, or empty banner.
8. **Recommendations**:
   - `PASS`: At least 2 recommendations from clients, executives, or colleagues validating operational impact.
   - `NEEDS-WORK`: 1 recommendation or older than 24 months.
   - `FAIL`: Zero recommendations.
9. **Recent Activity (Posts)**:
   - `PASS`: At least 1 original post in the last 30 days showcasing domain authority, operational insights, or audit case studies.
   - `NEEDS-WORK`: Only reshared content without original commentary.
   - `FAIL`: Zero activity or posts in 30+ days.

### Step 4: Generate Actionable Rewrites
For any component scoring `needs-work` or `fail`, generate ready-to-use copy:
1. **Headline Rewrites**: Provide 3 formulaic options under 220 characters:
   `[Target Role] | [Skill 1] | [Skill 2] | [Outcome Statement]`
   *(Ensuring the first 60–75 characters contain the primary search term).*
2. **About Section Rewrite**: Provide a full 4-part structure:
   - *Hook (Lines 1–3)*: Who I help and the specific outcome delivered.
   - *Career Narrative (3–5 sentences)*: First-person positioning and operational philosophy.
   - *Focus Areas (4–6 bullets)*: Capabilities mixing role keywords, tools, and outcomes.
   - *Call to Action*: Clear closing instructions on how to connect or request an audit.
3. **Skills Recommendations**: Top 3 pinned skills ranked by ICP search frequency.

### Step 5: Rank Priority Fixes by Impact
Organize recommendations strictly by leverage:
- **HIGH Priority**: Headline, About Section (determines SERP click-through and connection acceptance).
- **MEDIUM Priority**: Skills, Featured Section, Experience Section (validates credibility during profile visits).
- **LOW Priority**: Profile Photo, Banner, Custom URL, Recommendations, Activity cadence.

---

## 4. Hard Constraints & Safety Governance

1. **Strict READ-ONLY Enforcement**:
   - **Never call any write, mutation, or update tool on LinkedIn**.
   - Profile changes are provided solely as text deliverables for the user to copy-paste manually.
2. **Grounded in ICP Definition**:
   - All proposed positioning, hooks, and keywords must directly trace back to `.agents/rules/icp-definition.md`.
3. **Rate Limit & Tool Call Ceiling**:
   - Maximum **3 LinkedIn tool calls per audit invocation**.
4. **Resilient Failure Handling**:
   - If the LinkedIn URL is missing from `.agents/rules/user-profile.md` or the MCP server requires browser authentication, halt immediately and report clear instructions to the user.

---

## 5. Output Format (Markdown Deliverable)

```markdown
# LinkedIn Profile Audit: [User Name]
**Date:** [YYYY-MM-DD]  
**Target Market:** [One-line summary of target ICP]  

## Scorecard

| Component | Score | Reasoning |
| :--- | :---: | :--- |
| **Headline** | [pass / needs-work / fail] | [One-line reasoning] |
| **About Section** | [pass / needs-work / fail] | [One-line reasoning] |
| **Featured Section** | [pass / needs-work / fail] | [One-line reasoning] |
| **Experience** | [pass / needs-work / fail] | [One-line reasoning] |
| **Skills** | [pass / needs-work / fail] | [One-line reasoning] |
| **Custom URL** | [pass / needs-work / fail] | [One-line reasoning] |
| **Photo & Banner** | [pass / needs-work / fail] | [One-line reasoning] |
| **Recommendations** | [pass / needs-work / fail] | [One-line reasoning] |
| **Recent Activity** | [pass / needs-work / fail] | [One-line reasoning] |

---

## Priority Fixes

### 1. [Component Name] — [HIGH / MEDIUM / LOW]
**Current State**: [Observed content]  
**Diagnostic Problem**: [Why it fails against ICP standards]  
**Recommended Rewrite**:
> [Copy-paste text block]

---

## Quick Wins (< 10 Minutes)
- [Action item 1]
- [Action item 2]

## Deeper Work (< 1 Hour)
- [Action item 1]
- [Action item 2]

## Expected Visibility & Conversion Impact
[Strategic assessment of how these revisions improve search indexing, inbound inquiries, and outreach acceptance rates]
```
