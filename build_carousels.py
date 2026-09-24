#!/usr/bin/env python3
"""
LinkedIn Carousel Generator (Pinterest & LinkedIn High-Converting Style).
Renders 1080x1350 (4:5 portrait) multi-page PDF documents.
Each page is a pixel-perfect, elevated slide ready for direct LinkedIn upload.
"""
import os
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import pypdf

# Common CSS tokens for all carousels
CAROUSEL_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800;900&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@600;800&display=swap');

@page {
  size: 1080px 1350px;
  margin: 0;
}

* {
  box-sizing: border-box;
  -webkit-print-color-adjust: exact !important;
  print-color-adjust: exact !important;
}

body {
  margin: 0;
  padding: 0;
  font-family: 'Inter', sans-serif;
  background: #0b132b;
  color: #ffffff;
}

.slide {
  width: 1080px;
  height: 1350px;
  padding: 80px 75px;
  position: relative;
  page-break-after: always;
  background: radial-gradient(circle at 80% 20%, #1e293b 0%, #0f172a 60%, #0b132b 100%);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
}

.slide::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 8px;
  background: linear-gradient(90deg, #2563eb, #38bdf8, #6366f1);
}

/* Slide Header */
.slide-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 24px;
}

.author-badge {
  display: flex;
  align-items: center;
  gap: 14px;
}

.author-avatar {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2563eb, #38bdf8);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 18px;
  color: #ffffff;
}

.author-info {
  display: flex;
  flex-direction: column;
}

.author-name {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-weight: 700;
  font-size: 17px;
  color: #ffffff;
  letter-spacing: -0.01em;
}

.author-title {
  font-size: 13px;
  color: #94a3b8;
}

.slide-counter {
  font-family: 'JetBrains Mono', monospace;
  font-size: 15px;
  font-weight: 700;
  color: #38bdf8;
  background: rgba(56, 189, 248, 0.1);
  border: 1px solid rgba(56, 189, 248, 0.25);
  padding: 6px 14px;
  border-radius: 20px;
}

/* Slide Content */
.slide-body {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 20px 0;
}

.tag-pill {
  display: inline-block;
  align-self: flex-start;
  font-size: 13px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 6px 14px;
  border-radius: 6px;
  margin-bottom: 24px;
}

.tag-blue { background: rgba(37, 99, 235, 0.2); color: #60a5fa; border: 1px solid rgba(96, 165, 250, 0.3); }
.tag-red { background: rgba(220, 38, 38, 0.2); color: #f87171; border: 1px solid rgba(248, 113, 113, 0.3); }
.tag-amber { background: rgba(217, 119, 6, 0.2); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.3); }
.tag-emerald { background: rgba(5, 150, 105, 0.2); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.3); }

h1.slide-title {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 50px;
  font-weight: 900;
  line-height: 1.14;
  letter-spacing: -0.03em;
  margin: 0 0 24px 0;
  color: #ffffff;
}

h1.slide-title span.highlight {
  background: linear-gradient(90deg, #38bdf8, #818cf8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

h2.slide-sub {
  font-size: 24px;
  font-weight: 400;
  line-height: 1.45;
  color: #cbd5e1;
  margin: 0 0 32px 0;
}

/* Feature Cards */
.card-stack {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.feature-card {
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 14px;
  padding: 24px 28px;
  display: flex;
  gap: 20px;
  align-items: flex-start;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.card-number {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 28px;
  font-weight: 800;
  color: #38bdf8;
  background: rgba(56, 189, 248, 0.12);
  width: 52px;
  height: 52px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card-content h3 {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 22px;
  font-weight: 700;
  margin: 0 0 6px 0;
  color: #ffffff;
}

.card-content p {
  font-size: 16px;
  color: #94a3b8;
  margin: 0;
  line-height: 1.4;
}

/* Big Number Callout */
.big-stat-box {
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.15) 0%, rgba(99, 102, 241, 0.15) 100%);
  border: 1.5px solid rgba(56, 189, 248, 0.3);
  border-radius: 16px;
  padding: 36px 32px;
  text-align: center;
  margin: 20px 0;
}

.stat-number {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 76px;
  font-weight: 900;
  line-height: 1;
  color: #38bdf8;
  margin-bottom: 12px;
}

.stat-label {
  font-size: 20px;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 8px;
}

.stat-subtext {
  font-size: 15px;
  color: #94a3b8;
}

/* Slide Footer */
.slide-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 22px;
}

.footer-left {
  font-size: 14px;
  color: #64748b;
  font-weight: 500;
}

.swipe-cue {
  font-family: 'Plus Jakarta Sans', sans-serif;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 700;
  color: #38bdf8;
}

.swipe-arrow {
  display: inline-block;
  transition: transform 0.2s ease;
}
"""

def get_header(current_slide, total_slides):
    return f"""
    <div class="slide-header">
      <div class="author-badge">
        <div class="author-avatar">JS</div>
        <div class="author-info">
          <span class="author-name">Joel Adawah Sani</span>
          <span class="author-title">Principal Business Systems Consultant</span>
        </div>
      </div>
      <div class="slide-counter">{current_slide:02d} / {total_slides:02d}</div>
    </div>
    """

def get_footer(is_last=False):
    if is_last:
        return """
        <div class="slide-footer">
          <div class="footer-left">Joel Adawah Sani | Executive Systems Diagnostics</div>
          <div class="swipe-cue" style="color: #34d399;">SAVE & SHARE ✓</div>
        </div>
        """
    return """
    <div class="slide-footer">
      <div class="footer-left">Executive Operational Architecture</div>
      <div class="swipe-cue">SWIPE NEXT <span class="swipe-arrow">→</span></div>
    </div>
    """

def build_carousel_1():
    """Carousel 1: Speed to Lead & 9 PM Burst Pipe (6 slides)"""
    total = 6
    slides = [
        # Slide 1: Cover Hook
        f"""
        <div class="slide">
          {get_header(1, total)}
          <div class="slide-body">
            <span class="tag-pill tag-red">Operational Reality Check</span>
            <h1 class="slide-title">The 9:00 PM <span class="highlight">Burst Pipe</span></h1>
            <h2 class="slide-sub">Why response latency silently costs trade contractors <strong style="color: #f87171;">$14,500 every month</strong> — and how automated triage stops the bleed.</h2>
            <div class="big-stat-box">
              <div class="stat-number">60s</div>
              <div class="stat-label">The Critical Booking Window</div>
              <div class="stat-subtext">78% of emergency callers hire the first contractor who responds.</div>
            </div>
          </div>
          {get_footer()}
        </div>
        """,
        # Slide 2: The Problem
        f"""
        <div class="slide">
          {get_header(2, total)}
          <div class="slide-body">
            <span class="tag-pill tag-amber">The Breakdown</span>
            <h1 class="slide-title">Homeowners don't fill out forms in distress.</h1>
            <h2 class="slide-sub">When water is pouring through a ceiling, they aren't waiting 12 hours for an email reply.</h2>
            <div class="card-stack">
              <div class="feature-card">
                <div class="card-number">01</div>
                <div class="card-content">
                  <h3>They Call the Top 3 on Google Maps</h3>
                  <p>In high distress, homeowners call consecutively until someone answers or responds instantly.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="card-number">02</div>
                <div class="card-content">
                  <h3>Voicemail Is A Death Sentence</h3>
                  <p>Over 80% of emergency callers immediately hang up upon hearing a voicemail tone.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="card-number">03</div>
                <div class="card-content">
                  <h3>The Instant Responder Captures the Job</h3>
                  <p>A $3,500 emergency replacement goes to whoever acknowledges the distress within 60 seconds.</p>
                </div>
              </div>
            </div>
          </div>
          {get_footer()}
        </div>
        """,
        # Slide 3: The Leak
        f"""
        <div class="slide">
          {get_header(3, total)}
          <div class="slide-body">
            <span class="tag-pill tag-red">Financialized Model</span>
            <h1 class="slide-title">The Math Behind <span class="highlight">The Leakage</span></h1>
            <h2 class="slide-sub">What manual after-hours dispatch actually costs a 15-van plumbing contractor:</h2>
            <div class="big-stat-box" style="border-color: rgba(239, 68, 68, 0.4); background: rgba(220, 38, 38, 0.1);">
              <div class="stat-number" style="color: #f87171;">$174k</div>
              <div class="stat-label">Annual Lost Billable Capacity</div>
              <div class="stat-subtext">10 abandoned emergency calls/mo × $1,450 blended ticket size</div>
            </div>
            <div class="feature-card">
              <div class="card-number" style="color: #f87171; background: rgba(220, 38, 38, 0.15);">!</div>
              <div class="card-content">
                <h3>The Worst Part?</h3>
                <p>You already paid for the marketing lead via Google Ads or Local Services Ads. You just surrendered the payout at the finish line.</p>
              </div>
            </div>
          </div>
          {get_footer()}
        </div>
        """,
        # Slide 4: The 3-Step Solution
        f"""
        <div class="slide">
          {get_header(4, total)}
          <div class="slide-body">
            <span class="tag-pill tag-emerald">The Architecture</span>
            <h1 class="slide-title">The 3-Step <span class="highlight">Automated Triage</span> Stack</h1>
            <h2 class="slide-sub">Capture emergency jobs 24/7 without burning out your office staff:</h2>
            <div class="card-stack">
              <div class="feature-card">
                <div class="card-number">01</div>
                <div class="card-content">
                  <h3>Instant SMS Safety Protocol (&lt; 10s)</h3>
                  <p>Triggers immediate text greeting with water main shutoff instructions to protect the home.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="card-number">02</div>
                <div class="card-content">
                  <h3>Conversational Photo & Urgency Intake</h3>
                  <p>Asks homeowner to snap a photo of the leak and gathers address details automatically.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="card-number">03</div>
                <div class="card-content">
                  <h3>Direct CRM Dispatch Slot Reservation</h3>
                  <p>Locks in the morning arrival window or dispatches on-call truck based on emergency score.</p>
                </div>
              </div>
            </div>
          </div>
          {get_footer()}
        </div>
        """,
        # Slide 5: The ROI
        f"""
        <div class="slide">
          {get_header(5, total)}
          <div class="slide-body">
            <span class="tag-pill tag-blue">Operational Benchmark</span>
            <h1 class="slide-title">Speed to lead is <span class="highlight">operations</span>, not marketing.</h1>
            <h2 class="slide-sub">When you fix response latency, enterprise performance transforms:</h2>
            <div class="card-stack">
              <div class="feature-card">
                <div class="card-number" style="color: #34d399;">+</div>
                <div class="card-content">
                  <h3>Recaptures 10 to 15 High-Ticket Jobs / Mo</h3>
                  <p>Adds $14,500 to $22,000 in monthly gross billable work without a single dollar in extra ad spend.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="card-number" style="color: #34d399;">+</div>
                <div class="card-content">
                  <h3>Zero Midnight Phone Fatigue</h3>
                  <p>Owners and dispatchers sleep soundly knowing emergencies are triaged and logged cleanly.</p>
                </div>
              </div>
            </div>
          </div>
          {get_footer()}
        </div>
        """,
        # Slide 6: Summary & CTA
        f"""
        <div class="slide">
          {get_header(6, total)}
          <div class="slide-body">
            <span class="tag-pill tag-emerald">Executive Summary</span>
            <h1 class="slide-title">Ready to plug the <span class="highlight">leaks</span> in your firm?</h1>
            <h2 class="slide-sub">Review how this fits into an institutional 4-Pillar Executive Diagnostic:</h2>
            <div class="card-stack">
              <div class="feature-card" style="border: 1.5px solid #38bdf8; background: rgba(56, 189, 248, 0.08);">
                <div class="card-number">✓</div>
                <div class="card-content">
                  <h3>Inspect the Complete Sample Deliverable</h3>
                  <p>Check the <strong>4-page Executive Diagnostic PDF</strong> pinned in my <strong>Featured Section</strong> above.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="card-number">💬</div>
                <div class="card-content">
                  <h3>Request a 4-Pillar Audit for Your Fleet</h3>
                  <p>Send a direct message with your domain or schedule a 15-minute discovery call.</p>
                </div>
              </div>
            </div>
          </div>
          {get_footer(is_last=True)}
        </div>
        """
    ]
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CAROUSEL_CSS}</style></head><body>{"".join(slides)}</body></html>"""

def build_carousel_2():
    """Carousel 2: Choice Architecture & Good/Better/Best Quoting (5 slides)"""
    total = 5
    slides = [
        # Slide 1
        f"""
        <div class="slide">
          {get_header(1, total)}
          <div class="slide-body">
            <span class="tag-pill tag-amber">Pricing Strategy</span>
            <h1 class="slide-title">Why Single-Price Estimates <span class="highlight">Forfeit 22%</span> of Margin</h1>
            <h2 class="slide-sub">The subconscious psychology of contractor quoting — and how choice architecture transforms ticket sizes.</h2>
            <div class="big-stat-box">
              <div class="stat-number">+22%</div>
              <div class="stat-label">Average Ticket Size Lift</div>
              <div class="stat-subtext">Observed across 15-van plumbing and HVAC contractors.</div>
            </div>
          </div>
          {get_footer()}
        </div>
        """,
        # Slide 2
        f"""
        <div class="slide">
          {get_header(2, total)}
          <div class="slide-body">
            <span class="tag-pill tag-red">The Flaw</span>
            <h1 class="slide-title">The Binary Trap of Single Quotes</h1>
            <h2 class="slide-sub">When you give a customer one number (e.g. $4,800), you force a binary decision:</h2>
            <div class="card-stack">
              <div class="feature-card">
                <div class="card-number" style="color: #f87171;">VS</div>
                <div class="card-content">
                  <h3>"Should I buy this, or should I shop around?"</h3>
                  <p>The client's brain immediately compares your single price against the entire market or decides to delay.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="card-number" style="color: #f87171;">!</div>
                <div class="card-content">
                  <h3>Zero Choice for Upgrades</h3>
                  <p>Customers who value premium warranties, filtration, or higher-efficiency units are never given the chance to say yes.</p>
                </div>
              </div>
            </div>
          </div>
          {get_footer()}
        </div>
        """,
        # Slide 3
        f"""
        <div class="slide">
          {get_header(3, total)}
          <div class="slide-body">
            <span class="tag-pill tag-blue">The Architecture</span>
            <h1 class="slide-title">The 3-Tier <span class="highlight">Choice Architecture</span></h1>
            <h2 class="slide-sub">Switch field technicians to digital Good / Better / Best estimates:</h2>
            <div class="card-stack">
              <div class="feature-card">
                <div class="card-number">01</div>
                <div class="card-content">
                  <h3>Tier 1: Standard (Baseline)</h3>
                  <p>Solves the immediate mechanical failure. Standard 1-year warranty.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="card-number">02</div>
                <div class="card-content">
                  <h3>Tier 2: Enhanced (Most Popular)</h3>
                  <p>Upgraded equipment + 5-year labor warranty + free seasonal tune-up.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="card-number">03</div>
                <div class="card-content">
                  <h3>Tier 3: Premium (Total Peace of Mind)</h3>
                  <p>High-efficiency system + whole-home filtration + lifetime membership.</p>
                </div>
              </div>
            </div>
          </div>
          {get_footer()}
        </div>
        """,
        # Slide 4
        f"""
        <div class="slide">
          {get_header(4, total)}
          <div class="slide-body">
            <span class="tag-pill tag-emerald">The Outcome</span>
            <h1 class="slide-title">The Psychological Shift</h1>
            <h2 class="slide-sub">The customer's question shifts from external shopping to internal selection:</h2>
            <div class="big-stat-box" style="border-color: rgba(52, 211, 153, 0.3); background: rgba(5, 150, 105, 0.1);">
              <div class="stat-number" style="color: #34d399;">60%</div>
              <div class="stat-label">Choose Tier 2 or Tier 3</div>
              <div class="stat-subtext">Clients self-select higher tiers when choice architecture is clear.</div>
            </div>
            <div class="feature-card">
              <div class="card-number">✓</div>
              <div class="card-content">
                <h3>Zero Extra Lead Costs</h3>
                <p>Generating an extra $18,000 to $25,000 monthly from the exact same job volume.</p>
              </div>
            </div>
          </div>
          {get_footer()}
        </div>
        """,
        # Slide 5
        f"""
        <div class="slide">
          {get_header(5, total)}
          <div class="slide-body">
            <span class="tag-pill tag-blue">Executive Deliverable</span>
            <h1 class="slide-title">See the Full <span class="highlight">Economic Model</span></h1>
            <h2 class="slide-sub">How this ties into our complete 4-Pillar Executive Diagnostic:</h2>
            <div class="card-stack">
              <div class="feature-card" style="border: 1.5px solid #38bdf8;">
                <div class="card-number">📊</div>
                <div class="card-content">
                  <h3>Full Financial Leakage Model</h3>
                  <p>Review the <strong>Deloitte Effort vs. Impact Prioritization Matrix</strong> in the sample audit in my <strong>Featured Section</strong>.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="card-number">🤝</div>
                <div class="card-content">
                  <h3>Connect with Joel Adawah Sani</h3>
                  <p>DM me to audit your firm's quoting workflows and field software stack.</p>
                </div>
              </div>
            </div>
          </div>
          {get_footer(is_last=True)}
        </div>
        """
    ]
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CAROUSEL_CSS}</style></head><body>{"".join(slides)}</body></html>"""

def build_carousel_3():
    """Carousel 3: Dual-Trade Cross-Sell Silos (6 slides)"""
    total = 6
    slides = [
        # Slide 1
        f"""
        <div class="slide">
          {get_header(1, total)}
          <div class="slide-body">
            <span class="tag-pill tag-blue">Dual-Trade Growth</span>
            <h1 class="slide-title">The <span class="highlight">$216,000</span> Cross-Sell Silo</h1>
            <h2 class="slide-sub">If you offer Plumbing AND HVAC, why are 88% of your plumbing clients calling your competitor for AC?</h2>
            <div class="big-stat-box">
              <div class="stat-number">88%</div>
              <div class="stat-label">Uncaptured Secondary Trade Volume</div>
              <div class="stat-subtext">The hidden friction point inside dual-trade mechanical contractors.</div>
            </div>
          </div>
          {get_footer()}
        </div>
        """,
        # Slide 2
        f"""
        <div class="slide">
          {get_header(2, total)}
          <div class="slide-body">
            <span class="tag-pill tag-amber">The Bottleneck</span>
            <h1 class="slide-title">Why Field Techs Don't Cross-Sell</h1>
            <h2 class="slide-sub">Most owners blame their technicians: "They just don't remember to ask."</h2>
            <div class="card-stack">
              <div class="feature-card">
                <div class="card-number">01</div>
                <div class="card-content">
                  <h3>Technicians Are Fixers, Not Marketers</h3>
                  <p>A plumber's focus is resolving the immediate leak, clearing the drain, and moving to the next ticket.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="card-number">02</div>
                <div class="card-content">
                  <h3>Software Operates in Silos</h3>
                  <p>The dispatch CRM records the plumbing invoice, but never alerts the HVAC department to follow up.</p>
                </div>
              </div>
            </div>
          </div>
          {get_footer()}
        </div>
        """,
        # Slide 3
        f"""
        <div class="slide">
          {get_header(3, total)}
          <div class="slide-body">
            <span class="tag-pill tag-red">Financialized Model</span>
            <h1 class="slide-title">The Cost of <span class="highlight">Disconnected Silos</span></h1>
            <h2 class="slide-sub">In our audit of an 18-van dual-trade contractor (Summit Mechanical):</h2>
            <div class="big-stat-box" style="border-color: rgba(220, 38, 38, 0.4); background: rgba(220, 38, 38, 0.1);">
              <div class="stat-number" style="color: #f87171;">$18k/mo</div>
              <div class="stat-label">Forfeited Recurring Cash Flow</div>
              <div class="stat-subtext">1,200 single-trade residential accounts with zero automated cross-sell.</div>
            </div>
            <div class="feature-card">
              <div class="card-number" style="color: #f87171;">!</div>
              <div class="card-content">
                <h3>Annualized Value: $216,000</h3>
                <p>Lost recurring maintenance memberships and high-ticket pull-through equipment replacements.</p>
              </div>
            </div>
          </div>
          {get_footer()}
        </div>
        """,
        # Slide 4
        f"""
        <div class="slide">
          {get_header(4, total)}
          <div class="slide-body">
            <span class="tag-pill tag-emerald">The Architecture</span>
            <h1 class="slide-title">The 3 Automated <span class="highlight">Cross-Sell</span> Workflows</h1>
            <h2 class="slide-sub">Automate the handoff so technicians never have to pitch:</h2>
            <div class="card-stack">
              <div class="feature-card">
                <div class="card-number">01</div>
                <div class="card-content">
                  <h3>Invoice Sign-Off Webhook</h3>
                  <p>CRM webhook detects a single-trade completed job and tags the customer profile automatically.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="card-number">02</div>
                <div class="card-content">
                  <h3>Seasonal Cross-Trade Inspection Offer</h3>
                  <p>Triggers a complimentary pre-summer AC inspection or winter water-heater check 14 days later.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="card-number">03</div>
                <div class="card-content">
                  <h3>Unified Dual-Trade Membership</h3>
                  <p>One membership agreement protecting both HVAC and Plumbing for high client lifetime value.</p>
                </div>
              </div>
            </div>
          </div>
          {get_footer()}
        </div>
        """,
        # Slide 5
        f"""
        <div class="slide">
          {get_header(5, total)}
          <div class="slide-body">
            <span class="tag-pill tag-blue">Enterprise Impact</span>
            <h1 class="slide-title">Predictable Cash Flow & Client Retention</h1>
            <h2 class="slide-sub">Contractors with unified membership agreements command 3x valuation multiples:</h2>
            <div class="card-stack">
              <div class="feature-card">
                <div class="card-number" style="color: #34d399;">✓</div>
                <div class="card-content">
                  <h3>Zero Churn to Competitors</h3>
                  <p>Customers with dual-trade memberships don't search Google Maps when emergencies happen.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="card-number" style="color: #34d399;">✓</div>
                <div class="card-content">
                  <h3>Smooth Out Shoulder Seasons</h3>
                  <p>Recurring membership revenue keeps trucks running during slow spring and fall months.</p>
                </div>
              </div>
            </div>
          </div>
          {get_footer()}
        </div>
        """,
        # Slide 6
        f"""
        <div class="slide">
          {get_header(6, total)}
          <div class="slide-body">
            <span class="tag-pill tag-emerald">Take Action</span>
            <h1 class="slide-title">Inspect Your Firm's <span class="highlight">Workflows</span></h1>
            <h2 class="slide-sub">Download our complete dual-trade diagnostic deliverable:</h2>
            <div class="card-stack">
              <div class="feature-card" style="border: 1.5px solid #38bdf8;">
                <div class="card-number">📄</div>
                <div class="card-content">
                  <h3>Summit Mechanical Showcase Audit</h3>
                  <p>Review the full <strong>4-page executive diagnostic PDF</strong> pinned in my <strong>Featured Section</strong>.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="card-number">📅</div>
                <div class="card-content">
                  <h3>Book an Operational Discovery Call</h3>
                  <p>Use the calendar link on my profile for a 1-on-1 operational audit walkthrough.</p>
                </div>
              </div>
            </div>
          </div>
          {get_footer(is_last=True)}
        </div>
        """
    ]
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CAROUSEL_CSS}</style></head><body>{"".join(slides)}</body></html>"""

def build_carousel_4():
    """Carousel 4: The 4-Pillar Executive Diagnostic Framework (5 slides)"""
    total = 5
    slides = [
        # Slide 1
        f"""
        <div class="slide">
          {get_header(1, total)}
          <div class="slide-body">
            <span class="tag-pill tag-blue">Methodology</span>
            <h1 class="slide-title">Inside an Institutional <span class="highlight">4-Pillar Diagnostic</span></h1>
            <h2 class="slide-sub">Why traditional business audits fail — and how engineering rigor pinpoints exact dollarized leakage.</h2>
            <div class="big-stat-box">
              <div class="stat-number">4-Pillars</div>
              <div class="stat-label">Sales · Support · Field Delivery · Internal Ops</div>
              <div class="stat-subtext">The institutional framework for $1M–$10M trade contractors.</div>
            </div>
          </div>
          {get_footer()}
        </div>
        """,
        # Slide 2
        f"""
        <div class="slide">
          {get_header(2, total)}
          <div class="slide-body">
            <span class="tag-pill tag-amber">The 4 Domains</span>
            <h1 class="slide-title">The 4 Operational Pillars</h1>
            <h2 class="slide-sub">We evaluate enterprise infrastructure across 4 independent systems:</h2>
            <div class="card-stack">
              <div class="feature-card">
                <div class="card-number">01</div>
                <div class="card-content">
                  <h3>Sales & Customer Acquisition</h3>
                  <p>Mobile TTFB latency, review velocity, and suburban landing page coverage.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="card-number">02</div>
                <div class="card-content">
                  <h3>Customer Support & Dispatch Intake</h3>
                  <p>Speed to lead, 24/7 emergency triage, and CRM booking workflows.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="card-number">03</div>
                <div class="card-content">
                  <h3>Field Service & Delivery</h3>
                  <p>Technician en-route SMS, GPS visibility, and tiered Good/Better/Best quoting.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="card-number">04</div>
                <div class="card-content">
                  <h3>Internal Operations & Infrastructure</h3>
                  <p>DNS authorization (SPF/DKIM/DMARC), billing automation, and CRM sync.</p>
                </div>
              </div>
            </div>
          </div>
          {get_footer()}
        </div>
        """,
        # Slide 3
        f"""
        <div class="slide">
          {get_header(3, total)}
          <div class="slide-body">
            <span class="tag-pill tag-emerald">Diagnostic Rigor</span>
            <h1 class="slide-title">The 4-Step <span class="highlight">Reasoning Scaffold</span></h1>
            <h2 class="slide-sub">Zero vague opinions. Every score is derived through a strict formula:</h2>
            <div class="card-stack">
              <div class="feature-card">
                <div class="card-number">A</div>
                <div class="card-content">
                  <h3>Evidence (Observed Telemetry)</h3>
                  <p>Raw technical signals from DNS records, server latency, and GBP reviews.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="card-number">B</div>
                <div class="card-content">
                  <h3>Expected State (Benchmark)</h3>
                  <p>The operational benchmark achieved by top-decile firms in your sector.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="card-number">C</div>
                <div class="card-content">
                  <h3>Gap Magnitude & Dollarized Leakage</h3>
                  <p>Measuring the operational delta into exact monthly and annual revenue lost.</p>
                </div>
              </div>
            </div>
          </div>
          {get_footer()}
        </div>
        """,
        # Slide 4
        f"""
        <div class="slide">
          {get_header(4, total)}
          <div class="slide-body">
            <span class="tag-pill tag-blue">Prioritization</span>
            <h1 class="slide-title">Deloitte Effort vs. Impact Prioritization</h1>
            <h2 class="slide-sub">Categorizing all recommendations into high-ROI quick wins:</h2>
            <div class="card-stack">
              <div class="feature-card">
                <div class="card-number" style="color: #34d399;">QW</div>
                <div class="card-content">
                  <h3>Phase 1: Tactical Quick Wins (&lt; 30 Days)</h3>
                  <p>Low-CapEx, high-return adjustments (DNS repair, review SMS, tiered quoting) with &lt; 14-day payback.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="card-number" style="color: #38bdf8;">OS</div>
                <div class="card-content">
                  <h3>Phase 2: Operational Scale (30–90 Days)</h3>
                  <p>24/7 automated intake triage, automated membership cross-sell, and suburban SEO expansion.</p>
                </div>
              </div>
            </div>
          </div>
          {get_footer()}
        </div>
        """,
        # Slide 5
        f"""
        <div class="slide">
          {get_header(5, total)}
          <div class="slide-body">
            <span class="tag-pill tag-emerald">Executive Deliverables</span>
            <h1 class="slide-title">Review the Full <span class="highlight">Audit Deliverables</span></h1>
            <h2 class="slide-sub">Institutional consulting delivered with total transparency:</h2>
            <div class="card-stack">
              <div class="feature-card" style="border: 1.5px solid #38bdf8;">
                <div class="card-number">★</div>
                <div class="card-content">
                  <h3>Explore the Featured Section</h3>
                  <p>Download our complete 4-page sample diagnostics for <strong>Apex Home Services</strong> and <strong>Summit Mechanical</strong>.</p>
                </div>
              </div>
              <div class="feature-card">
                <div class="card-number">✉</div>
                <div class="card-content">
                  <h3>Connect with Joel Adawah Sani</h3>
                  <p>Principal Business Systems Consultant. DM me or schedule a 15-minute discovery call.</p>
                </div>
              </div>
            </div>
          </div>
          {get_footer(is_last=True)}
        </div>
        """
    ]
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CAROUSEL_CSS}</style></head><body>{"".join(slides)}</body></html>"""

async def render_carousel(html_content, output_pdf_path):
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge")
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})
        await page.set_content(html_content, wait_until="networkidle")
        await page.pdf(
            path=output_pdf_path,
            width="1080px",
            height="1350px",
            print_background=True,
            margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
        )
        await browser.close()

def main():
    carousels = [
        ("carousel_1_speed_to_lead", build_carousel_1()),
        ("carousel_2_choice_architecture", build_carousel_2()),
        ("carousel_3_dual_trade_cross_sell", build_carousel_3()),
        ("carousel_4_four_pillar_audit", build_carousel_4()),
    ]
    
    out_dir = Path("outputs/linkedin_content/carousels")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    for name, html in carousels:
        pdf_path = str(out_dir / f"{name}.pdf")
        html_path = str(out_dir / f"{name}.html")
        
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
            
        print(f"Rendering carousel: {pdf_path}...")
        asyncio.run(render_carousel(html, pdf_path))
        
        reader = pypdf.PdfReader(pdf_path)
        print(f"Verified {name}.pdf: {len(reader.pages)} slides rendered successfully.")

    print("\nALL 4 LINKEDIN CAROUSELS RENDERED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
