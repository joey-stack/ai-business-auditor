# Ideal Customer Profile (ICP) Definition

This document defines the qualifying criteria for high-probability target accounts for AI business audits, process automation, and managed optimization engagements. It is directly evaluated during prospect scoring.

---

## 1. Target Industries
- High-ticket local service contractors (Commercial/Residential Plumbing, HVAC, Roofing, Electrical).
- Professional services & advisory (Independent Asset Handlers, Wealth Managers, Property Developers, Boutique Law Firms).
- Multi-chair private healthcare and dental practices.

---

## 2. Company Scale
- **Employee Headcount**: 5 to 50 employees (sweet spot: 10–35).
- **Annual Revenue Range**: $1,000,000 to $10,000,000 USD (or equivalent local turnover).

---

## 3. Decision-Maker Profile
- **Target Job Titles**: Owner, Founder, CEO, Managing Director, Operations Director, General Manager.
- **Engagement Persona**: Owner-operator or senior operational stakeholder with direct purchasing and workflow transformation authority.

---

## 4. Geography
- Tier-1 and Tier-2 Metropolitan Markets (e.g., Austin, TX; London, UK; Manchester, UK; Abuja, Nigeria; Lagos, Nigeria).

---

## 5. Must-Have Attributes (Mandatory Pass)
Every qualified prospect must satisfy **all** of the following:
1. **Verified Physical or Registered Trading Location**: Has a verifiable physical premises or listed Google Maps service location.
2. **Active Customer Review History**: Minimum 10+ public customer reviews on Google Maps.
3. **Dedicated Business Phone Line**: A callable telephone line listed publicly for incoming inquiries.

*If any Must-Have Attribute is missing, `icp_fit_score` is automatically set to **0**.*

---

## 6. Immediate Disqualifiers (Automatic Rejection)
Any prospect matching any of the following conditions is disqualified (`icp_fit_score = 0`):
1. **National/Global Franchises**: Brand operations bound by rigid corporate IT stacks (e.g., Roto-Rooter corporate, franchise fast casual).
2. **Dedicated In-House Engineering/Marketing Teams**: Companies with in-house CMOs, VP Engineering, or internal software development staff.
3. **Dormant or Inactive Entities**: Listings flagged as permanently closed or without active reviews in the last 12 months.
