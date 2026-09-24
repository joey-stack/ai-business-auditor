# User Profile Configuration

This document stores the consultant's own professional identity and LinkedIn profile information. It is used by the `profile-self-audit` skill and `/audit-my-profile` workflow to evaluate profile alignment against the target Ideal Customer Profile (ICP).

---

## 1. LinkedIn Profile Settings

- **`linkedin_url`**: `https://www.linkedin.com/in/joel-adawah-sani`
- **`full_name`**: "Joel Adawah Sani"
- **`current_title`**: "AI Business Auditor & Operational Consultant"
- **`target_service`**: "AI Business Audits, Operational Workflow Automation & Consulting"

---

## 2. Usage Instructions

To audit your own LinkedIn profile:
1. Update `linkedin_url` above with your full public LinkedIn profile URL (e.g., `https://www.linkedin.com/in/your-handle`).
2. Run `/audit-my-profile` in the chat or orchestrator.
3. The system will retrieve your current headline, About section, experience, skills, and recent posts, scoring all 9 components against `.agents/rules/icp-definition.md`.
