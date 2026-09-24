#!/usr/bin/env python3
"""
Generate Flagship Client-Facing PDF Lead Magnets and Organize Per-Post Dedicated Folders.
1. Lead Magnet #1: "The 10-Second After-Hours Dispatch Blueprint" (For Video #1 Bio Link)
2. Lead Magnet #2: "The 4-Pillar Systems Diagnostic Checklist" (For Video #2 'AUDIT' Comment)
3. Lead Magnet #3: "The Weekend Protection Blueprint" (For Video #3 Offer)
4. Reorganizes TikTok and LinkedIn content into dedicated per-post directories:
   outputs/tiktok_content/post_01_..., post_02_..., etc.
   outputs/linkedin_content/post_01_..., post_02_..., etc.
"""
import os
import sys
import shutil
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from playwright.sync_api import sync_playwright

OUTPUT_DIR = Path("outputs")
TIKTOK_DIR = OUTPUT_DIR / "tiktok_content"
LINKEDIN_DIR = OUTPUT_DIR / "linkedin_content"

LEAD_MAGNETS_DIR = OUTPUT_DIR / "lead_magnets"
LEAD_MAGNETS_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------
# 1. HTML Templates for Lead Magnets
# ----------------------------------------------------------------------

def get_base_css():
    return """
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700;800&display=swap');
    * { box-sizing: border-box; margin: 0; padding: 0; }
    @page {
        size: letter;
        margin: 10mm 12mm 10mm 12mm;
    }
    body {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
        color: #0F172A;
        background: #FFFFFF;
        line-height: 1.45;
        font-size: 10pt;
    }
    .header-bar {
        border-bottom: 2px solid #0F172A;
        padding-bottom: 12px;
        margin-bottom: 16px;
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
    }
    .brand-title {
        font-size: 16pt;
        font-weight: 900;
        letter-spacing: -0.02em;
        color: #0F172A;
    }
    .brand-sub {
        font-size: 8.5pt;
        font-weight: 700;
        color: #0284C7;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .badge {
        background: #0F172A;
        color: #FFFFFF;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 7.5pt;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    .hero-box {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: #FFFFFF;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 18px;
    }
    .hero-box h1 {
        font-size: 19pt;
        font-weight: 900;
        line-height: 1.2;
        letter-spacing: -0.02em;
        margin-bottom: 6px;
    }
    .hero-box p {
        font-size: 10pt;
        color: #94A3B8;
        font-weight: 500;
    }
    .card {
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 14px;
        background: #F8FAFC;
    }
    .card-title {
        font-size: 11pt;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .step-badge {
        background: #0284C7;
        color: #FFF;
        font-size: 8pt;
        font-weight: 900;
        padding: 2px 8px;
        border-radius: 4px;
    }
    .flow-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 12px;
        margin-bottom: 16px;
    }
    .flow-card {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }
    .flow-icon {
        font-size: 20pt;
        margin-bottom: 6px;
    }
    .flow-title {
        font-weight: 800;
        font-size: 9.5pt;
        color: #0F172A;
    }
    .flow-desc {
        font-size: 8pt;
        color: #64748B;
        margin-top: 4px;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        font-size: 8.5pt;
        margin: 10px 0;
    }
    th {
        background: #0F172A;
        color: #FFF;
        padding: 8px 10px;
        text-align: left;
        font-weight: 700;
    }
    td {
        padding: 7px 10px;
        border-bottom: 1px solid #E2E8F0;
    }
    tr:nth-child(even) {
        background: #F1F5F9;
    }
    .cta-footer {
        background: #0284C7;
        color: #FFF;
        border-radius: 10px;
        padding: 14px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 18px;
    }
    .cta-footer h3 {
        font-size: 11pt;
        font-weight: 800;
    }
    .cta-footer p {
        font-size: 8.5pt;
        color: #E0F2FE;
    }
    .cta-btn {
        background: #FFF;
        color: #0F172A;
        padding: 8px 16px;
        border-radius: 6px;
        font-weight: 800;
        font-size: 9pt;
        text-decoration: none;
        white-space: nowrap;
    }
    .checklist-item {
        display: flex;
        align-items: flex-start;
        gap: 8px;
        margin-bottom: 7px;
        font-size: 8.5pt;
    }
    .checkbox-box {
        width: 14px;
        height: 14px;
        border: 1.5px solid #0284C7;
        border-radius: 3px;
        flex-shrink: 0;
        margin-top: 2px;
    }
    """

def html_10s_dispatch_blueprint():
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>The 10-Second After-Hours Dispatch Architecture</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap');
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    @page {{
        size: letter;
        margin: 7mm 9mm 7mm 9mm;
    }}
    body {{
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
        color: #0F172A;
        background: #FFFFFF;
        line-height: 1.3;
        font-size: 8pt;
    }}
    .header-bar {{
        border-bottom: 1.5px solid #0F172A;
        padding-bottom: 6px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
    }}
    .brand-title {{
        font-size: 13pt;
        font-weight: 900;
        letter-spacing: -0.02em;
        color: #0F172A;
        line-height: 1;
    }}
    .brand-sub {{
        font-size: 7pt;
        font-weight: 700;
        color: #0284C7;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 2px;
    }}
    .badge {{
        background: #0F172A;
        color: #FFFFFF;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 6.5pt;
        font-weight: 800;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }}
    .hero-box {{
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: #FFFFFF;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
    }}
    .hero-box h1 {{
        font-size: 13pt;
        font-weight: 900;
        line-height: 1.15;
        letter-spacing: -0.02em;
        margin-bottom: 3px;
    }}
    .hero-box p {{
        font-size: 7.5pt;
        color: #94A3B8;
        font-weight: 500;
    }}
    .card {{
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 7px 10px;
        margin-bottom: 7px;
        background: #F8FAFC;
    }}
    .card-title {{
        font-size: 8.5pt;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    .step-badge {{
        background: #0284C7;
        color: #FFF;
        font-size: 6.5pt;
        font-weight: 900;
        padding: 1px 5px;
        border-radius: 3px;
    }}
    .flow-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 8px;
        margin-bottom: 7px;
    }}
    .flow-card {{
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 6px;
        padding: 6px 8px;
        text-align: center;
    }}
    .flow-icon {{
        font-size: 13pt;
        margin-bottom: 2px;
    }}
    .flow-title {{
        font-weight: 800;
        font-size: 7.5pt;
        color: #0F172A;
    }}
    .flow-desc {{
        font-size: 6.8pt;
        color: #64748B;
        margin-top: 2px;
        line-height: 1.25;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 7.2pt;
        margin: 3px 0;
    }}
    th {{
        background: #0F172A;
        color: #FFF;
        padding: 4px 6px;
        text-align: left;
        font-weight: 700;
        font-size: 7pt;
    }}
    td {{
        padding: 4px 6px;
        border-bottom: 1px solid #E2E8F0;
        vertical-align: top;
    }}
    tr:nth-child(even) {{
        background: #F1F5F9;
    }}
    .cta-footer {{
        background: #0284C7;
        color: #FFF;
        border-radius: 6px;
        padding: 8px 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 6px;
    }}
    .cta-footer h3 {{
        font-size: 8.5pt;
        font-weight: 800;
    }}
    .cta-footer p {{
        font-size: 7pt;
        color: #E0F2FE;
    }}
    .cta-btn {{
        background: #FFF;
        color: #0F172A;
        padding: 5px 10px;
        border-radius: 4px;
        font-weight: 800;
        font-size: 7.2pt;
        text-decoration: none;
        white-space: nowrap;
    }}
</style>
</head>
<body>
    <div class="header-bar">
        <div>
            <div class="brand-title">JOEL ADAWAH SANI</div>
            <div class="brand-sub">Principal Business Systems Consultant • Operational SOP Series</div>
        </div>
        <div class="badge">OFFICIAL WORKFLOW BLUEPRINT</div>
    </div>

    <div class="hero-box">
        <h1>The 10-Second After-Hours Dispatch Architecture</h1>
        <p>Standard Operating Procedure & Automation Logic for $1M–$10M Plumbing, HVAC & Electrical Fleets</p>
    </div>

    <div class="card" style="border-left: 3px solid #EF4444; background: #FEF2F2; padding: 6px 10px; margin-bottom: 6px;">
        <div class="card-title" style="color: #991B1B; font-size: 8pt; margin-bottom: 2px;">
            ⚠️ The $14,500/Month Emergency Latency Gap
        </div>
        <p style="font-size: 7.2pt; color: #7F1D1D; line-height: 1.3;">
            In our trade fleet audits, <strong>17.4% of high-intent calls arrive after 5:00 PM or weekends</strong>. When dropped to voicemail, 82% immediately dial competitor #2. In emergency trades ($2,500–$3,500 ticket size), 4 missed calls = <strong>$14,500/mo uncaptured margin ($174,000/year)</strong>.
        </p>
    </div>

    <div class="flow-grid">
        <div class="flow-card" style="border-top: 2.5px solid #0284C7;">
            <div class="flow-icon">📞</div>
            <div class="flow-title">1. Instant 8s Trigger</div>
            <div class="flow-desc">Inbound call drops ➔ Webhook detects unanswered call ➔ 2-way SMS fires in &lt;10s.</div>
        </div>
        <div class="flow-card" style="border-top: 2.5px solid #F59E0B;">
            <div class="flow-icon">🔍</div>
            <div class="flow-title">2. Interactive Triage</div>
            <div class="flow-desc">Emergency (Shutoff steps + on-call tech alert) vs. Routine (Auto-queued Mon 8:00 AM).</div>
        </div>
        <div class="flow-card" style="border-top: 2.5px solid #10B981;">
            <div class="flow-icon">💰</div>
            <div class="flow-title">3. Zero Headcount</div>
            <div class="flow-desc">$2,500–$3,500 ticket captured in CRM without $3,000/mo answering service payroll.</div>
        </div>
    </div>

    <div class="card">
        <div class="card-title"><span class="step-badge">STEP 1</span> The Outbound SMS Interceptor Copy & Logic</div>
        <div style="background: #E2E8F0; padding: 5px 8px; border-radius: 4px; font-family: 'JetBrains Mono', monospace; font-size: 6.8pt; color: #0F172A; margin: 3px 0;">
            "Hi, this is [Company Name] Emergency Dispatch. We see you just called. Are you experiencing an active water leak, gas smell, or safety hazard? Reply YES for immediate emergency technician dispatch, or NO for standard priority service."
        </div>
        <div style="font-size: 6.8pt; color: #475569; display: flex; justify-content: space-between; margin-top: 2px;">
            <span><strong>Webhook Trigger:</strong> Twilio / ServiceTitan missed-call status</span>
            <span><strong>Response Window:</strong> &lt;60s (captures 78% of callers)</span>
        </div>
    </div>

    <div class="card">
        <div class="card-title"><span class="step-badge">STEP 2</span> The Dual-Branch Automated Decision Tree</div>
        <table>
            <thead>
                <tr>
                    <th style="width: 22%;">Customer Reply</th>
                    <th style="width: 48%;">Automated System Action</th>
                    <th style="width: 30%;">Outcome & Business Impact</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Reply: "YES"</strong><br><span style="color:#DC2626; font-weight:700;">(Emergency)</span></td>
                    <td>1. Sends instant shutoff valve safety instructions.<br>2. Pushes high-priority SMS & mobile app alert to on-call tech.<br>3. Holds priority job in CRM dispatch tray.</td>
                    <td><strong>$3,500 Job Won.</strong> Customer stops calling competitors on Google Maps.</td>
                </tr>
                <tr>
                    <td><strong>Reply: "NO"</strong><br><span style="color:#0284C7; font-weight:700;">(Routine Quote)</span></td>
                    <td>1. Sends self-service calendar link for next-day inspection.<br>2. Queues record into Monday 8:00 AM CSR call list.<br>3. Suppresses on-call technician phone notifications.</td>
                    <td><strong>Zero Burnout.</strong> Weekend family dinner protected. Zero overtime payroll waste.</td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="card">
        <div class="card-title"><span class="step-badge">STEP 3</span> Financial Leakage & Recovery Model ($3M Trade Fleet)</div>
        <table>
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Manual Voicemail (Current)</th>
                    <th>10-Second Automated Triage (Optimized)</th>
                    <th>Net Monthly Recovery</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>After-Hours Calls / Mo</strong></td>
                    <td>32 Calls</td>
                    <td>32 Calls</td>
                    <td>—</td>
                </tr>
                <tr>
                    <td><strong>Capture & Booking Rate</strong></td>
                    <td>12.5% (4 Jobs)</td>
                    <td>46.8% (15 Jobs)</td>
                    <td><strong>+11 Additional Jobs</strong></td>
                </tr>
                <tr>
                    <td><strong>Average Emergency Ticket</strong></td>
                    <td>$2,850</td>
                    <td>$3,150 (Choice Quoting)</td>
                    <td>+$300 per ticket</td>
                </tr>
                <tr>
                    <td><strong>Monthly Gross Revenue</strong></td>
                    <td>$11,400</td>
                    <td>$47,250</td>
                    <td><strong style="color: #059669; font-size: 7.8pt;">+$35,850 / month</strong></td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="cta-footer">
        <div>
            <h3>Ready to Install This Architecture In Your Trade Fleet?</h3>
            <p>Schedule a 15-minute diagnostic with Joel Adawah Sani to review your CRM and dispatch setup.</p>
        </div>
        <a class="cta-btn" href="https://calendar.google.com/calendar/appointments/schedules/AcZssZ2r0EoR-9X1C3_Bn2Mu0Xk0FiShErGrUvD8fmPsyK6A9va6kFWeewRqTZxGNX_gE7MzNIuUnNZX">SCHEDULE DISCOVERY CALL ➔</a>
    </div>
</body>
</html>"""

def html_4_pillar_checklist():
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>The 4-Pillar Systems Diagnostic Checklist</title>
<style>{get_base_css()}</style>
</head>
<body>
    <div class="header-bar">
        <div>
            <div class="brand-title">JOEL ADAWAH SANI</div>
            <div class="brand-sub">Principal Business Systems Consultant • Diagnostic Suite</div>
        </div>
        <div class="badge">PROPRIETARY CLIENT CHECKLIST</div>
    </div>

    <div class="hero-box">
        <h1>The 4-Pillar Systems Diagnostic Checklist</h1>
        <p>A 15-Minute Operational Health & Revenue Leakage Self-Audit for Trade Fleet Owners ($1M–$10M)</p>
    </div>

    <p style="font-size: 8.5pt; color: #475569; margin-bottom: 14px;">
        Use this checklist to score your service enterprise across our 4 core operational pillars. Each pillar contains 5 benchmarks (5 points each, 100 points total). Calculate your score to identify active revenue leakage.
    </p>

    <!-- PILLAR 1 -->
    <div class="card" style="border-left: 4px solid #0284C7;">
        <div class="card-title" style="color: #0284C7;">
            PILLAR 1: Speed-to-Lead & Response Latency (Max: 25 Points)
        </div>
        <div class="checklist-item">
            <div class="checkbox-box"></div>
            <div><strong>Under 60-Second Inbound Response:</strong> Inbound web form and emergency calls receive automated confirmation within 60 seconds (Harvard benchmark).</div>
        </div>
        <div class="checklist-item">
            <div class="checkbox-box"></div>
            <div><strong>Automated After-Hours SMS Triage:</strong> Unassisted calls after 5:00 PM trigger immediate 2-way text to classify active leaks vs routine service.</div>
        </div>
        <div class="checklist-item">
            <div class="checkbox-box"></div>
            <div><strong>Weekend Priority Routing:</strong> Genuine emergencies automatically route to on-call technicians without waking up the founder or paying call center surcharges.</div>
        </div>
        <div class="checklist-item">
            <div class="checkbox-box"></div>
            <div><strong>Google Maps Latency Tracking:</strong> Firm monitors speed-to-lead response decay from local Google Business Profile calls.</div>
        </div>
        <div class="checklist-item">
            <div class="checkbox-box"></div>
            <div><strong>Automated Missed-Call Recapture:</strong> System tracks abandoned calls and re-engages prospective leads within 3 minutes.</div>
        </div>
    </div>

    <!-- PILLAR 2 -->
    <div class="card" style="border-left: 4px solid #10B981;">
        <div class="card-title" style="color: #059669;">
            PILLAR 2: Customer Experience & Support Architecture (Max: 25 Points)
        </div>
        <div class="checklist-item">
            <div class="checkbox-box"></div>
            <div><strong>Automated Review Generation:</strong> Invoices closed in CRM automatically trigger SMS review requests within 15 minutes of job completion.</div>
        </div>
        <div class="checklist-item">
            <div class="checkbox-box"></div>
            <div><strong>Review Velocity Consistency:</strong> Firm generates 15–25 verified 5-star reviews every 30 days to dominate Google Map Pack rank.</div>
        </div>
        <div class="checklist-item">
            <div class="checkbox-box"></div>
            <div><strong>Live Dispatch Notifications:</strong> Customers receive 'Technician En Route' tracking link with photo, ETA, and technician bio.</div>
        </div>
        <div class="checklist-item">
            <div class="checkbox-box"></div>
            <div><strong>Self-Service Scheduling Portal:</strong> Repeat customers can book routine maintenance and annual tune-ups directly online.</div>
        </div>
        <div class="checklist-item">
            <div class="checkbox-box"></div>
            <div><strong>Post-Service Quality Pulse:</strong> 48-hour automated check-in SMS ensures complete customer satisfaction before billing dispute occurs.</div>
        </div>
    </div>

    <!-- PILLAR 3 -->
    <div class="card" style="border-left: 4px solid #F59E0B;">
        <div class="card-title" style="color: #D97706;">
            PILLAR 3: Quoting Architecture & Choice Psychology (Max: 25 Points)
        </div>
        <div class="checklist-item">
            <div class="checkbox-box"></div>
            <div><strong>Good-Better-Best Digital Proposals:</strong> Field technicians present 3-tiered options on tablets rather than 1 flat price quote.</div>
        </div>
        <div class="checklist-item">
            <div class="checkbox-box"></div>
            <div><strong>Decoy Effect Integration:</strong> Middle 'Better' tier is engineered to maximize gross margin and capture 65%+ of equipment conversions.</div>
        </div>
        <div class="checklist-item">
            <div class="checkbox-box"></div>
            <div><strong>Integrated 0% Financing:</strong> Monthly payment options are displayed automatically on quotes over $2,500.</div>
        </div>
        <div class="checklist-item">
            <div class="checkbox-box"></div>
            <div><strong>Automated Quote Follow-Up:</strong> Unsigned estimates trigger automated 24-hour and 72-hour SMS reminder sequences.</div>
        </div>
        <div class="checklist-item">
            <div class="checkbox-box"></div>
            <div><strong>Digital Signature & Deposit:</strong> Customers can authorize quotes and pay initial deposits instantly on mobile.</div>
        </div>
    </div>

    <!-- PILLAR 4 -->
    <div class="card" style="border-left: 4px solid #8B5CF6;">
        <div class="card-title" style="color: #7C3AED;">
            PILLAR 4: Internal Operations & Infrastructure (Max: 25 Points)
        </div>
        <div class="checklist-item">
            <div class="checkbox-box"></div>
            <div><strong>Dual-Trade Cross-Sell Automation:</strong> CRM detects single-trade clients and triggers seasonal cross-sell opportunities (e.g. water heater checks).</div>
        </div>
        <div class="checklist-item">
            <div class="checkbox-box"></div>
            <div><strong>Sub-2.5s Mobile Page Speed:</strong> Website loads in under 2.5s on 4G mobile, preventing the 52% bounce penalty.</div>
        </div>
        <div class="checklist-item">
            <div class="checkbox-box"></div>
            <div><strong>Authenticated Email Infrastructure:</strong> SPF, DKIM, and DMARC records are configured to prevent commercial quotes landing in SPAM.</div>
        </div>
        <div class="checklist-item">
            <div class="checkbox-box"></div>
            <div><strong>Unified Dispatch & Inventory:</strong> Truck stock syncs with job invoices to eliminate second-trip parts runs.</div>
        </div>
        <div class="checklist-item">
            <div class="checkbox-box"></div>
            <div><strong>Deloitte Effort vs. Impact Prioritization:</strong> Leadership reviews monthly roadmap matrix ranking operational fixes by gross value recovery.</div>
        </div>
    </div>

    <!-- SCORING TABLE -->
    <div class="card">
        <div class="card-title">📊 Self-Audit Score Interpretation</div>
        <table>
            <thead>
                <tr>
                    <th>Score Range</th>
                    <th>Classification</th>
                    <th>Operational Reality & Recommended Action</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>85–100 Points</strong></td>
                    <td><span style="color: #059669; font-weight: 800;">Tier 1: Industry Leader</span></td>
                    <td>High-efficiency operations. Minimal revenue leakage. Scale ad spend with confidence.</td>
                </tr>
                <tr>
                    <td><strong>65–84 Points</strong></td>
                    <td><span style="color: #D97706; font-weight: 800;">Tier 2: Moderate Leakage</span></td>
                    <td>Leaking $8,000–$15,000/mo in after-hours abandonment and flat-pricing surrender.</td>
                </tr>
                <tr>
                    <td><strong>Under 65 Points</strong></td>
                    <td><span style="color: #DC2626; font-weight: 800;">Tier 3: Severe Hemorrhage</span></td>
                    <td>Surrendering $25,000+/mo to competitors. Immediate 4-pillar systems overhaul required.</td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="cta-footer">
        <div>
            <h3>Want an Institutional Review of Your Checklist Score?</h3>
            <p>Joel Adawah Sani conducts deep-dive 4-pillar audits for select $1M–$10M trade contractors.</p>
        </div>
        <a class="cta-btn" href="https://calendar.google.com/calendar/appointments/schedules/AcZssZ2r0EoR-9X1C3_Bn2Mu0Xk0FiShErGrUvD8fmPsyK6A9va6kFWeewRqTZxGNX_gE7MzNIuUnNZX">BOOK AUDIT REVIEW ➔</a>
    </div>
</body>
</html>
"""

def html_weekend_protection_blueprint():
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>The Weekend Protection Blueprint</title>
<style>{get_base_css()}</style>
</head>
<body>
    <div class="header-bar">
        <div>
            <div class="brand-title">JOEL ADAWAH SANI</div>
            <div class="brand-sub">Principal Business Systems Consultant • Contractor Lifestyle & Systems Series</div>
        </div>
        <div class="badge">EXECUTIVE BLUEPRINT</div>
    </div>

    <div class="hero-box">
        <h1>The Weekend Protection Blueprint</h1>
        <p>How Trade Contractors Stop Emergency Calls from Ruining Family Dinner While Capturing $2,500+ Tickets</p>
    </div>

    <div class="card" style="border-left: 4px solid #F59E0B; background: #FFFBEB;">
        <div class="card-title" style="color: #B45309;">
            🍲 The Saturday Dinner Trap
        </div>
        <p style="font-size: 8.5pt; color: #92400E;">
            Most trade contractors face a false choice: either answer every phone call during weekend family dinner, or miss out on high-margin emergency revenue. The solution is <strong>automated triage architecture</strong> that filters noise from true emergencies without adding payroll.
        </p>
    </div>

    <div class="flow-grid">
        <div class="flow-card" style="border-top: 3px solid #0284C7;">
            <div class="flow-icon">📱</div>
            <div class="flow-title">1. SMS Guardrail</div>
            <div class="flow-desc">Unanswered weekend calls receive immediate 2-way text to separate emergencies from routine requests.</div>
        </div>
        <div class="flow-card" style="border-top: 3px solid #10B981;">
            <div class="flow-icon">⚡</div>
            <div class="flow-title">2. True Emergency Dispatch</div>
            <div class="flow-desc">Active leaks & safety hazards trigger shutoff steps and alert the on-call technician directly.</div>
        </div>
        <div class="flow-card" style="border-top: 3px solid #6366F1;">
            <div class="flow-icon">📅</div>
            <div class="flow-title">3. Monday Auto-Queue</div>
            <div class="flow-desc">Routine inquiries are booked for Monday 8:00 AM. Zero distraction during your weekend dinner.</div>
        </div>
    </div>

    <div class="card">
        <div class="card-title">🛠️ The Weekend Protocol Comparison</div>
        <table>
            <thead>
                <tr>
                    <th>Workflow Stage</th>
                    <th>Without Systems Automation</th>
                    <th>With Weekend Protection Stack</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Saturday 7:30 PM Call</strong></td>
                    <td>Owner answers during family dinner. Spends 15 mins on non-urgent inquiry.</td>
                    <td>Automated SMS confirms receipt in 8s. Client texts "Need routine service".</td>
                </tr>
                <tr>
                    <td><strong>Scheduling Action</strong></td>
                    <td>Owner jots note on napkin; risks forgetting to schedule on Monday.</td>
                    <td>System auto-queues record for Monday 8:00 AM CSR call list.</td>
                </tr>
                <tr>
                    <td><strong>Emergency Handling</strong></td>
                    <td>Owner scrambles to call 3 technicians to find someone on call.</td>
                    <td>Emergency webhook routes ticket directly to on-call tech's mobile app.</td>
                </tr>
                <tr>
                    <td><strong>Monthly Cost</strong></td>
                    <td>$3,000/mo answering service or extreme founder burnout.</td>
                    <td><strong>$0 added headcount.</strong> Clean, automated dispatch software.</td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="cta-footer">
        <div>
            <h3>Reclaim Your Weekends Without Forfeiting High-Margin Revenue</h3>
            <p>Schedule an operational walkthrough with Joel Adawah Sani to install this stack.</p>
        </div>
        <a class="cta-btn" href="https://calendar.google.com/calendar/appointments/schedules/AcZssZ2r0EoR-9X1C3_Bn2Mu0Xk0FiShErGrUvD8fmPsyK6A9va6kFWeewRqTZxGNX_gE7MzNIuUnNZX">SCHEDULE A 15-MIN WALKTHROUGH ➔</a>
    </div>
</body>
</html>
"""

# ----------------------------------------------------------------------
# 2. Render PDFs via Playwright
# ----------------------------------------------------------------------

def render_pdf(html_content: str, output_pdf_path: Path):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            executable_path=r"C:\Users\user\AppData\Local\ms-playwright\chromium_headless_shell-1234\chrome-headless-shell-win64\chrome-headless-shell.exe"
        )
        page = browser.new_page()
        page.set_content(html_content, wait_until="networkidle")
        output_pdf_path.parent.mkdir(parents=True, exist_ok=True)
        page.pdf(
            path=str(output_pdf_path),
            format="Letter",
            print_background=True,
            margin={"top": "10mm", "bottom": "10mm", "left": "12mm", "right": "12mm"}
        )
        browser.close()
    print(f"Generated PDF: {output_pdf_path}")

# ----------------------------------------------------------------------
# 3. Organize Per-Post Dedicated Folders for TikTok & LinkedIn
# ----------------------------------------------------------------------

def organize_tiktok_posts():
    print("\n--- Organizing TikTok Posts into Dedicated Folders ---")
    
    # Map post numbers to names
    tiktok_map = {
        1: {
            "folder": "post_01_speed_to_lead_burst_pipe",
            "script": "video_01_speed-to-lead_and_response_latency.md",
            "voiceover": "video_01_voiceover_clean.mp3",
            "video": "video_01_burst_pipe_remotion.mp4",
            "lead_magnet": "10_second_dispatch_workflow_blueprint.pdf",
            "stills_prefix": "video_01"
        },
        2: {
            "folder": "post_02_sixty_second_rule_google_maps",
            "script": "video_02_speed-to-lead_and_response_latency.md",
            "voiceover": "video_02_voiceover.mp3",
            "video": "video_02_sixty_second_rule_remotion.mp4",
            "lead_magnet": "4_pillar_systems_diagnostic_checklist.pdf",
            "stills_prefix": "video_02"
        },
        3: {
            "folder": "post_03_protect_weekend_dinner",
            "script": "video_03_speed-to-lead_and_response_latency.md",
            "voiceover": "video_03_voiceover.mp3",
            "video": "video_03_protect_weekend_remotion.mp4",
            "lead_magnet": "weekend_protection_blueprint.pdf",
            "stills_prefix": "video_03"
        }
    }

    from generate_tiktok_engine import VIDEOS
    for vid in VIDEOS:
        idx = vid["num"]
        clean_name = re.sub(r'[^a-zA-Z0-9_]+', '_', vid["text_hook"].lower()).strip('_')
        folder_name = f"post_{idx:02d}_{clean_name}"
        post_folder = TIKTOK_DIR / folder_name
        post_folder.mkdir(parents=True, exist_ok=True)
        
        # Script copy
        matches = list((TIKTOK_DIR / "scripts").glob(f"video_{idx:02d}_*.md"))
        script_src = matches[0] if matches else None

        if script_src.exists():
            shutil.copyfile(script_src, post_folder / "script.md")

        # If it's posts 1-3, copy renders, voiceovers, stills, and lead magnets
        if idx in tiktok_map:
            cfg = tiktok_map[idx]
            
            # Copy voiceover
            vo_src = TIKTOK_DIR / "rendered" / cfg["voiceover"]
            if vo_src.exists():
                shutil.copyfile(vo_src, post_folder / "voiceover.mp3")
            
            # Copy video
            vid_src = TIKTOK_DIR / "rendered" / cfg["video"]
            if vid_src.exists():
                shutil.copyfile(vid_src, post_folder / "video.mp4")
            
            # Copy lead magnet PDF
            lm_src = LEAD_MAGNETS_DIR / cfg["lead_magnet"]
            if lm_src.exists():
                shutil.copyfile(lm_src, post_folder / cfg["lead_magnet"])

            # Copy stills
            stills_dest = post_folder / "stills"
            stills_dest.mkdir(parents=True, exist_ok=True)
            for still in (TIKTOK_DIR / "rendered" / "stills").glob(f"{cfg['stills_prefix']}*.png"):
                shutil.copyfile(still, stills_dest / still.name)

        print(f"Prepared TikTok folder: {folder_name}")

def organize_linkedin_posts():
    print("\n--- Organizing LinkedIn Posts into Dedicated Folders ---")
    sys.path.insert(0, ".")
    from generate_60_day_content import build_data
    data = build_data()
    posts = data[7:] # 25 posts

    for idx, p in enumerate(posts, 1):
        topic_slug = re.sub(r'[^a-zA-Z0-9_]+', '_', p[3].lower()).strip('_')
        folder_name = f"post_{idx:02d}_{topic_slug}"
        post_folder = LINKEDIN_DIR / folder_name
        post_folder.mkdir(parents=True, exist_ok=True)

        # Write individual post_copy.md
        post_md = f"""# LinkedIn Post #{idx:02d}

- **Scheduled Date & Time**: {p[1]}
- **Format**: {p[2]}
- **Content Pillar**: {p[3]}
- **Status**: {p[4]}
- **Single-Line Hook (<58 chars)**: `{p[5]}` (Length: {len(p[5])} chars)
- **Attached Asset**: `{p[7]}`

---

## Ready-to-Paste Post Copy

```text
{p[6]}
```

---

## Publishing Instructions
{p[9]}
"""
        with open(post_folder / "post_copy.md", "w", encoding="utf-8") as f:
            f.write(post_md)

        # If post has attached carousel PDF, copy it into post folder
        if "carousel" in p[7].lower():
            # find carousel path
            match = re.search(r'(outputs/linkedin_content/carousels/[\w\-_]+\.pdf)', p[7])
            if match:
                car_path = Path(match.group(1))
                if car_path.exists():
                    shutil.copyfile(car_path, post_folder / car_path.name)

        # Also copy relevant lead magnet PDF for easy sharing in DMs / comments
        txt_lower = (p[5] + " " + p[6]).lower()
        if "lead" in txt_lower or "pipe" in txt_lower or "emergency" in txt_lower or "dispatch" in txt_lower:
            shutil.copyfile(LEAD_MAGNETS_DIR / "10_second_dispatch_workflow_blueprint.pdf", post_folder / "10_second_dispatch_workflow_blueprint.pdf")
        if "checklist" in txt_lower or "audit" in txt_lower or "pillar" in txt_lower or "diagnostic" in txt_lower:
            shutil.copyfile(LEAD_MAGNETS_DIR / "4_pillar_systems_diagnostic_checklist.pdf", post_folder / "4_pillar_systems_diagnostic_checklist.pdf")
        if "weekend" in txt_lower or "dinner" in txt_lower or "burnout" in txt_lower or "founder" in txt_lower:
            shutil.copyfile(LEAD_MAGNETS_DIR / "weekend_protection_blueprint.pdf", post_folder / "weekend_protection_blueprint.pdf")

        print(f"Prepared LinkedIn folder: {folder_name}")

def main():
    # 1. Render Lead Magnets
    print("--- Rendering Client-Facing PDF Lead Magnets ---")
    lm1_path = LEAD_MAGNETS_DIR / "10_second_dispatch_workflow_blueprint.pdf"
    render_pdf(html_10s_dispatch_blueprint(), lm1_path)
    print(f"Rendered Lead magnet 1: {lm1_path}")

    lm2_path = LEAD_MAGNETS_DIR / "4_pillar_systems_diagnostic_checklist.pdf"
    render_pdf(html_4_pillar_checklist(), lm2_path)
    print(f"Rendered Lead magnet 2: {lm2_path}")

    lm3_path = LEAD_MAGNETS_DIR / "weekend_protection_blueprint.pdf"
    render_pdf(html_weekend_protection_blueprint(), lm3_path)
    print(f"Rendered Lead magnet 3: {lm3_path}")

    # 2. Organize Folders
    organize_tiktok_posts()
    organize_linkedin_posts()

    print("\n[SUCCESS] ALL LEAD MAGNETS GENERATED AND POST FOLDERS ORGANIZED!")

if __name__ == "__main__":
    main()
