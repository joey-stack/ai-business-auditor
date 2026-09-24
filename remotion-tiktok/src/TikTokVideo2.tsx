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

export const TikTokVideo2: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 1. Subtle camera drift & ambient particle flow (Jorge Canedo: Layered Motion)
  const camTiltX = Math.sin(frame / 45) * 1.6;
  const camTiltY = Math.cos(frame / 50) * 1.4;
  const orb1X = Math.sin(frame / 38) * 100;
  const orb1Y = Math.cos(frame / 42) * 85;
  const orb2X = Math.cos(frame / 48) * 110;
  const orb2Y = Math.sin(frame / 40) * 95;

  // 2. Screen Shake on Heavy Impacts (e.g. 21x drop at frame 820, Leak stamp at frame 380)
  const shake1 = frame - 380;
  const shake2 = frame - 820;
  let shakeOffset = 0;
  if (shake1 >= 0 && shake1 < 12) {
    shakeOffset = Math.sin(shake1 * 3.0) * interpolate(shake1, [0, 12], [14, 0], { extrapolateRight: "clamp" });
  } else if (shake2 >= 0 && shake2 < 14) {
    shakeOffset = Math.sin(shake2 * 3.2) * interpolate(shake2, [0, 14], [18, 0], { extrapolateRight: "clamp" });
  }

  // 3. Real-time Top Progress Bar
  const totalFrames = 1520;
  const progressPct = Math.min(100, (frame / totalFrames) * 100);

  // 4. Subtitle phrases mapped to spoken voice beats
  const subtitles = [
    { start: 0, end: 210, text: "Whoever responds within 60 seconds captures 78% of local emergency service calls." },
    { start: 210, end: 390, text: "Look at this number right here: $14,500 every single month." },
    { start: 390, end: 630, text: "That is uncaptured revenue from customers who called this plumbing company and hung up." },
    { start: 630, end: 810, text: "Harvard Business Review tested lead response times across thousands of businesses." },
    { start: 810, end: 1050, text: "If you respond within 5 minutes vs 30 minutes, your qualification rate drops by 21 times." },
    { start: 1050, end: 1260, text: "In emergency trades like plumbing, HVAC, and roofing, the window is 60 seconds." },
    { start: 1260, end: 1380, text: "If your trucks aren't automated to reply instantly, you're buying leads for your competitors." },
    { start: 1380, end: 1520, text: "Comment 'AUDIT' below, and I'll send you our 4-pillar systems diagnostic checklist." },
  ];

  const currentSub = subtitles.find((s) => frame >= s.start && frame < s.end);

  return (
    <div
      style={{
        width: 1080,
        height: 1920,
        backgroundColor: "#05070B",
        backgroundImage: `
          radial-gradient(circle at 50% 12%, rgba(16, 185, 129, 0.12) 0%, transparent 55%),
          radial-gradient(circle at 50% 88%, rgba(244, 63, 94, 0.10) 0%, transparent 60%),
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
      {/* 1. MASTER AUDIO & SYNCHRONIZED TACTILE SFX */}
      <Audio src={staticFile("audio_v2.mp3")} volume={1.0} />

      {/* Frame 0 Entrance Whoosh */}
      <Sequence from={0} durationInFrames={20}>
        <Audio src={staticFile("sfx/whoosh.wav")} volume={0.4} />
      </Sequence>

      {/* Stopwatch Ticks during Hook */}
      {[25, 55, 85, 115, 145, 175].map((tickFrame, idx) => (
        <Sequence key={idx} from={tickFrame} durationInFrames={10}>
          <Audio src={staticFile("sfx/tick.wav")} volume={0.35} />
        </Sequence>
      ))}

      {/* Frame 130 78% Lock-in Ding */}
      <Sequence from={130} durationInFrames={30}>
        <Audio src={staticFile("sfx/ding.wav")} volume={0.7} />
      </Sequence>

      {/* Frame 210 Scene 2 Whoosh into Audit Dossier */}
      <Sequence from={210} durationInFrames={20}>
        <Audio src={staticFile("sfx/whoosh.wav")} volume={0.45} />
      </Sequence>

      {/* Frame 250 Alert ping for $14,500 leak */}
      <Sequence from={250} durationInFrames={25}>
        <Audio src={staticFile("sfx/alert.wav")} volume={0.6} />
      </Sequence>

      {/* Frame 380 Slam for Uncaptured Revenue Stamp */}
      <Sequence from={380} durationInFrames={25}>
        <Audio src={staticFile("sfx/slam.wav")} volume={0.8} />
      </Sequence>

      {/* Frame 630 Scene 3 Whoosh into Harvard Business Review */}
      <Sequence from={630} durationInFrames={20}>
        <Audio src={staticFile("sfx/whoosh.wav")} volume={0.45} />
      </Sequence>

      {/* Frame 680 Sonar Ping on HBR Chart */}
      <Sequence from={680} durationInFrames={30}>
        <Audio src={staticFile("sfx/ping.wav")} volume={0.5} />
      </Sequence>

      {/* Frame 820 Slam on the 21x Crash */}
      <Sequence from={820} durationInFrames={25}>
        <Audio src={staticFile("sfx/slam.wav")} volume={0.85} />
      </Sequence>

      {/* Frame 1050 Scene 4 Whoosh into Emergency Trades Radar */}
      <Sequence from={1050} durationInFrames={20}>
        <Audio src={staticFile("sfx/whoosh.wav")} volume={0.45} />
      </Sequence>

      {/* Frame 1130 Click for Instant 8s SMS Triage */}
      <Sequence from={1130} durationInFrames={15}>
        <Audio src={staticFile("sfx/click.wav")} volume={0.6} />
      </Sequence>

      {/* Frame 1380 Scene 5 Whoosh into Checklist CTA */}
      <Sequence from={1380} durationInFrames={20}>
        <Audio src={staticFile("sfx/whoosh.wav")} volume={0.5} />
      </Sequence>

      {/* Frame 1420 Ding on Checklist Ready */}
      <Sequence from={1420} durationInFrames={35}>
        <Audio src={staticFile("sfx/ding.wav")} volume={0.8} />
      </Sequence>

      {/* TOP PROGRESS BAR */}
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
            background: "linear-gradient(90deg, #10B981, #06B6D4, #F43F5E)",
            boxShadow: "0 0 15px #10B981",
          }}
        />
      </div>

      {/* AMBIENT LIVING ORBS */}
      <div
        style={{
          position: "absolute",
          width: 750,
          height: 750,
          borderRadius: "50%",
          background: "#059669",
          filter: "blur(140px)",
          opacity: 0.22,
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
          background: "#F43F5E",
          filter: "blur(140px)",
          opacity: 0.20,
          bottom: 100,
          left: -120,
          transform: `translate(${orb2X}px, ${orb2Y}px)`,
          pointerEvents: "none",
        }}
      />

      {/* TOP BRAND HEADER */}
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
              background: "linear-gradient(135deg, #10B981, #0284C7)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontWeight: 800,
              fontSize: 22,
              color: "#FFF",
              boxShadow: "0 4px 15px rgba(16, 185, 129, 0.4)",
            }}
          >
            ⏱️
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
            background: "rgba(16, 185, 129, 0.12)",
            border: "1px solid rgba(16, 185, 129, 0.3)",
            padding: "8px 18px",
            borderRadius: 30,
            fontSize: 14,
            fontWeight: 800,
            color: "#34D399",
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
              backgroundColor: "#10B981",
              boxShadow: "0 0 10px #10B981",
            }}
          />
          VIDEO #02 • GOOGLE MAPS
        </div>
      </div>

      {/* ========================================================================= */}
      {/* SCENE 1: THE 60-SECOND COUNTDOWN STOPWATCH HUD (Frames 0 - 210, 0s - 7s)   */}
      {/* ========================================================================= */}
      {frame < 225 && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            padding: "160px 70px 240px",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            opacity: interpolate(frame, [0, 15, 205, 220], [0, 1, 1, 0], { extrapolateRight: "clamp" }),
            transform: `scale(${interpolate(frame, [0, 20], [0.92, 1], { extrapolateRight: "clamp" })})`,
          }}
        >
          {/* Badge */}
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
              marginBottom: 28,
            }}
          >
            FIELD SERVICE DISPATCH PROTOCOL
          </div>

          {/* Main Hook Heading */}
          <h1
            style={{
              fontSize: 66,
              fontWeight: 900,
              lineHeight: 1.1,
              textAlign: "center",
              letterSpacing: "-0.03em",
              marginBottom: 40,
              maxWidth: 920,
            }}
          >
            The{" "}
            <span
              style={{
                background: "linear-gradient(135deg, #34D399, #06B6D4)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
              }}
            >
              60-Second Rule
            </span>{" "}
            on Google Maps
          </h1>

          {/* 2.5D Animated Stopwatch Component */}
          {(() => {
            const timeElapsed = Math.min(60, (frame / 200) * 60);
            const secondsLeft = Math.max(0, 60 - Math.floor(timeElapsed));
            const ms = Math.floor((1 - (timeElapsed % 1)) * 99);
            const circleDash = 2 * Math.PI * 180;
            const dashOffset = circleDash * (timeElapsed / 60);

            return (
              <div
                style={{
                  position: "relative",
                  width: 440,
                  height: 440,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  marginBottom: 40,
                }}
              >
                {/* SVG Radial Gauge */}
                <svg width="440" height="440" style={{ transform: "rotate(-90deg)" }}>
                  <circle
                    cx="220"
                    cy="220"
                    r="180"
                    fill="none"
                    stroke="rgba(255, 255, 255, 0.06)"
                    strokeWidth="18"
                  />
                  <circle
                    cx="220"
                    cy="220"
                    r="180"
                    fill="none"
                    stroke="#10B981"
                    strokeWidth="18"
                    strokeDasharray={circleDash}
                    strokeDashoffset={dashOffset}
                    strokeLinecap="round"
                    style={{
                      filter: "drop-shadow(0 0 16px rgba(16, 185, 129, 0.8))",
                    }}
                  />
                </svg>

                {/* Digital Center Readout */}
                <div
                  style={{
                    position: "absolute",
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                >
                  <div
                    style={{
                      fontFamily: "'JetBrains Mono', monospace",
                      fontSize: 84,
                      fontWeight: 900,
                      letterSpacing: "-0.04em",
                      color: secondsLeft < 15 ? "#F43F5E" : "#F8FAFC",
                    }}
                  >
                    00:{secondsLeft.toString().padStart(2, "0")}
                  </div>
                  <div
                    style={{
                      fontSize: 18,
                      fontWeight: 700,
                      color: "#94A3B8",
                      letterSpacing: "0.15em",
                      textTransform: "uppercase",
                      marginTop: 4,
                    }}
                  >
                    RESPONSE LATENCY
                  </div>
                </div>
              </div>
            );
          })()}

          {/* 78% Win Rate Stat Card */}
          {(() => {
            const cardPop = spring({ frame: frame - 110, fps, config: { stiffness: 180, damping: 14 } });
            return (
              <div
                style={{
                  width: "100%",
                  maxWidth: 900,
                  background: "rgba(15, 23, 42, 0.85)",
                  border: "1px solid rgba(16, 185, 129, 0.4)",
                  borderRadius: 24,
                  padding: "26px 36px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  boxShadow: "0 20px 40px rgba(0, 0, 0, 0.6)",
                  transform: `scale(${interpolate(cardPop, [0, 1], [0.8, 1])}) translateY(${interpolate(cardPop, [0, 1], [40, 0])}px)`,
                  opacity: interpolate(cardPop, [0, 1], [0, 1]),
                }}
              >
                <div>
                  <div style={{ fontSize: 16, fontWeight: 700, color: "#34D399", letterSpacing: "0.08em" }}>
                    FIRST-RESPONDER ADVANTAGE
                  </div>
                  <div style={{ fontSize: 28, fontWeight: 800, marginTop: 4 }}>
                    Captures Emergency Service Calls
                  </div>
                </div>
                <div
                  style={{
                    fontSize: 64,
                    fontWeight: 900,
                    color: "#34D399",
                    fontFamily: "'JetBrains Mono', monospace",
                    textShadow: "0 0 25px rgba(52, 211, 153, 0.6)",
                  }}
                >
                  78%
                </div>
              </div>
            );
          })()}
        </div>
      )}

      {/* ========================================================================= */}
      {/* SCENE 2: THE AUDIT DOSSIER & $14,500 LEAKAGE (Frames 210 - 640, 7s - 21s) */}
      {/* ========================================================================= */}
      {frame >= 200 && frame < 645 && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            padding: "160px 70px 240px",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            opacity: interpolate(frame, [205, 225, 625, 640], [0, 1, 1, 0], { extrapolateRight: "clamp" }),
            transform: `scale(${interpolate(frame, [210, 230], [0.92, 1], { extrapolateRight: "clamp" })})`,
          }}
        >
          <div
            style={{
              background: "rgba(244, 63, 94, 0.15)",
              border: "1px solid rgba(244, 63, 94, 0.4)",
              borderRadius: 40,
              padding: "10px 24px",
              color: "#FB7185",
              fontSize: 17,
              fontWeight: 800,
              letterSpacing: "0.12em",
              textTransform: "uppercase",
              marginBottom: 24,
            }}
          >
            REAL CLIENT SYSTEMS AUDIT
          </div>

          <h2
            style={{
              fontSize: 56,
              fontWeight: 900,
              lineHeight: 1.15,
              textAlign: "center",
              letterSpacing: "-0.03em",
              marginBottom: 36,
            }}
          >
            This Isn't Ad Spend. <br />
            It's{" "}
            <span
              style={{
                background: "linear-gradient(135deg, #FB7185, #F43F5E)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
              }}
            >
              Uncaptured Revenue.
            </span>
          </h2>

          {/* 2.5D Audit Dossier Card */}
          {(() => {
            const cardSpring = spring({ frame: frame - 220, fps, config: { stiffness: 160, damping: 16 } });
            const stampSpring = spring({ frame: frame - 375, fps, config: { stiffness: 260, damping: 10, mass: 1.2 } });

            return (
              <div
                style={{
                  position: "relative",
                  width: "100%",
                  maxWidth: 920,
                  background: "linear-gradient(145deg, #0B111E, #070B14)",
                  border: "1px solid rgba(255, 255, 255, 0.1)",
                  borderRadius: 28,
                  padding: "40px 44px",
                  boxShadow: "0 30px 60px rgba(0, 0, 0, 0.7)",
                  transform: `scale(${interpolate(cardSpring, [0, 1], [0.85, 1])}) translateY(${interpolate(cardSpring, [0, 1], [50, 0])}px)`,
                }}
              >
                {/* Dossier Header */}
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    borderBottom: "1px solid rgba(255, 255, 255, 0.08)",
                    paddingBottom: 22,
                    marginBottom: 30,
                  }}
                >
                  <div>
                    <div style={{ fontSize: 15, color: "#94A3B8", fontWeight: 700, letterSpacing: "0.1em" }}>
                      CLIENT SYSTEM AUDIT • PAGE 2
                    </div>
                    <div style={{ fontSize: 26, fontWeight: 900, marginTop: 4 }}>
                      Apex Home Services ($3.8M Fleet)
                    </div>
                  </div>
                  <div
                    style={{
                      background: "rgba(244, 63, 94, 0.15)",
                      border: "1px solid rgba(244, 63, 94, 0.4)",
                      padding: "8px 16px",
                      borderRadius: 12,
                      fontSize: 14,
                      fontWeight: 800,
                      color: "#FB7185",
                    }}
                  >
                    🚨 CRITICAL LEAK DETECTED
                  </div>
                </div>

                {/* Audit Metrics Breakdown */}
                <div style={{ display: "flex", gap: 24, marginBottom: 30 }}>
                  <div
                    style={{
                      flex: 1,
                      background: "rgba(255, 255, 255, 0.03)",
                      border: "1px solid rgba(255, 255, 255, 0.06)",
                      borderRadius: 18,
                      padding: "24px",
                    }}
                  >
                    <div style={{ fontSize: 14, color: "#94A3B8", fontWeight: 700 }}>MONTHLY INBOUND CALLS</div>
                    <div style={{ fontSize: 36, fontWeight: 900, marginTop: 6, fontFamily: "'JetBrains Mono', monospace" }}>
                      184 Calls
                    </div>
                    <div style={{ fontSize: 13, color: "#64748B", marginTop: 4 }}>Google Map Pack & Ads</div>
                  </div>

                  <div
                    style={{
                      flex: 1,
                      background: "rgba(244, 63, 94, 0.08)",
                      border: "1px solid rgba(244, 63, 94, 0.3)",
                      borderRadius: 18,
                      padding: "24px",
                    }}
                  >
                    <div style={{ fontSize: 14, color: "#FB7185", fontWeight: 700 }}>UNASSISTED AFTER-HOURS</div>
                    <div
                      style={{
                        fontSize: 36,
                        fontWeight: 900,
                        marginTop: 6,
                        color: "#FB7185",
                        fontFamily: "'JetBrains Mono', monospace",
                      }}
                    >
                      32 Calls (17.4%)
                    </div>
                    <div style={{ fontSize: 13, color: "#F43F5E", marginTop: 4 }}>Sent directly to Voicemail</div>
                  </div>
                </div>

                {/* Big Leakage Highlight Box */}
                <div
                  style={{
                    background: "radial-gradient(circle at 50% 50%, rgba(244, 63, 94, 0.15) 0%, rgba(15, 23, 42, 0.8) 100%)",
                    border: "2px solid #F43F5E",
                    borderRadius: 22,
                    padding: "32px",
                    textAlign: "center",
                    position: "relative",
                    overflow: "hidden",
                  }}
                >
                  <div style={{ fontSize: 16, fontWeight: 800, color: "#FB7185", letterSpacing: "0.15em" }}>
                    CALCULATED MONTHLY REVENUE LEAKAGE
                  </div>
                  <div
                    style={{
                      fontSize: 78,
                      fontWeight: 900,
                      color: "#F8FAFC",
                      fontFamily: "'JetBrains Mono', monospace",
                      margin: "12px 0 6px",
                      textShadow: "0 0 35px rgba(244, 63, 94, 0.6)",
                    }}
                  >
                    -$14,500
                    <span style={{ fontSize: 32, color: "#FB7185", fontWeight: 700 }}> / month</span>
                  </div>
                  <div style={{ fontSize: 18, color: "#CBD5E1", fontWeight: 600 }}>
                    Equivalent to <strong style={{ color: "#FFF" }}>$174,000 / year</strong> walked directly to competing trade fleets
                  </div>

                  {/* Stamp Overlay: UNCAPTURED REVENUE */}
                  {frame >= 375 && (
                    <div
                      style={{
                        position: "absolute",
                        top: "50%",
                        left: "50%",
                        transform: `translate(-50%, -50%) rotate(-12deg) scale(${interpolate(stampSpring, [0, 1], [2.2, 1])})`,
                        background: "rgba(225, 29, 72, 0.92)",
                        border: "5px solid #FFE4E6",
                        borderRadius: 16,
                        padding: "16px 36px",
                        color: "#FFF",
                        fontSize: 34,
                        fontWeight: 900,
                        letterSpacing: "0.15em",
                        boxShadow: "0 20px 50px rgba(0, 0, 0, 0.8)",
                        pointerEvents: "none",
                        whiteSpace: "nowrap",
                      }}
                    >
                      UNCAPTURED REVENUE ❌
                    </div>
                  )}
                </div>
              </div>
            );
          })()}
        </div>
      )}

      {/* ========================================================================= */}
      {/* SCENE 3: THE HARVARD BUSINESS REVIEW 21X CLIFF (Frames 630 - 1060, 21s-35s) */}
      {/* ========================================================================= */}
      {frame >= 620 && frame < 1065 && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            padding: "160px 70px 240px",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            opacity: interpolate(frame, [625, 645, 1045, 1060], [0, 1, 1, 0], { extrapolateRight: "clamp" }),
            transform: `scale(${interpolate(frame, [630, 650], [0.92, 1], { extrapolateRight: "clamp" })})`,
          }}
        >
          <div
            style={{
              background: "rgba(59, 130, 246, 0.15)",
              border: "1px solid rgba(59, 130, 246, 0.4)",
              borderRadius: 40,
              padding: "10px 24px",
              color: "#60A5FA",
              fontSize: 17,
              fontWeight: 800,
              letterSpacing: "0.12em",
              textTransform: "uppercase",
              marginBottom: 24,
            }}
          >
            EMPIRICAL DATA BENCHMARK
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
            Harvard Business Review: <br />
            The{" "}
            <span
              style={{
                background: "linear-gradient(135deg, #F43F5E, #FB7185)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
              }}
            >
              21× Conversion Drop
            </span>
          </h2>

          {/* Dual Bar Chart Comparison Container */}
          {(() => {
            const chartSpring = spring({ frame: frame - 640, fps, config: { stiffness: 170, damping: 15 } });
            const dropSpring = spring({ frame: frame - 810, fps, config: { stiffness: 220, damping: 14 } });

            // Bar heights
            const bar1Height = interpolate(chartSpring, [0, 1], [0, 360]);
            // Drops dramatically on frame 810
            const bar2Height = interpolate(dropSpring, [0, 1], [360, 24]);

            return (
              <div
                style={{
                  width: "100%",
                  maxWidth: 920,
                  background: "linear-gradient(145deg, #0B111E, #070B14)",
                  border: "1px solid rgba(255, 255, 255, 0.08)",
                  borderRadius: 28,
                  padding: "44px",
                  boxShadow: "0 30px 60px rgba(0, 0, 0, 0.7)",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                }}
              >
                {/* Visual Chart Comparison */}
                <div
                  style={{
                    width: "100%",
                    display: "flex",
                    justifyContent: "space-around",
                    alignItems: "flex-end",
                    height: 400,
                    borderBottom: "2px solid rgba(255, 255, 255, 0.12)",
                    paddingBottom: 20,
                    position: "relative",
                  }}
                >
                  {/* Left Column: 5 Minutes */}
                  <div style={{ display: "flex", flexDirection: "column", alignItems: "center", width: 260 }}>
                    <div style={{ fontSize: 24, fontWeight: 900, color: "#34D399", marginBottom: 12 }}>
                      100% BASELINE
                    </div>
                    <div
                      style={{
                        width: 180,
                        height: bar1Height,
                        background: "linear-gradient(180deg, #10B981 0%, #047857 100%)",
                        borderRadius: "16px 16px 4px 4px",
                        boxShadow: "0 0 25px rgba(16, 185, 129, 0.4)",
                      }}
                    />
                    <div style={{ marginTop: 18, fontSize: 22, fontWeight: 800 }}>⚡ Under 5 Mins</div>
                    <div style={{ fontSize: 14, color: "#94A3B8" }}>High Lead Qualification</div>
                  </div>

                  {/* Middle Arrow / Metric */}
                  <div
                    style={{
                      display: "flex",
                      flexDirection: "column",
                      alignItems: "center",
                      justifyContent: "center",
                      paddingBottom: 80,
                      opacity: interpolate(dropSpring, [0, 1], [0, 1]),
                      transform: `scale(${interpolate(dropSpring, [0, 1], [0.5, 1])})`,
                    }}
                  >
                    <div
                      style={{
                        background: "rgba(244, 63, 94, 0.2)",
                        border: "2px solid #F43F5E",
                        borderRadius: 20,
                        padding: "16px 28px",
                        textAlign: "center",
                        boxShadow: "0 0 35px rgba(244, 63, 94, 0.5)",
                      }}
                    >
                      <div
                        style={{
                          fontSize: 54,
                          fontWeight: 900,
                          color: "#F43F5E",
                          fontFamily: "'JetBrains Mono', monospace",
                        }}
                      >
                        21× DROP
                      </div>
                      <div style={{ fontSize: 14, fontWeight: 700, color: "#FB7185", letterSpacing: "0.08em" }}>
                        QUALIFICATION COLLAPSE
                      </div>
                    </div>
                  </div>

                  {/* Right Column: 30 Minutes */}
                  <div style={{ display: "flex", flexDirection: "column", alignItems: "center", width: 260 }}>
                    <div
                      style={{
                        fontSize: 24,
                        fontWeight: 900,
                        color: "#F43F5E",
                        marginBottom: 12,
                        opacity: interpolate(dropSpring, [0, 1], [0, 1]),
                      }}
                    >
                      4.7% CONVERSION
                    </div>
                    <div
                      style={{
                        width: 180,
                        height: bar2Height,
                        background: "linear-gradient(180deg, #F43F5E 0%, #BE123C 100%)",
                        borderRadius: "16px 16px 4px 4px",
                        boxShadow: "0 0 25px rgba(244, 63, 94, 0.4)",
                      }}
                    />
                    <div style={{ marginTop: 18, fontSize: 22, fontWeight: 800 }}>⏳ After 30 Mins</div>
                    <div style={{ fontSize: 14, color: "#94A3B8" }}>Lead Almost Always Lost</div>
                  </div>
                </div>

                <div
                  style={{
                    marginTop: 28,
                    fontSize: 20,
                    fontWeight: 700,
                    color: "#94A3B8",
                    textAlign: "center",
                  }}
                >
                  Source: <em>Harvard Business Review Study across 2,241 U.S. Companies</em>
                </div>
              </div>
            );
          })()}
        </div>
      )}

      {/* ========================================================================= */}
      {/* SCENE 4: THE 60-SEC EMERGENCY THRESHOLD (Frames 1050 - 1390, 35s - 46s)    */}
      {/* ========================================================================= */}
      {frame >= 1040 && frame < 1395 && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            padding: "160px 70px 240px",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            opacity: interpolate(frame, [1045, 1065, 1375, 1390], [0, 1, 1, 0], { extrapolateRight: "clamp" }),
            transform: `scale(${interpolate(frame, [1050, 1070], [0.92, 1], { extrapolateRight: "clamp" })})`,
          }}
        >
          <div
            style={{
              background: "rgba(234, 179, 8, 0.15)",
              border: "1px solid rgba(234, 179, 8, 0.4)",
              borderRadius: 40,
              padding: "10px 24px",
              color: "#FACC15",
              fontSize: 17,
              fontWeight: 800,
              letterSpacing: "0.12em",
              textTransform: "uppercase",
              marginBottom: 24,
            }}
          >
            HOME SERVICES REALITY
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
            In Trades, The Window Isn't 5 Mins. <br />
            It's{" "}
            <span
              style={{
                background: "linear-gradient(135deg, #10B981, #06B6D4)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
              }}
            >
              60 Seconds.
            </span>
          </h2>

          {/* Trade Fleet Comparison Cards */}
          <div style={{ width: "100%", maxWidth: 920, display: "flex", flexDirection: "column", gap: 24 }}>
            {/* Card 1: The Manual Contractor (Buying Competitor Leads) */}
            <div
              style={{
                background: "rgba(15, 23, 42, 0.8)",
                border: "1px solid rgba(244, 63, 94, 0.4)",
                borderRadius: 22,
                padding: "26px 32px",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                boxShadow: "0 15px 35px rgba(0, 0, 0, 0.5)",
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
                <div
                  style={{
                    width: 64,
                    height: 64,
                    borderRadius: 18,
                    background: "rgba(244, 63, 94, 0.15)",
                    border: "1px solid rgba(244, 63, 94, 0.3)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 30,
                  }}
                >
                  ❌
                </div>
                <div>
                  <div style={{ fontSize: 24, fontWeight: 800 }}>The Manual Fleet (Voicemail)</div>
                  <div style={{ fontSize: 16, color: "#94A3B8", marginTop: 4 }}>
                    Customer rings out ➔ Dials next Google Maps contractor
                  </div>
                </div>
              </div>
              <div style={{ textAlign: "right" }}>
                <div style={{ fontSize: 26, fontWeight: 900, color: "#F43F5E", fontFamily: "'JetBrains Mono', monospace" }}>
                  LEAD LOST
                </div>
                <div style={{ fontSize: 14, color: "#FB7185", fontWeight: 700 }}>-$3,500 Ticket</div>
              </div>
            </div>

            {/* Card 2: The Automated Fleet (Instant 8-Second Triage) */}
            <div
              style={{
                background: "radial-gradient(circle at 80% 50%, rgba(16, 185, 129, 0.15) 0%, rgba(15, 23, 42, 0.95) 100%)",
                border: "2px solid #10B981",
                borderRadius: 22,
                padding: "28px 32px",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                boxShadow: "0 20px 45px rgba(16, 185, 129, 0.25)",
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
                <div
                  style={{
                    width: 64,
                    height: 64,
                    borderRadius: 18,
                    background: "rgba(16, 185, 129, 0.2)",
                    border: "1px solid #10B981",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 30,
                  }}
                >
                  ⚡
                </div>
                <div>
                  <div style={{ fontSize: 24, fontWeight: 800, color: "#F8FAFC" }}>
                    Automated Fleet (Instant Triage)
                  </div>
                  <div style={{ fontSize: 16, color: "#34D399", marginTop: 4, fontWeight: 600 }}>
                    Missed Call ➔ 8-Second SMS Triage ➔ Booked Dispatch
                  </div>
                </div>
              </div>
              <div style={{ textAlign: "right" }}>
                <div style={{ fontSize: 28, fontWeight: 900, color: "#34D399", fontFamily: "'JetBrains Mono', monospace" }}>
                  JOB WON ✅
                </div>
                <div style={{ fontSize: 14, color: "#A7F3D0", fontWeight: 700 }}>Locked in 60s</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* SCENE 5: CAPSTONE OFFER & DIAGNOSTIC CHECKLIST CTA (Frames 1380 - 1520)    */}
      {/* ========================================================================= */}
      {frame >= 1370 && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            padding: "160px 70px 240px",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            opacity: interpolate(frame, [1375, 1395], [0, 1], { extrapolateRight: "clamp" }),
            transform: `scale(${interpolate(frame, [1380, 1400], [0.92, 1], { extrapolateRight: "clamp" })})`,
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
            ACTIONABLE NEXT STEP
          </div>

          <h2
            style={{
              fontSize: 62,
              fontWeight: 900,
              lineHeight: 1.15,
              textAlign: "center",
              letterSpacing: "-0.03em",
              marginBottom: 36,
            }}
          >
            Audit Your Trade Fleet <br />
            In 15 Minutes
          </h2>

          {/* 3D Floating Checklist Card */}
          {(() => {
            const checkSpring = spring({ frame: frame - 1390, fps, config: { stiffness: 180, damping: 14 } });

            return (
              <div
                style={{
                  width: "100%",
                  maxWidth: 900,
                  background: "linear-gradient(145deg, #0F172A, #070B14)",
                  border: "1px solid rgba(255, 255, 255, 0.1)",
                  borderRadius: 28,
                  padding: "40px 48px",
                  boxShadow: "0 30px 60px rgba(0, 0, 0, 0.7)",
                  transform: `scale(${interpolate(checkSpring, [0, 1], [0.85, 1])}) translateY(${interpolate(checkSpring, [0, 1], [40, 0])}px)`,
                  marginBottom: 36,
                }}
              >
                <div style={{ fontSize: 18, fontWeight: 800, color: "#34D399", letterSpacing: "0.08em", marginBottom: 20 }}>
                  THE 4-PILLAR SYSTEMS DIAGNOSTIC CHECKLIST
                </div>

                <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
                  {[
                    "1. After-Hours Speed-to-Lead & 60s SMS Triage",
                    "2. Choice Architecture & Good-Better-Best Quoting",
                    "3. Dual-Trade Cross-Sell Routing (Water Heater Checks)",
                    "4. Google Map Pack Latency & Automated Review Engine",
                  ].map((item, idx) => (
                    <div
                      key={idx}
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: 16,
                        fontSize: 22,
                        fontWeight: 700,
                        color: "#E2E8F0",
                      }}
                    >
                      <div
                        style={{
                          width: 32,
                          height: 32,
                          borderRadius: 10,
                          background: "#10B981",
                          color: "#FFF",
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "center",
                          fontSize: 18,
                          fontWeight: 900,
                        }}
                      >
                        ✓
                      </div>
                      {item}
                    </div>
                  ))}
                </div>
              </div>
            );
          })()}

          {/* Comment "AUDIT" Action Callout Button */}
          {(() => {
            const btnPulse = Math.sin(frame / 12) * 4;
            return (
              <div
                style={{
                  background: "linear-gradient(135deg, #10B981, #0284C7)",
                  padding: "24px 60px",
                  borderRadius: 50,
                  fontSize: 32,
                  fontWeight: 900,
                  letterSpacing: "0.05em",
                  color: "#FFF",
                  boxShadow: "0 10px 40px rgba(16, 185, 129, 0.6)",
                  display: "flex",
                  alignItems: "center",
                  gap: 16,
                  transform: `scale(${1 + btnPulse * 0.01})`,
                }}
              >
                💬 COMMENT "AUDIT" BELOW
              </div>
            );
          })()}
        </div>
      )}

      {/* ========================================================================= */}
      {/* BOTTOM SUBTITLE OVERLAY                                                   */}
      {/* ========================================================================= */}
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
