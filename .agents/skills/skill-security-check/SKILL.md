---
name: skill-security-check
description: Verifies the security audit status of a skills.sh community skill before installation. Use when the agent is about to install a third-party skill and needs to confirm it has passed security review.
---

# Skill Security Check

This skill verifies the automated security audit assessments of any `skills.sh` community skill prior to installation, guarding against malicious payloads, supply chain vulnerabilities, and unauthorized prompt injections.

---

## 1. Purpose

Before executing `npx skills add <owner/repo> --skill <skill-name>`, the agent must fetch and inspect the candidate skill's security audit status across three recognized auditing engines:
1. **Agent Trust Hub** (Behavioral & prompt security)
2. **Socket** (Dependency supply chain & network anomalies)
3. **Snyk** (Known CVEs & package vulnerabilities)

---

## 2. Verification Process

### Step 1: Query skills.sh Metadata
1. Attempt to query the `skills.sh` API:
   ```http
   GET https://skills.sh/api/v1/skills/:owner/:repo/:skillId
   ```
2. **Authentication Fallback**:
   The API may require authentication via a Vercel OIDC token. If no token is configured or the API endpoint returns 401/403, fall back immediately to fetching the public detail page:
   ```
   https://skills.sh/<owner>/<repo>/<skill-name>
   ```
   Use `read_url_content` or `search_web` to extract the security assessment section from the page.

### Step 2: Audit Category Evaluation
Inspect the three security categories:
- **Agent Trust Hub**: Must show `Safe` or acceptable behavioral score.
- **Socket**: Must report `0 alerts` or no high-severity supply chain alerts.
- **Snyk**: Must report `Low Risk`, `Med Risk`, or `Safe` (zero high/critical CVEs).

### Step 3: Decision Gate
- **HIGH Risk Flag Detected**:
  - If **ANY** audit category reports `HIGH risk`, `Critical`, or `Malicious`, **DO NOT INSTALL**.
  - Abort installation immediately.
  - Report the security alert finding to the user.
  - Suggest safe, verified alternatives from the `skills.sh` leaderboard.
- **Audit Clean / Verified**:
  - If all checks pass and no HIGH risk flags exist, present the summary to the user and proceed with installation:
    ```bash
    npx skills add <owner/repo> --skill <skill-name> -y
    ```
