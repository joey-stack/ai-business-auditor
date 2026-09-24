import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  staticFile,
  Audio,
  Sequence,
} from "remotion";

export const TikTokVideo3: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Continuous Camera Drift & Ambient Particles (Jorge Canedo Principles)
  const camTiltX = Math.sin(frame / 46) * 1.5;
  const camTiltY = Math.cos(frame / 52) * 1.3;
  const orb1X = Math.sin(frame / 42) * 105;
  const orb1Y = Math.cos(frame / 48) * 85;
  const orb2X = Math.cos(frame / 50) * 115;
  const orb2Y = Math.sin(frame / 44) * 90;

  // Screen Shake on impacts
  const shake1 = frame - 460;
  const shake2 = frame - 1200;
  let shakeOffset = 0;
  if (shake1 >= 0 && shake1 < 12) {
    shakeOffset = Math.sin(shake1 * 3.0) * interpolate(shake1, [0, 12], [14, 0], { extrapolateRight: "clamp" });
  } else if (shake2 >= 0 && shake2 < 12) {
    shakeOffset = Math.sin(shake2 * 3.0) * interpolate(shake2, [0, 12], [12, 0], { extrapolateRight: "clamp" });
  }

  // Top Progress Bar
  const totalFrames = 1925;
  const progressPct = Math.min(100, (frame / totalFrames) * 100);

  // Synchronized Subtitles
  const subtitles = [
    { start: 0, end: 240, text: "Here is the exact 3-step automation that stops emergency calls from ruining family dinner." },
    { start: 240, end: 380, text: "Every contractor tells me: either my phone rings off the hook at dinner..." },
    { start: 380, end: 520, text: "Or I miss out on thousands in revenue. Here's how we fix it with zero added headcount." },
    { start: 520, end: 720, text: "Step 1: Instant SMS Trigger. If a call is missed after hours, an automated text fires in 10 seconds." },
    { start: 720, end: 920, text: "'We see you called! Are you experiencing an active water leak or safety hazard?'" },
    { start: 920, end: 1180, text: "Step 2: Interactive Triage. If they text 'Yes', they get safety shutoff steps + tech alert." },
    { start: 1180, end: 1420, text: "If 'No', the job is automatically queued for Monday at 8:00 AM." },
    { start: 1420, end: 1680, text: "Step 3: Zero Headcount. You capture $2,500 emergency jobs without paying a $3,000/mo call center." },
    { start: 1680, end: 1925, text: "Tap the link in my bio to see the exact 3-step workflow." },
  ];

  const currentSub = subtitles.find((s) => frame >= s.start && frame < s.end);

  return (
    <div
      style={{
        width: 1080,
        height: 1920,
        backgroundColor: "#05070B",
        backgroundImage: `
          radial-gradient(circle at 50% 12%, rgba(245, 158, 11, 0.12) 0%, transparent 55%),
          radial-gradient(circle at 50% 88%, rgba(14, 165, 233, 0.12) 0%, transparent 60%),
          linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
          linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px)
        `,
        backgroundSize: "100% 100%, 100% 100%, 48px 48px, 48px 48px",
        color: "#F8FAFC",
        fontFamily: "'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif",
        position: "relative",
        overflow: "hidden",
        transform: `translate(${shakeOffset}px, ${shakeOffset * 0.5}px) perspective(1200px) rotateX(${camTiltX}deg) rotateY(${camTiltY}deg)`,
      }}
    >
      {/* 1. MASTER VOICE & TACTILE SFX */}
      <Audio src={staticFile("audio_v3.mp3")} volume={1.0} />

      <Sequence from={0} durationInFrames={20}>
        <Audio src={staticFile("sfx/whoosh.wav")} volume={0.4} />
      </Sequence>

      {/* Frame 120 Ping on 3-Step Banner */}
      <Sequence from={120} durationInFrames={25}>
        <Audio src={staticFile("sfx/ping.wav")} volume={0.5} />
      </Sequence>

      {/* Frame 240 Whoosh into Dilemma */}
      <Sequence from={240} durationInFrames={20}>
        <Audio src={staticFile("sfx/whoosh.wav")} volume={0.45} />
      </Sequence>

      {/* Frame 460 Slam on Zero Headcount */}
      <Sequence from={460} durationInFrames={25}>
        <Audio src={staticFile("sfx/slam.wav")} volume={0.75} />
      </Sequence>

      {/* Frame 520 Whoosh into Step 1 SMS */}
      <Sequence from={520} durationInFrames={20}>
        <Audio src={staticFile("sfx/whoosh.wav")} volume={0.45} />
      </Sequence>

      {/* Frame 680 Click for SMS Send */}
      <Sequence from={680} durationInFrames={15}>
        <Audio src={staticFile("sfx/click.wav")} volume={0.6} />
      </Sequence>

      {/* Frame 920 Whoosh into Step 2 Triage */}
      <Sequence from={920} durationInFrames={20}>
        <Audio src={staticFile("sfx/whoosh.wav")} volume={0.45} />
      </Sequence>

      {/* Frame 1080 Alert on Priority Tech Alert */}
      <Sequence from={1080} durationInFrames={25}>
        <Audio src={staticFile("sfx/alert.wav")} volume={0.65} />
      </Sequence>

      {/* Frame 1420 Whoosh into Step 3 Financial Capture */}
      <Sequence from={1420} durationInFrames={20}>
        <Audio src={staticFile("sfx/whoosh.wav")} volume={0.45} />
      </Sequence>

      {/* Frame 1520 Ding on $2,500 Ticket Won */}
      <Sequence from={1520} durationInFrames={35}>
        <Audio src={staticFile("sfx/ding.wav")} volume={0.8} />
      </Sequence>

      {/* Frame 1720 Ping on Bio CTA */}
      <Sequence from={1720} durationInFrames={30}>
        <Audio src={staticFile("sfx/ping.wav")} volume={0.6} />
      </Sequence>

      {/* PROGRESS BAR */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: 10,
          background: "rgba(255, 255, 255, 0.08)",
          zIndex: 200,
        }}
      >
        <div
          style={{
            height: "100%",
            width: `${progressPct}%`,
            background: "linear-gradient(90deg, #F59E0B, #0284C7, #10B981)",
            boxShadow: "0 0 15px #F59E0B",
          }}
        />
      </div>

      {/* AMBIENT ORBS */}
      <div
        style={{
          position: "absolute",
          width: 750,
          height: 750,
          borderRadius: "50%",
          background: "#D97706",
          filter: "blur(140px)",
          opacity: 0.20,
          top: -100,
          right: -100,
          transform: `translate(${orb1X}px, ${orb1Y}px)`,
          pointerEvents: "none",
        }}
      />
      <div
        style={{
          position: "absolute",
          width: 700,
          height: 700,
          borderRadius: "50%",
          background: "#0284C7",
          filter: "blur(140px)",
          opacity: 0.18,
          bottom: 100,
          left: -120,
          transform: `translate(${orb2X}px, ${orb2Y}px)`,
          pointerEvents: "none",
        }}
      />

      {/* BRAND HEADER */}
      <div
        style={{
          position: "absolute",
          top: 55,
          left: 70,
          right: 70,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          zIndex: 100,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <div
            style={{
              width: 48,
              height: 48,
              borderRadius: 14,
              background: "linear-gradient(135deg, #F59E0B, #EA580C)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontWeight: 800,
              fontSize: 22,
              color: "#FFF",
              boxShadow: "0 4px 15px rgba(245, 158, 11, 0.4)",
            }}
          >
            🍲
          </div>
          <div>
            <div style={{ fontSize: 22, fontWeight: 800, letterSpacing: "-0.02em" }}>
              JOEL ADAWAH SANI
            </div>
            <div
              style={{
                fontSize: 14,
                color: "#94A3B8",
                fontWeight: 600,
                letterSpacing: "0.08em",
                textTransform: "uppercase",
              }}
            >
              Principal Business Systems Consultant
            </div>
          </div>
        </div>

        <div
          style={{
            background: "rgba(245, 158, 11, 0.12)",
            border: "1px solid rgba(245, 158, 11, 0.35)",
            padding: "8px 18px",
            borderRadius: 30,
            fontSize: 14,
            fontWeight: 800,
            color: "#FBBF24",
            letterSpacing: "0.05em",
            display: "flex",
            alignItems: "center",
            gap: 8,
          }}
        >
          <span
            style={{
              width: 8,
              height: 8,
              borderRadius: "50%",
              backgroundColor: "#F59E0B",
              boxShadow: "0 0 10px #F59E0B",
            }}
          />
          VIDEO #03 • DISPATCH WORKFLOW
        </div>
      </div>

      {/* ========================================================================= */}
      {/* SCENE 1: THE HOOK — PROTECT YOUR WEEKEND DINNER (Frames 0 - 240, 0s - 8s) */}
      {/* ========================================================================= */}
      {frame < 255 && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            padding: "160px 70px 240px",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            opacity: interpolate(frame, [0, 15, 235, 250], [0, 1, 1, 0], { extrapolateRight: "clamp" }),
            transform: `scale(${interpolate(frame, [0, 20], [0.92, 1], { extrapolateRight: "clamp" })})`,
          }}
        >
          <div
            style={{
              background: "rgba(245, 158, 11, 0.15)",
              border: "1px solid rgba(245, 158, 11, 0.4)",
              borderRadius: 40,
              padding: "10px 24px",
              color: "#FBBF24",
              fontSize: 17,
              fontWeight: 800,
              letterSpacing: "0.12em",
              textTransform: "uppercase",
              marginBottom: 28,
            }}
          >
            AFTER-HOURS DISPATCH AUTOMATION
          </div>

          <h1
            style={{
              fontSize: 66,
              fontWeight: 900,
              lineHeight: 1.15,
              textAlign: "center",
              letterSpacing: "-0.03em",
              marginBottom: 44,
              maxWidth: 920,
            }}
          >
            How To Protect Your <br />
            <span
              style={{
                background: "linear-gradient(135deg, #FBBF24, #F97316)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
              }}
            >
              Weekend Dinner 📱🍲
            </span>
          </h1>

          {/* 3-Step Sequence Overview Badge */}
          {(() => {
            const cardSpring = spring({ frame: frame - 60, fps, config: { stiffness: 180, damping: 14 } });
            return (
              <div
                style={{
                  width: "100%",
                  maxWidth: 920,
                  background: "linear-gradient(145deg, #0F172A, #070B14)",
                  border: "1px solid rgba(245, 158, 11, 0.35)",
                  borderRadius: 28,
                  padding: "40px",
                  boxShadow: "0 30px 60px rgba(0, 0, 0, 0.7)",
                  display: "flex",
                  justifyContent: "space-around",
                  alignItems: "center",
                  transform: `scale(${interpolate(cardSpring, [0, 1], [0.85, 1])}) translateY(${interpolate(cardSpring, [0, 1], [40, 0])}px)`,
                  opacity: interpolate(cardSpring, [0, 1], [0, 1]),
                }}
              >
                {[
                  { step: "01", title: "10s SMS Trigger", desc: "Instant Acknowledgment", icon: "⚡" },
                  { step: "02", title: "Interactive Triage", desc: "Emergency vs Routine", icon: "🔍" },
                  { step: "03", title: "Zero Headcount", desc: "$2,500 Captured", icon: "💰" },
                ].map((item, idx) => (
                  <div key={idx} style={{ textAlign: "center", width: 240 }}>
                    <div
                      style={{
                        width: 76,
                        height: 76,
                        borderRadius: 22,
                        background: "rgba(245, 158, 11, 0.15)",
                        border: "1.5px solid #F59E0B",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        fontSize: 34,
                        margin: "0 auto 14px",
                      }}
                    >
                      {item.icon}
                    </div>
                    <div style={{ fontSize: 14, color: "#FBBF24", fontWeight: 800, letterSpacing: "0.1em" }}>
                      STEP {item.step}
                    </div>
                    <div style={{ fontSize: 20, fontWeight: 900, color: "#FFF", marginTop: 4 }}>
                      {item.title}
                    </div>
                    <div style={{ fontSize: 14, color: "#94A3B8", marginTop: 2 }}>{item.desc}</div>
                  </div>
                ))}
              </div>
            );
          })()}
        </div>
      )}

      {/* ========================================================================= */}
      {/* SCENE 2: THE FOUNDER DILEMMA (Frames 240 - 520, 8s - 17.3s)                */}
      {/* ========================================================================= */}
      {frame >= 235 && frame < 535 && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            padding: "160px 70px 240px",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            opacity: interpolate(frame, [240, 260, 510, 530], [0, 1, 1, 0], { extrapolateRight: "clamp" }),
            transform: `scale(${interpolate(frame, [245, 265], [0.92, 1], { extrapolateRight: "clamp" })})`,
          }}
        >
          <div
            style={{
              background: "rgba(239, 68, 68, 0.15)",
              border: "1px solid rgba(239, 68, 68, 0.4)",
              borderRadius: 40,
              padding: "10px 24px",
              color: "#F87171",
              fontSize: 17,
              fontWeight: 800,
              letterSpacing: "0.12em",
              textTransform: "uppercase",
              marginBottom: 24,
            }}
          >
            THE CONTRACTOR'S DILEMMA
          </div>

          <h2
            style={{
              fontSize: 58,
              fontWeight: 900,
              lineHeight: 1.15,
              textAlign: "center",
              letterSpacing: "-0.03em",
              marginBottom: 36,
            }}
          >
            "Either My Phone Rings At Dinner... <br />
            Or I Lose{" "}
            <span
              style={{
                background: "linear-gradient(135deg, #F87171, #EF4444)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
              }}
            >
              Thousands in Revenue."
            </span>
          </h2>

          <div style={{ width: "100%", maxWidth: 920, display: "flex", gap: 24, marginBottom: 30 }}>
            <div
              style={{
                flex: 1,
                background: "rgba(15, 23, 42, 0.8)",
                border: "1px solid rgba(239, 68, 68, 0.35)",
                borderRadius: 24,
                padding: "32px",
                textAlign: "center",
              }}
            >
              <div style={{ fontSize: 50, marginBottom: 12 }}>📞😵</div>
              <div style={{ fontSize: 24, fontWeight: 900, color: "#F87171" }}>TRAP #1</div>
              <div style={{ fontSize: 22, fontWeight: 800, marginTop: 6 }}>Answering Manually</div>
              <div style={{ fontSize: 16, color: "#94A3B8", marginTop: 8 }}>
                Family dinners interrupted by tire-kickers and routine inquiries.
              </div>
            </div>

            <div
              style={{
                flex: 1,
                background: "rgba(15, 23, 42, 0.8)",
                border: "1px solid rgba(239, 68, 68, 0.35)",
                borderRadius: 24,
                padding: "32px",
                textAlign: "center",
              }}
            >
              <div style={{ fontSize: 50, marginBottom: 12 }}>💸📉</div>
              <div style={{ fontSize: 24, fontWeight: 900, color: "#F87171" }}>TRAP #2</div>
              <div style={{ fontSize: 22, fontWeight: 800, marginTop: 6 }}>Ignoring Calls</div>
              <div style={{ fontSize: 16, color: "#94A3B8", marginTop: 8 }}>
                $3,500 burst pipe replacement walks straight to the competitor.
              </div>
            </div>
          </div>

          {/* Solution Banner */}
          {(() => {
            const solSpring = spring({ frame: frame - 440, fps, config: { stiffness: 200, damping: 14 } });
            return (
              <div
                style={{
                  width: "100%",
                  maxWidth: 920,
                  background: "linear-gradient(135deg, #0284C7, #059669)",
                  borderRadius: 24,
                  padding: "24px 36px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  boxShadow: "0 20px 40px rgba(0, 0, 0, 0.6)",
                  transform: `scale(${interpolate(solSpring, [0, 1], [0.85, 1])})`,
                  opacity: interpolate(solSpring, [0, 1], [0, 1]),
                }}
              >
                <div style={{ fontSize: 28, fontWeight: 900, color: "#FFF" }}>
                  ⚡ The Solution: Automated Triage
                </div>
                <div
                  style={{
                    background: "rgba(255, 255, 255, 0.2)",
                    padding: "8px 20px",
                    borderRadius: 30,
                    fontSize: 18,
                    fontWeight: 900,
                  }}
                >
                  ZERO HEADCOUNT
                </div>
              </div>
            );
          })()}
        </div>
      )}

      {/* ========================================================================= */}
      {/* SCENE 3: STEP 1 — INSTANT 10-SEC SMS TRIGGER (Frames 520 - 920, 17s - 30s) */}
      {/* ========================================================================= */}
      {frame >= 510 && frame < 930 && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            padding: "160px 70px 240px",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            opacity: interpolate(frame, [515, 535, 910, 925], [0, 1, 1, 0], { extrapolateRight: "clamp" }),
            transform: `scale(${interpolate(frame, [520, 540], [0.92, 1], { extrapolateRight: "clamp" })})`,
          }}
        >
          <div
            style={{
              background: "rgba(14, 165, 233, 0.15)",
              border: "1px solid rgba(14, 165, 233, 0.4)",
              borderRadius: 40,
              padding: "10px 24px",
              color: "#38BDF8",
              fontSize: 17,
              fontWeight: 800,
              letterSpacing: "0.12em",
              textTransform: "uppercase",
              marginBottom: 24,
            }}
          >
            STEP 01 • LATENCY ELIMINATION
          </div>

          <h2
            style={{
              fontSize: 58,
              fontWeight: 900,
              lineHeight: 1.15,
              textAlign: "center",
              letterSpacing: "-0.03em",
              marginBottom: 36,
            }}
          >
            The{" "}
            <span
              style={{
                background: "linear-gradient(135deg, #38BDF8, #818CF8)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
              }}
            >
              10-Second SMS Trigger
            </span>
          </h2>

          {/* Smartphone SMS Simulation Card */}
          <div
            style={{
              width: "100%",
              maxWidth: 920,
              background: "linear-gradient(145deg, #0B111E, #070B14)",
              border: "1px solid rgba(56, 189, 248, 0.35)",
              borderRadius: 28,
              padding: "36px",
              boxShadow: "0 30px 60px rgba(0, 0, 0, 0.7)",
            }}
          >
            {/* Event 1: Unassisted Call */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 16,
                background: "rgba(244, 63, 94, 0.12)",
                border: "1px solid rgba(244, 63, 94, 0.3)",
                borderRadius: 18,
                padding: "18px 24px",
                marginBottom: 24,
              }}
            >
              <div style={{ fontSize: 28 }}>📵</div>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 18, fontWeight: 900, color: "#FB7185" }}>
                  Inbound Call Missed • Saturday 7:42 PM
                </div>
                <div style={{ fontSize: 14, color: "#94A3B8" }}>
                  Contractor at family dinner • Dispatch line unassisted
                </div>
              </div>
              <div
                style={{
                  background: "#F43F5E",
                  color: "#FFF",
                  fontWeight: 900,
                  fontSize: 13,
                  padding: "6px 14px",
                  borderRadius: 20,
                }}
              >
                AUTOMATION ENGAGED
              </div>
            </div>

            {/* Event 2: Instant Auto SMS */}
            <div
              style={{
                background: "rgba(15, 23, 42, 0.95)",
                border: "2px solid #0284C7",
                borderRadius: 22,
                padding: "28px",
                position: "relative",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
                <div style={{ fontSize: 15, color: "#38BDF8", fontWeight: 800, letterSpacing: "0.08em" }}>
                  💬 OUTBOUND 2-WAY DISPATCH SMS (8 SECONDS)
                </div>
                <div style={{ fontSize: 13, color: "#94A3B8", fontFamily: "'JetBrains Mono', monospace" }}>
                  Delivered 7:42:08 PM
                </div>
              </div>

              <div
                style={{
                  background: "#0284C7",
                  color: "#FFF",
                  padding: "22px 26px",
                  borderRadius: "20px 20px 4px 20px",
                  fontSize: 24,
                  fontWeight: 700,
                  lineHeight: 1.4,
                  boxShadow: "0 10px 25px rgba(2, 132, 199, 0.3)",
                }}
              >
                "Hi! We see you just called. Are you experiencing an <strong>active water leak</strong> or <strong>immediate safety hazard</strong>?"
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* SCENE 4: STEP 2 — INTERACTIVE AI TRIAGE (Frames 920 - 1420, 30s - 47s)     */}
      {/* ========================================================================= */}
      {frame >= 915 && frame < 1435 && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            padding: "160px 70px 240px",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            opacity: interpolate(frame, [920, 940, 1405, 1425], [0, 1, 1, 0], { extrapolateRight: "clamp" }),
            transform: `scale(${interpolate(frame, [925, 945], [0.92, 1], { extrapolateRight: "clamp" })})`,
          }}
        >
          <div
            style={{
              background: "rgba(16, 185, 129, 0.15)",
              border: "1px solid rgba(16, 185, 129, 0.4)",
              borderRadius: 40,
              padding: "10px 24px",
              color: "#34D399",
              fontSize: 17,
              fontWeight: 800,
              letterSpacing: "0.12em",
              textTransform: "uppercase",
              marginBottom: 24,
            }}
          >
            STEP 02 • INTERACTIVE TRIAGE
          </div>

          <h2
            style={{
              fontSize: 58,
              fontWeight: 900,
              lineHeight: 1.15,
              textAlign: "center",
              letterSpacing: "-0.03em",
              marginBottom: 36,
            }}
          >
            Emergency vs. Routine <br />
            <span
              style={{
                background: "linear-gradient(135deg, #34D399, #06B6D4)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
              }}
            >
              Automatic Decision Tree
            </span>
          </h2>

          {/* 2-Branch Interactive Triage Display */}
          <div style={{ width: "100%", maxWidth: 920, display: "flex", flexDirection: "column", gap: 20 }}>
            {/* Branch A: YES (Emergency) */}
            <div
              style={{
                background: "radial-gradient(circle at 80% 50%, rgba(16, 185, 129, 0.15) 0%, rgba(15, 23, 42, 0.95) 100%)",
                border: "2px solid #10B981",
                borderRadius: 24,
                padding: "28px 36px",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                boxShadow: "0 20px 40px rgba(16, 185, 129, 0.25)",
              }}
            >
              <div>
                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                  <span style={{ background: "#10B981", color: "#05070B", padding: "4px 12px", borderRadius: 8, fontWeight: 900 }}>
                    CUSTOMER TEXTS: "YES"
                  </span>
                  <span style={{ fontSize: 20, fontWeight: 900, color: "#34D399" }}>🚨 ACTIVE EMERGENCY</span>
                </div>
                <div style={{ fontSize: 18, color: "#CBD5E1", marginTop: 8, fontWeight: 600 }}>
                  ➔ Customer receives <strong>instant shutoff instructions</strong>
                </div>
                <div style={{ fontSize: 18, color: "#34D399", marginTop: 4, fontWeight: 700 }}>
                  ➔ On-call technician receives <strong>priority dispatch alert</strong>
                </div>
              </div>
              <div style={{ textAlign: "right" }}>
                <div style={{ fontSize: 30, fontWeight: 900, color: "#34D399", fontFamily: "'JetBrains Mono', monospace" }}>
                  DISPATCHED
                </div>
                <div style={{ fontSize: 14, color: "#A7F3D0" }}>$2,500 Locked</div>
              </div>
            </div>

            {/* Branch B: NO (Routine) */}
            <div
              style={{
                background: "rgba(15, 23, 42, 0.8)",
                border: "1px solid rgba(255, 255, 255, 0.12)",
                borderRadius: 24,
                padding: "26px 36px",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
              }}
            >
              <div>
                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                  <span style={{ background: "rgba(255, 255, 255, 0.15)", color: "#FFF", padding: "4px 12px", borderRadius: 8, fontWeight: 900 }}>
                    CUSTOMER TEXTS: "NO"
                  </span>
                  <span style={{ fontSize: 20, fontWeight: 900, color: "#94A3B8" }}>📅 ROUTINE SERVICE</span>
                </div>
                <div style={{ fontSize: 17, color: "#94A3B8", marginTop: 8, fontWeight: 600 }}>
                  ➔ Auto-queued for <strong>Monday at 8:00 AM</strong> calendar
                </div>
                <div style={{ fontSize: 17, color: "#64748B", marginTop: 4 }}>
                  ➔ Zero phone ringing • Family dinner 100% protected
                </div>
              </div>
              <div style={{ textAlign: "right" }}>
                <div style={{ fontSize: 26, fontWeight: 900, color: "#94A3B8", fontFamily: "'JetBrains Mono', monospace" }}>
                  QUEUED
                </div>
                <div style={{ fontSize: 14, color: "#64748B" }}>Zero Distraction</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* SCENE 5: STEP 3 — ZERO HEADCOUNT & BIO CTA (Frames 1420 - 1925)            */}
      {/* ========================================================================= */}
      {frame >= 1410 && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            padding: "160px 70px 240px",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            opacity: interpolate(frame, [1415, 1435], [0, 1], { extrapolateRight: "clamp" }),
            transform: `scale(${interpolate(frame, [1420, 1440], [0.92, 1], { extrapolateRight: "clamp" })})`,
          }}
        >
          <div
            style={{
              background: "rgba(245, 158, 11, 0.15)",
              border: "1px solid rgba(245, 158, 11, 0.4)",
              borderRadius: 40,
              padding: "10px 24px",
              color: "#FBBF24",
              fontSize: 17,
              fontWeight: 800,
              letterSpacing: "0.12em",
              textTransform: "uppercase",
              marginBottom: 24,
            }}
          >
            STEP 03 • FINANCIAL CAPTURE
          </div>

          <h2
            style={{
              fontSize: 58,
              fontWeight: 900,
              lineHeight: 1.15,
              textAlign: "center",
              letterSpacing: "-0.03em",
              marginBottom: 36,
            }}
          >
            Capture $2,500 Jobs <br />
            Without A $3,000/Mo Call Center
          </h2>

          {/* Comparison Card (Call Center vs Automation) */}
          <div style={{ width: "100%", maxWidth: 920, display: "flex", gap: 24, marginBottom: 36 }}>
            <div
              style={{
                flex: 1,
                background: "rgba(244, 63, 94, 0.1)",
                border: "1px solid rgba(244, 63, 94, 0.35)",
                borderRadius: 24,
                padding: "30px",
                textAlign: "center",
              }}
            >
              <div style={{ fontSize: 16, fontWeight: 800, color: "#FB7185" }}>OUTSOURCED CALL CENTER</div>
              <div style={{ fontSize: 44, fontWeight: 900, color: "#F43F5E", margin: "8px 0", fontFamily: "'JetBrains Mono', monospace" }}>
                -$3,000/mo
              </div>
              <div style={{ fontSize: 15, color: "#94A3B8" }}>Untrained reps, dropped leads, costly overhead</div>
            </div>

            <div
              style={{
                flex: 1,
                background: "radial-gradient(circle, rgba(16, 185, 129, 0.15) 0%, rgba(15, 23, 42, 0.95) 100%)",
                border: "2px solid #10B981",
                borderRadius: 24,
                padding: "30px",
                textAlign: "center",
                boxShadow: "0 15px 35px rgba(16, 185, 129, 0.25)",
              }}
            >
              <div style={{ fontSize: 16, fontWeight: 800, color: "#34D399" }}>10-SECOND AUTOMATED TRIAGE</div>
              <div style={{ fontSize: 44, fontWeight: 900, color: "#34D399", margin: "8px 0", fontFamily: "'JetBrains Mono', monospace" }}>
                +$2,500 Won
              </div>
              <div style={{ fontSize: 15, color: "#A7F3D0" }}>Per emergency dispatch • Zero overhead</div>
            </div>
          </div>

          {/* Redesigned Wide CTA Card (Spacious, Zero Overlap) */}
          {(() => {
            const ctaPulse = Math.sin(frame / 14) * 3;
            return (
              <div
                style={{
                  width: 920,
                  background: "linear-gradient(135deg, #0284C7 0%, #1E40AF 100%)",
                  border: "2px solid rgba(56, 189, 248, 0.5)",
                  borderRadius: 30,
                  padding: "32px 42px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  gap: 32,
                  boxShadow: "0 25px 60px rgba(2, 132, 199, 0.4), 0 0 30px rgba(56, 189, 248, 0.2)",
                  transform: `scale(${1 + ctaPulse * 0.008})`,
                }}
              >
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div
                    style={{
                      fontSize: 34,
                      fontWeight: 900,
                      color: "#FFFFFF",
                      letterSpacing: "-0.02em",
                      lineHeight: 1.2,
                    }}
                  >
                    See The Exact 3-Step Workflow
                  </div>
                  <div
                    style={{
                      fontSize: 18,
                      color: "#BAE6FD",
                      fontWeight: 700,
                      marginTop: 6,
                      letterSpacing: "0.01em",
                    }}
                  >
                    Stop Letting After-Hours Calls Control Your Life
                  </div>
                </div>

                <div
                  style={{
                    flexShrink: 0,
                    background: "#FFFFFF",
                    color: "#0F172A",
                    padding: "20px 36px",
                    borderRadius: 22,
                    fontSize: 22,
                    fontWeight: 900,
                    letterSpacing: "0.04em",
                    boxShadow: "0 10px 30px rgba(0, 0, 0, 0.35)",
                    display: "flex",
                    alignItems: "center",
                    gap: 12,
                    whiteSpace: "nowrap",
                  }}
                >
                  TAP BIO LINK ➔
                </div>
              </div>
            );
          })()}
        </div>
      )}

      {/* SUBTITLE OVERLAY */}
      <div
        style={{
          position: "absolute",
          bottom: 70,
          left: 70,
          right: 70,
          display: "flex",
          justifyContent: "center",
          zIndex: 100,
        }}
      >
        {currentSub && (
          <div
            style={{
              background: "rgba(11, 17, 30, 0.94)",
              border: "1px solid rgba(255, 255, 255, 0.12)",
              backdropFilter: "blur(20px)",
              padding: "20px 44px",
              borderRadius: 30,
              maxWidth: 960,
              textAlign: "center",
              boxShadow: "0 15px 35px rgba(0, 0, 0, 0.6)",
            }}
          >
            <span
              style={{
                fontSize: 32,
                fontWeight: 800,
                color: "#F8FAFC",
                lineHeight: 1.35,
                letterSpacing: "-0.01em",
              }}
            >
              {currentSub.text}
            </span>
          </div>
        )}
      </div>
    </div>
  );
};
