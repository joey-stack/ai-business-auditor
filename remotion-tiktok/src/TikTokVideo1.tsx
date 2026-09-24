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

export const TikTokVideo1: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Subtle continuous camera drift & ambient particle flow (Jorge Canedo: Layered Motion)
  const camTiltX = Math.sin(frame / 48) * 1.8;
  const camTiltY = Math.cos(frame / 55) * 1.5;
  const orb1X = Math.sin(frame / 40) * 110;
  const orb1Y = Math.cos(frame / 45) * 90;
  const orb2X = Math.cos(frame / 50) * 120;
  const orb2Y = Math.sin(frame / 42) * 100;

  // Screen shake on heavy impact (e.g. frame 234: NOT A CHANCE stamp)
  const shakeFrame = frame - 234;
  const isShaking = shakeFrame >= 0 && shakeFrame < 14;
  const shakeOffset = isShaking
    ? Math.sin(shakeFrame * 2.8) * interpolate(shakeFrame, [0, 14], [18, 0], {
        extrapolateRight: "clamp",
      })
    : 0;

  // Real-time Top Progress Bar
  const totalFrames = 1465;
  const progressPct = Math.min(100, (frame / totalFrames) * 100);

  // Subtitle phrases mapped to spoken voice beats
  const subtitles = [
    { start: 0, end: 140, text: "If a homeowner has water pouring through their ceiling at 9:00 PM..." },
    { start: 140, end: 234, text: "Do you think they fill out an estimate form and wait 24 hours?" },
    { start: 234, end: 276, text: "NOT A CHANCE." },
    { start: 276, end: 495, text: "They pull out their phone, search Google Maps, and dial the first 3 contractors." },
    { start: 495, end: 645, text: "Whoever answers first, or texts back in 60 seconds..." },
    { start: 645, end: 795, text: "Wins the $3,500 emergency replacement job on the spot." },
    { start: 795, end: 990, text: "Right now, trade fleets leak over $14,500 every single month..." },
    { start: 990, end: 1155, text: "That is over $174,000 a year walked directly to competitors." },
    { start: 1155, end: 1335, text: "You don't need a $4,000 call center. You just need 10-second automated dispatch." },
    { start: 1335, end: 1465, text: "Tap the link in my bio to see the exact workflow and plug the leak." },
  ];

  const currentSub = subtitles.find((s) => frame >= s.start && frame < s.end);

  return (
    <div
      style={{
        width: 1080,
        height: 1920,
        backgroundColor: "#05070B",
        backgroundImage: `
          radial-gradient(circle at 50% 15%, rgba(14, 165, 233, 0.12) 0%, transparent 55%),
          radial-gradient(circle at 50% 85%, rgba(244, 63, 94, 0.10) 0%, transparent 60%),
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
      {/* 1. MASTER AUDIO & TACTILE SOUND DESIGN (Jorge Canedo Principle #1 & #5) */}
      <Audio src={staticFile("audio.mp3")} volume={1.0} />

      {/* SFX: Frame 0 entrance whoosh */}
      <Sequence from={0} durationInFrames={20}>
        <Audio src={staticFile("sfx/whoosh.wav")} volume={0.4} />
      </Sequence>

      {/* SFX: Frame 234 Heavy Impact Slam for "NOT A CHANCE" */}
      <Sequence from={232} durationInFrames={25}>
        <Audio src={staticFile("sfx/slam.wav")} volume={0.85} />
      </Sequence>

      {/* SFX: Frame 276 Whoosh into Google Maps */}
      <Sequence from={276} durationInFrames={20}>
        <Audio src={staticFile("sfx/whoosh.wav")} volume={0.45} />
      </Sequence>

      {/* SFX: Frame 330 Sonar Ping for Google Maps Search */}
      <Sequence from={330} durationInFrames={30}>
        <Audio src={staticFile("sfx/ping.wav")} volume={0.5} />
      </Sequence>

      {/* SFX: Frame 495 Whoosh into $3,500 Winner */}
      <Sequence from={495} durationInFrames={20}>
        <Audio src={staticFile("sfx/whoosh.wav")} volume={0.45} />
      </Sequence>

      {/* SFX: Frame 550 Cash Ding Chime for $3,500 Job Won */}
      <Sequence from={550} durationInFrames={35}>
        <Audio src={staticFile("sfx/ding.wav")} volume={0.8} />
      </Sequence>

      {/* SFX: Frame 795 Whoosh into Financial Leakage Reactor */}
      <Sequence from={795} durationInFrames={20}>
        <Audio src={staticFile("sfx/whoosh.wav")} volume={0.5} />
      </Sequence>

      {/* SFX: Frame 850 Slam for -$174,000 annual leak */}
      <Sequence from={850} durationInFrames={30}>
        <Audio src={staticFile("sfx/slam.wav")} volume={0.7} />
      </Sequence>

      {/* SFX: Frame 1155 Whoosh into 10-Second AI Solution */}
      <Sequence from={1155} durationInFrames={20}>
        <Audio src={staticFile("sfx/whoosh.wav")} volume={0.45} />
      </Sequence>

      {/* SFX: Frame 1220 Click/Pop on AI Dispatch Activation */}
      <Sequence from={1220} durationInFrames={15}>
        <Audio src={staticFile("sfx/click.wav")} volume={0.5} />
      </Sequence>

      {/* SFX: Frame 1340 Final Call-to-action chime */}
      <Sequence from={1340} durationInFrames={30}>
        <Audio src={staticFile("sfx/ping.wav")} volume={0.6} />
      </Sequence>

      {/* 2. TOP HIGH-PRECISION PROGRESS BAR */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: 10,
          background: "rgba(255, 255, 255, 0.08)",
          zIndex: 100,
        }}
      >
        <div
          style={{
            height: "100%",
            width: `${progressPct}%`,
            background: "linear-gradient(90deg, #38BDF8, #818CF8 50%, #F43F5E 100%)",
            boxShadow: "0 0 16px rgba(56, 189, 248, 0.8)",
          }}
        />
      </div>

      {/* 3. AMBIENT LIVING LIGHT ORBS */}
      <div
        style={{
          position: "absolute",
          width: 800,
          height: 800,
          borderRadius: "50%",
          background: "radial-gradient(circle, #0284C7 0%, transparent 70%)",
          filter: "blur(140px)",
          opacity: 0.22,
          top: -120,
          right: -100,
          transform: `translate(${orb1X}px, ${orb1Y}px)`,
          pointerEvents: "none",
        }}
      />
      <div
        style={{
          position: "absolute",
          width: 750,
          height: 750,
          borderRadius: "50%",
          background: "radial-gradient(circle, #F43F5E 0%, transparent 70%)",
          filter: "blur(140px)",
          opacity: 0.18,
          bottom: 100,
          left: -120,
          transform: `translate(${orb2X}px, ${orb2Y}px)`,
          pointerEvents: "none",
        }}
      />

      {/* 4. MAIN STAGE VIEWPORT */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: 1080,
          height: 1920,
          padding: "90px 70px 120px 70px",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          zIndex: 10,
        }}
      >
        {/* UPPER BANNER / BRAND TELEMETRY */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 12,
              background: "rgba(15, 23, 42, 0.85)",
              border: "1px solid rgba(56, 189, 248, 0.3)",
              padding: "10px 20px",
              borderRadius: 999,
              backdropFilter: "blur(16px)",
            }}
          >
            <div
              style={{
                width: 10,
                height: 10,
                borderRadius: "50%",
                background: "#10B981",
                boxShadow: "0 0 10px #10B981",
                animation: "pulse 2s infinite",
              }}
            />
            <span
              style={{
                fontSize: 16,
                fontWeight: 800,
                letterSpacing: 2,
                color: "#94A3B8",
                textTransform: "uppercase",
              }}
            >
              EXECUTIVE AUDIT INTEL • 01/25
            </span>
          </div>

          <div
            style={{
              background: "rgba(244, 63, 94, 0.15)",
              border: "1px solid rgba(244, 63, 94, 0.5)",
              padding: "10px 22px",
              borderRadius: 999,
              fontSize: 16,
              fontWeight: 800,
              color: "#FB7185",
              letterSpacing: 1.5,
              textTransform: "uppercase",
            }}
          >
            AFTER-HOURS CRISIS
          </div>
        </div>

        {/* INTERACTIVE SCENE CONTAINER (1400px height) */}
        <div style={{ position: "relative", width: "100%", height: 1380 }}>
          {/* SCENE 1: THE 9:00 PM BURST PIPE EMERGENCY (0 - 276 frames / 9.2s) */}
          <Sequence from={0} durationInFrames={276}>
            <Scene1BurstPipe />
          </Sequence>

          {/* SCENE 2: GOOGLE MAPS & THE 3 CONTRACTORS (276 - 495 frames / 7.3s) */}
          <Sequence from={276} durationInFrames={219}>
            <Scene2GoogleMapsRace />
          </Sequence>

          {/* SCENE 3: THE $3,500 VICTORY & SPEED-TO-LEAD CURVE (495 - 795 frames / 10s) */}
          <Sequence from={495} durationInFrames={300}>
            <Scene3SpeedToLeadCurve />
          </Sequence>

          {/* SCENE 4: THE $174,000 REVENUE LEAK REACTOR (795 - 1155 frames / 12s) */}
          <Sequence from={795} durationInFrames={360}>
            <Scene4RevenueLeakReactor />
          </Sequence>

          {/* SCENE 5: 10-SECOND AUTOMATED DISPATCH & CALL TO ACTION (1155 - 1465 frames / 10.3s) */}
          <Sequence from={1155} durationInFrames={310}>
            <Scene5AutomatedTriage />
          </Sequence>
        </div>

        {/* BOTTOM METRIC SUBTITLE CARD (Word-Synced Kinetic Highlight) */}
        <div style={{ width: "100%", display: "flex", justifyContent: "center", marginBottom: 15 }}>
          <div
            style={{
              background: "rgba(10, 15, 29, 0.94)",
              border: "1.5px solid rgba(56, 189, 248, 0.4)",
              borderRadius: 24,
              padding: "20px 36px",
              fontSize: 27,
              fontWeight: 800,
              color: "#F8FAFC",
              textAlign: "center",
              boxShadow:
                "0 20px 50px rgba(0, 0, 0, 0.6), 0 0 30px rgba(56, 189, 248, 0.15)",
              maxWidth: 960,
              lineHeight: 1.35,
              backdropFilter: "blur(20px)",
              transform: `scale(${1 + Math.sin(frame / 12) * 0.008})`,
            }}
          >
            {currentSub ? currentSub.text : ""}
          </div>
        </div>

        {/* FOOTER AUTHORITY SIGNATURE */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            borderTop: "1.5px solid rgba(255, 255, 255, 0.1)",
            paddingTop: 24,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
            <div
              style={{
                width: 66,
                height: 66,
                borderRadius: "50%",
                background: "linear-gradient(135deg, #0284C7 0%, #4F46E5 100%)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: 24,
                fontWeight: 900,
                color: "#FFFFFF",
                border: "2px solid rgba(255, 255, 255, 0.25)",
                boxShadow: "0 0 20px rgba(2, 132, 199, 0.5)",
              }}
            >
              JA
            </div>
            <div>
              <div style={{ fontSize: 26, fontWeight: 900, color: "#FFFFFF", letterSpacing: -0.5 }}>
                Joel Adawah Sani
              </div>
              <div style={{ fontSize: 17, color: "#94A3B8", fontWeight: 700, marginTop: 3 }}>
                Principal Business Systems Consultant
              </div>
            </div>
          </div>

          <div
            style={{
              background: "rgba(255, 255, 255, 0.06)",
              border: "1px solid rgba(255, 255, 255, 0.15)",
              padding: "10px 22px",
              borderRadius: 14,
              fontSize: 16,
              fontWeight: 800,
              color: "#E2E8F0",
              fontFamily: "'JetBrains Mono', monospace",
              letterSpacing: 1,
            }}
          >
            ⚡ SYSTEMS AUDIT
          </div>
        </div>
      </div>
    </div>
  );
};

/* =========================================================================
   SCENE 1: THE 9:00 PM BURST PIPE EMERGENCY
   Principles: Dynamic Scale, Anticipation, Overshoot, Secondary Ripples
   ========================================================================= */
const Scene1BurstPipe: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Entrance spring with anticipation
  const cardSpring = spring({
    frame,
    fps,
    config: { damping: 14, mass: 0.9, stiffness: 100 },
  });

  // Pulsing sonar waves for emergency alarm
  const wave1 = (frame * 3.5) % 180;
  const wave2 = ((frame + 60) * 3.5) % 180;

  // "NOT A CHANCE" Rubber Stamp at frame 234 (7.8s)
  const stampProgress = spring({
    frame: frame - 232,
    fps,
    config: { damping: 9, mass: 0.7, stiffness: 160 },
  });
  const stampScale = interpolate(stampProgress, [0, 1], [3.2, 1.0], {
    extrapolateRight: "clamp",
  });
  const stampOpacity = interpolate(stampProgress, [0, 0.2, 1], [0, 1, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        position: "relative",
      }}
    >
      {/* Background Water Pulse Rings */}
      <div
        style={{
          position: "absolute",
          top: "40%",
          left: "50%",
          width: wave1 * 4.5,
          height: wave1 * 4.5,
          borderRadius: "50%",
          border: "2px solid rgba(244, 63, 94, 0.4)",
          transform: "translate(-50%, -50%)",
          opacity: 1 - wave1 / 180,
          pointerEvents: "none",
        }}
      />
      <div
        style={{
          position: "absolute",
          top: "40%",
          left: "50%",
          width: wave2 * 4.5,
          height: wave2 * 4.5,
          borderRadius: "50%",
          border: "2px solid rgba(56, 189, 248, 0.3)",
          transform: "translate(-50%, -50%)",
          opacity: 1 - wave2 / 180,
          pointerEvents: "none",
        }}
      />

      {/* Hero Headline with Staggered Word Reveals */}
      <div style={{ textAlign: "center", marginBottom: 35, zIndex: 5 }}>
        <div
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 10,
            background: "rgba(244, 63, 94, 0.2)",
            border: "1.5px solid rgba(244, 63, 94, 0.7)",
            padding: "8px 24px",
            borderRadius: 999,
            fontSize: 20,
            fontWeight: 900,
            color: "#FB7185",
            letterSpacing: 2,
            textTransform: "uppercase",
            marginBottom: 20,
          }}
        >
          🚨 EMERGENCY DISPATCH DISASTER
        </div>
        <h1
          style={{
            fontSize: 66,
            fontWeight: 900,
            lineHeight: 1.12,
            letterSpacing: -2,
            color: "#FFFFFF",
            margin: 0,
          }}
        >
          Water Pouring Through <br />
          <span
            style={{
              background: "linear-gradient(90deg, #FB7185, #F43F5E 50%, #FDA4AF 100%)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              textShadow: "0 0 40px rgba(244, 63, 94, 0.5)",
            }}
          >
            The Ceiling at 9:00 PM.
          </span>
        </h1>
      </div>

      {/* 2.5D Realistic Smartphone Emergency Dispatch Mockup */}
      <div
        style={{
          width: 680,
          background: "linear-gradient(180deg, rgba(20, 29, 47, 0.95) 0%, rgba(10, 15, 29, 0.98) 100%)",
          border: "2px solid rgba(244, 63, 94, 0.4)",
          borderRadius: 40,
          padding: "36px 36px",
          boxShadow:
            "0 30px 80px rgba(0, 0, 0, 0.8), 0 0 50px rgba(244, 63, 94, 0.25)",
          transform: `scale(${cardSpring}) translateY(${interpolate(cardSpring, [0, 1], [60, 0])}px)`,
          position: "relative",
          backdropFilter: "blur(24px)",
          zIndex: 10,
        }}
      >
        {/* Phone Dynamic Header */}
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            borderBottom: "1px solid rgba(255, 255, 255, 0.1)",
            paddingBottom: 20,
            marginBottom: 24,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
            <div
              style={{
                width: 52,
                height: 52,
                borderRadius: 16,
                background: "rgba(244, 63, 94, 0.2)",
                border: "1.5px solid rgba(244, 63, 94, 0.6)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: 26,
              }}
            >
              🌊
            </div>
            <div>
              <div style={{ fontSize: 24, fontWeight: 900, color: "#FFF" }}>
                Severe Water Leak Detected
              </div>
              <div style={{ fontSize: 16, color: "#FB7185", fontWeight: 700 }}>
                Master Bedroom Ceiling • 21:00:14
              </div>
            </div>
          </div>
          <div
            style={{
              background: "rgba(244, 63, 94, 0.2)",
              color: "#FB7185",
              padding: "6px 16px",
              borderRadius: 8,
              fontSize: 14,
              fontWeight: 900,
            }}
          >
            CRITICAL
          </div>
        </div>

        {/* Live Audio Waveform Simulation */}
        <div
          style={{
            background: "rgba(0, 0, 0, 0.4)",
            borderRadius: 20,
            padding: "20px 24px",
            border: "1px solid rgba(255, 255, 255, 0.08)",
            marginBottom: 24,
          }}
        >
          <div style={{ fontSize: 15, fontWeight: 700, color: "#94A3B8", marginBottom: 10 }}>
            DISPATCH AUDIO STREAM
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: 6, height: 44 }}>
            {Array.from({ length: 28 }).map((_, i) => {
              const h = 8 + Math.abs(Math.sin((frame + i * 8) / 7)) * 32;
              return (
                <div
                  key={i}
                  style={{
                    flex: 1,
                    height: `${h}px`,
                    borderRadius: 4,
                    background: i % 2 === 0 ? "#F43F5E" : "#38BDF8",
                    opacity: 0.85,
                  }}
                />
              );
            })}
          </div>
        </div>

        {/* The Absurd Expectation Box */}
        <div
          style={{
            background: "rgba(255, 255, 255, 0.04)",
            border: "1px dashed rgba(255, 255, 255, 0.2)",
            borderRadius: 20,
            padding: "22px 24px",
            display: "flex",
            flexDirection: "column",
            gap: 8,
          }}
        >
          <div style={{ fontSize: 15, fontWeight: 800, color: "#E2E8F0" }}>
            WEBSITE ESTIMATE FORM:
          </div>
          <div style={{ fontSize: 18, color: "#94A3B8", fontStyle: "italic" }}>
            "Thank you for contacting us. Our office hours are 8am - 5pm. A representative will review your ticket within 24 to 48 hours."
          </div>
        </div>

        {/* GIANT "NOT A CHANCE" RUBBER STAMP (Hits at frame 234) */}
        {frame >= 230 && (
          <div
            style={{
              position: "absolute",
              top: "38%",
              left: "14%",
              transform: `scale(${stampScale}) rotate(-14deg)`,
              opacity: stampOpacity,
              background: "rgba(225, 29, 72, 0.95)",
              border: "8px solid #FFFFFF",
              borderRadius: 24,
              padding: "20px 48px",
              boxShadow: "0 0 60px rgba(225, 29, 72, 0.9), 0 20px 40px rgba(0,0,0,0.8)",
              zIndex: 50,
            }}
          >
            <div
              style={{
                fontSize: 64,
                fontWeight: 1000,
                color: "#FFFFFF",
                letterSpacing: 4,
                textAlign: "center",
                lineHeight: 1.0,
                textTransform: "uppercase",
              }}
            >
              NOT A CHANCE!
            </div>
            <div
              style={{
                fontSize: 20,
                fontWeight: 900,
                color: "#FECDD3",
                letterSpacing: 3,
                textAlign: "center",
                marginTop: 6,
              }}
            >
              THEY CALL THE NEXT NUMBER
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

/* =========================================================================
   SCENE 2: GOOGLE MAPS & THE 3 CONTRACTORS RACE
   Principles: Staggered Cascade, Match Cut Zoom, Competitor Visual Hierarchy
   ========================================================================= */
const Scene2GoogleMapsRace: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Search input typing effect
  const searchBarSpring = spring({ frame, fps, config: { damping: 14 } });
  const card1Spring = spring({ frame: frame - 15, fps, config: { damping: 13 } });
  const card2Spring = spring({ frame: frame - 30, fps, config: { damping: 13 } });
  const card3Spring = spring({ frame: frame - 45, fps, config: { damping: 13 } });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/* Scene Header */}
      <div style={{ textAlign: "center", marginBottom: 30 }}>
        <div
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 10,
            background: "rgba(56, 189, 248, 0.15)",
            border: "1.5px solid rgba(56, 189, 248, 0.6)",
            padding: "8px 24px",
            borderRadius: 999,
            fontSize: 18,
            fontWeight: 800,
            color: "#38BDF8",
            letterSpacing: 2,
            textTransform: "uppercase",
            marginBottom: 16,
          }}
        >
          📍 LIVE CUSTOMER DECISION BEHAVIOR
        </div>
        <h2
          style={{
            fontSize: 60,
            fontWeight: 900,
            lineHeight: 1.15,
            letterSpacing: -1.5,
            color: "#FFFFFF",
            margin: 0,
          }}
        >
          They Search Google Maps & <br />
          <span
            style={{
              background: "linear-gradient(90deg, #38BDF8, #818CF8)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
            }}
          >
            Dial The First 3 Contractors
          </span>
        </h2>
      </div>

      {/* Simulated Google Search Input */}
      <div
        style={{
          width: 780,
          background: "rgba(15, 23, 42, 0.9)",
          border: "2px solid rgba(56, 189, 248, 0.5)",
          borderRadius: 24,
          padding: "18px 28px",
          display: "flex",
          alignItems: "center",
          gap: 18,
          marginBottom: 28,
          boxShadow: "0 15px 40px rgba(0, 0, 0, 0.5)",
          transform: `scale(${searchBarSpring})`,
        }}
      >
        <span style={{ fontSize: 26 }}>🔍</span>
        <div style={{ fontSize: 24, fontWeight: 700, color: "#F8FAFC", fontFamily: "monospace" }}>
          emergency plumber near me 24/7
        </div>
        <div
          style={{
            marginLeft: "auto",
            background: "#0284C7",
            padding: "6px 16px",
            borderRadius: 12,
            fontSize: 15,
            fontWeight: 800,
          }}
        >
          SEARCH
        </div>
      </div>

      {/* 3 Contractors Cascading Cards */}
      <div style={{ width: 780, display: "flex", flexDirection: "column", gap: 16 }}>
        {/* Contractor #1: Missed / Voicemail */}
        <div
          style={{
            background: "rgba(30, 20, 30, 0.85)",
            border: "1.5px solid rgba(244, 63, 94, 0.4)",
            borderRadius: 22,
            padding: "22px 28px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            transform: `translateX(${interpolate(card1Spring, [0, 1], [-80, 0])}px)`,
            opacity: card1Spring,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
            <div
              style={{
                width: 48,
                height: 48,
                borderRadius: "50%",
                background: "rgba(244, 63, 94, 0.2)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: 22,
                color: "#F43F5E",
                fontWeight: 900,
              }}
            >
              1
            </div>
            <div>
              <div style={{ fontSize: 24, fontWeight: 800, color: "#FFFFFF" }}>Apex Plumbing Pros</div>
              <div style={{ fontSize: 16, color: "#94A3B8" }}>4.8 ★ (184 reviews) • Dialed 21:01</div>
            </div>
          </div>
          <div
            style={{
              background: "rgba(244, 63, 94, 0.25)",
              border: "1px solid rgba(244, 63, 94, 0.6)",
              padding: "8px 18px",
              borderRadius: 12,
              fontSize: 16,
              fontWeight: 900,
              color: "#FDA4AF",
            }}
          >
            ❌ VOICEMAIL (ABANDONED)
          </div>
        </div>

        {/* Contractor #2: Rings Out */}
        <div
          style={{
            background: "rgba(30, 20, 30, 0.85)",
            border: "1.5px solid rgba(244, 63, 94, 0.4)",
            borderRadius: 22,
            padding: "22px 28px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            transform: `translateX(${interpolate(card2Spring, [0, 1], [-80, 0])}px)`,
            opacity: card2Spring,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
            <div
              style={{
                width: 48,
                height: 48,
                borderRadius: "50%",
                background: "rgba(244, 63, 94, 0.2)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: 22,
                color: "#F43F5E",
                fontWeight: 900,
              }}
            >
              2
            </div>
            <div>
              <div style={{ fontSize: 24, fontWeight: 800, color: "#FFFFFF" }}>Rapid Drain & Rooter</div>
              <div style={{ fontSize: 16, color: "#94A3B8" }}>4.6 ★ (92 reviews) • Dialed 21:02</div>
            </div>
          </div>
          <div
            style={{
              background: "rgba(244, 63, 94, 0.25)",
              border: "1px solid rgba(244, 63, 94, 0.6)",
              padding: "8px 18px",
              borderRadius: 12,
              fontSize: 16,
              fontWeight: 900,
              color: "#FDA4AF",
            }}
          >
            ❌ NO ANSWER (RANG OUT)
          </div>
        </div>

        {/* Contractor #3: THE WINNER (Luminous Emerald Glow) */}
        <div
          style={{
            background: "linear-gradient(135deg, rgba(6, 78, 59, 0.9) 0%, rgba(6, 40, 35, 0.95) 100%)",
            border: "2.5px solid #10B981",
            borderRadius: 24,
            padding: "26px 32px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            transform: `scale(${card3Spring})`,
            boxShadow: "0 0 50px rgba(16, 185, 129, 0.4), 0 20px 40px rgba(0,0,0,0.6)",
            position: "relative",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
            <div
              style={{
                width: 54,
                height: 54,
                borderRadius: "50%",
                background: "#10B981",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: 26,
                color: "#064E3B",
                fontWeight: 900,
                boxShadow: "0 0 20px #10B981",
              }}
            >
              3
            </div>
            <div>
              <div style={{ fontSize: 26, fontWeight: 900, color: "#FFFFFF" }}>
                Metro Rooter & Emergency Services
              </div>
              <div style={{ fontSize: 17, color: "#A7F3D0", fontWeight: 700 }}>
                ⚡ AUTOMATED SMS + AI CALL DISPATCH IN 4 SECONDS
              </div>
            </div>
          </div>
          <div
            style={{
              background: "#10B981",
              color: "#064E3B",
              padding: "12px 24px",
              borderRadius: 14,
              fontSize: 20,
              fontWeight: 900,
              letterSpacing: 1,
              boxShadow: "0 0 25px rgba(16, 185, 129, 0.8)",
            }}
          >
            🏆 WINS JOB
          </div>
        </div>
      </div>
    </div>
  );
};

/* =========================================================================
   SCENE 3: THE $3,500 JOB & SPEED-TO-LEAD CURVE
   Principles: Dynamic Counting Ticker, Non-Linear Graph Animation, Visual Punch
   ========================================================================= */
const Scene3SpeedToLeadCurve: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Animated dollar counter from 0 to $3,500
  const counterSpring = spring({ frame, fps, config: { damping: 16, mass: 0.8 } });
  const dollarVal = Math.floor(interpolate(counterSpring, [0, 1], [0, 3500]));

  // Curve draw animation
  const curveDraw = interpolate(frame, [20, 120], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/* Huge Win Counter Card */}
      <div
        style={{
          width: 780,
          background: "linear-gradient(180deg, rgba(16, 185, 129, 0.15) 0%, rgba(6, 78, 59, 0.3) 100%)",
          border: "2px solid rgba(16, 185, 129, 0.6)",
          borderRadius: 36,
          padding: "36px 48px",
          textAlign: "center",
          boxShadow: "0 25px 60px rgba(0, 0, 0, 0.7), 0 0 50px rgba(16, 185, 129, 0.25)",
          marginBottom: 35,
          position: "relative",
        }}
      >
        <div
          style={{
            fontSize: 20,
            fontWeight: 800,
            letterSpacing: 2,
            color: "#A7F3D0",
            textTransform: "uppercase",
            marginBottom: 10,
          }}
        >
          REVENUE CAPTURED BY FASTEST RESPONDER
        </div>
        <div
          style={{
            fontSize: 98,
            fontWeight: 1000,
            color: "#34D399",
            letterSpacing: -3,
            lineHeight: 1.0,
            textShadow: "0 0 40px rgba(52, 211, 153, 0.6)",
          }}
        >
          ${dollarVal.toLocaleString()}+
        </div>
        <div style={{ fontSize: 20, color: "#F8FAFC", fontWeight: 700, marginTop: 12 }}>
          Average Emergency Replacement / Repipe Ticket Size
        </div>
      </div>

      {/* The Speed-to-Lead Decay Graph */}
      <div
        style={{
          width: 780,
          background: "rgba(15, 23, 42, 0.9)",
          border: "1.5px solid rgba(255, 255, 255, 0.12)",
          borderRadius: 30,
          padding: "32px 40px",
          boxShadow: "0 20px 50px rgba(0, 0, 0, 0.6)",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: 20,
          }}
        >
          <div style={{ fontSize: 22, fontWeight: 900, color: "#FFFFFF" }}>
            📉 Close Probability vs. Response Time
          </div>
          <div
            style={{
              background: "rgba(239, 68, 68, 0.2)",
              color: "#F87171",
              padding: "6px 14px",
              borderRadius: 8,
              fontSize: 14,
              fontWeight: 800,
            }}
          >
            HARVARD BUSINESS BENCHMARK
          </div>
        </div>

        {/* SVG Bezier Decay Curve */}
        <svg width="700" height="240" viewBox="0 0 700 240" style={{ overflow: "visible" }}>
          {/* Grid lines */}
          <line x1="0" y1="200" x2="700" y2="200" stroke="rgba(255,255,255,0.15)" strokeWidth="2" />
          <line x1="0" y1="50" x2="700" y2="50" stroke="rgba(255,255,255,0.08)" strokeDasharray="6 6" />

          {/* Labels */}
          <text x="10" y="40" fill="#34D399" fontSize="16" fontWeight="800">
            78% WIN RATE (&lt; 60 SECONDS)
          </text>
          <text x="500" y="190" fill="#F87171" fontSize="16" fontWeight="800">
            &lt; 4% WIN RATE (&gt; 30 MIN)
          </text>

          {/* Dynamic Decay Curve */}
          <path
            d="M 20 60 Q 150 70, 240 160 T 680 195"
            fill="none"
            stroke="url(#curveGradient)"
            strokeWidth="8"
            strokeLinecap="round"
            strokeDasharray={800}
            strokeDashoffset={800 * (1 - curveDraw)}
          />

          {/* Glowing Head Dot */}
          {curveDraw > 0.05 && (
            <circle
              cx={20 + curveDraw * 660}
              cy={60 + (1 - Math.exp(-curveDraw * 3)) * 135}
              r="10"
              fill="#F43F5E"
              stroke="#FFF"
              strokeWidth="3"
            />
          )}

          <defs>
            <linearGradient id="curveGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#10B981" />
              <stop offset="35%" stopColor="#F59E0B" />
              <stop offset="100%" stopColor="#EF4444" />
            </linearGradient>
          </defs>
        </svg>

        {/* Speed Stats Comparison Pills */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginTop: 24 }}>
          <div
            style={{
              background: "rgba(16, 185, 129, 0.15)",
              border: "1px solid rgba(16, 185, 129, 0.4)",
              borderRadius: 16,
              padding: "16px 20px",
            }}
          >
            <div style={{ fontSize: 28, fontWeight: 900, color: "#34D399" }}>Under 60s</div>
            <div style={{ fontSize: 15, color: "#94A3B8" }}>7x higher customer qualification rate</div>
          </div>
          <div
            style={{
              background: "rgba(239, 68, 68, 0.15)",
              border: "1px solid rgba(239, 68, 68, 0.4)",
              borderRadius: 16,
              padding: "16px 20px",
            }}
          >
            <div style={{ fontSize: 28, fontWeight: 900, color: "#F87171" }}>After 30m</div>
            <div style={{ fontSize: 15, color: "#94A3B8" }}>Job already secured by faster competitor</div>
          </div>
        </div>
      </div>
    </div>
  );
};

/* =========================================================================
   SCENE 4: THE $174,000 REVENUE LEAK REACTOR
   Principles: Heavy Weight, Warning Palette, Particle Bleed, Dollar Leakage
   ========================================================================= */
const Scene4RevenueLeakReactor: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Ticker for -$14,500/mo and -$174,000/yr
  const tickerSpring = spring({ frame, fps, config: { damping: 15, mass: 0.9 } });
  const monthlyLeak = Math.floor(interpolate(tickerSpring, [0, 1], [0, 14500]));
  const annualLeak = Math.floor(interpolate(tickerSpring, [0, 1], [0, 174000]));

  const alarmStrobe = Math.sin(frame / 6) > 0 ? 0.35 : 0.15;

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/* Alarm Banner */}
      <div
        style={{
          display: "inline-flex",
          alignItems: "center",
          gap: 12,
          background: `rgba(239, 68, 68, ${alarmStrobe})`,
          border: "2px solid #EF4444",
          padding: "10px 28px",
          borderRadius: 999,
          fontSize: 20,
          fontWeight: 900,
          color: "#FCA5A5",
          letterSpacing: 2,
          textTransform: "uppercase",
          marginBottom: 26,
        }}
      >
        ⚠️ UNNOTICED BALANCE SHEET DRAIN
      </div>

      {/* Giant Negative Financial Meter */}
      <div
        style={{
          width: 780,
          background: "linear-gradient(180deg, rgba(239, 68, 68, 0.2) 0%, rgba(127, 29, 29, 0.35) 100%)",
          border: "2.5px solid #EF4444",
          borderRadius: 36,
          padding: "40px 48px",
          textAlign: "center",
          boxShadow: "0 30px 80px rgba(0,0,0,0.8), 0 0 60px rgba(239, 68, 68, 0.35)",
          marginBottom: 30,
        }}
      >
        <div style={{ fontSize: 20, fontWeight: 800, color: "#FCA5A5", letterSpacing: 2 }}>
          ESTIMATED MONTHLY CASH LEAKAGE
        </div>
        <div
          style={{
            fontSize: 94,
            fontWeight: 1000,
            color: "#EF4444",
            letterSpacing: -3,
            lineHeight: 1.0,
            textShadow: "0 0 45px rgba(239, 68, 68, 0.7)",
          }}
        >
          -${monthlyLeak.toLocaleString()}{" "}
          <span style={{ fontSize: 40, fontWeight: 800, color: "#FCA5A5" }}>/ mo</span>
        </div>

        <div
          style={{
            marginTop: 20,
            paddingTop: 20,
            borderTop: "1px solid rgba(255,255,255,0.15)",
            display: "flex",
            justifyContent: "space-around",
            alignItems: "center",
          }}
        >
          <div>
            <div style={{ fontSize: 16, color: "#94A3B8", fontWeight: 700 }}>ANNUAL LOSS</div>
            <div style={{ fontSize: 44, fontWeight: 900, color: "#FFFFFF" }}>
              -${annualLeak.toLocaleString()}
            </div>
          </div>
          <div style={{ width: 1, height: 50, background: "rgba(255,255,255,0.15)" }} />
          <div>
            <div style={{ fontSize: 16, color: "#94A3B8", fontWeight: 700 }}>MISSED CALLS / MO</div>
            <div style={{ fontSize: 44, fontWeight: 900, color: "#FDA4AF" }}>42 Calls</div>
          </div>
        </div>
      </div>

      {/* The 3 Fatal Root Causes */}
      <div style={{ width: 780, display: "flex", flexDirection: "column", gap: 14 }}>
        <div
          style={{
            background: "rgba(15, 23, 42, 0.85)",
            border: "1px solid rgba(255, 255, 255, 0.1)",
            borderRadius: 18,
            padding: "18px 24px",
            display: "flex",
            alignItems: "center",
            gap: 16,
          }}
        >
          <span style={{ fontSize: 24 }}>📵</span>
          <div style={{ fontSize: 19, fontWeight: 700, color: "#E2E8F0" }}>
            Voicemails left after 5:00 PM are ignored until 8:30 AM next morning.
          </div>
        </div>

        <div
          style={{
            background: "rgba(15, 23, 42, 0.85)",
            border: "1px solid rgba(255, 255, 255, 0.1)",
            borderRadius: 18,
            padding: "18px 24px",
            display: "flex",
            alignItems: "center",
            gap: 16,
          }}
        >
          <span style={{ fontSize: 24 }}>💸</span>
          <div style={{ fontSize: 19, fontWeight: 700, color: "#E2E8F0" }}>
            Customer was in acute distress and booked the 2nd contractor on Google.
          </div>
        </div>

        <div
          style={{
            background: "rgba(15, 23, 42, 0.85)",
            border: "1px solid rgba(255, 255, 255, 0.1)",
            borderRadius: 18,
            padding: "18px 24px",
            display: "flex",
            alignItems: "center",
            gap: 16,
          }}
        >
          <span style={{ fontSize: 24 }}>📉</span>
          <div style={{ fontSize: 19, fontWeight: 700, color: "#E2E8F0" }}>
            Ad spend ($50+/click on Google LSA) burned with 0% dispatch conversion.
          </div>
        </div>
      </div>
    </div>
  );
};

/* =========================================================================
   SCENE 5: 10-SECOND AUTOMATED DISPATCH & CALL TO ACTION
   Principles: Linear / Stripe Architecture Node, High Contrast, Direct Clarity
   ========================================================================= */
const Scene5AutomatedTriage: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const nodeSpring = spring({ frame, fps, config: { damping: 14 } });
  const ctaSpring = spring({ frame: frame - 40, fps, config: { damping: 12 } });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/* Category Pill */}
      <div
        style={{
          display: "inline-flex",
          alignItems: "center",
          gap: 10,
          background: "rgba(56, 189, 248, 0.15)",
          border: "1.5px solid rgba(56, 189, 248, 0.6)",
          padding: "8px 24px",
          borderRadius: 999,
          fontSize: 18,
          fontWeight: 800,
          color: "#38BDF8",
          letterSpacing: 2,
          textTransform: "uppercase",
          marginBottom: 20,
        }}
      >
        ⚡ THE ZERO-LEAK INFRASTRUCTURE
      </div>

      <h2
        style={{
          fontSize: 58,
          fontWeight: 900,
          lineHeight: 1.15,
          letterSpacing: -1.5,
          color: "#FFFFFF",
          textAlign: "center",
          margin: "0 0 35px 0",
        }}
      >
        You Don't Need A $4,000 Call Center. <br />
        <span
          style={{
            background: "linear-gradient(90deg, #38BDF8, #818CF8 50%, #10B981 100%)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
          }}
        >
          Just 10-Second Automated Dispatch.
        </span>
      </h2>

      {/* The 3-Node Interactive Circuit */}
      <div
        style={{
          width: 920,
          background: "rgba(15, 23, 42, 0.95)",
          border: "2px solid rgba(56, 189, 248, 0.4)",
          borderRadius: 32,
          padding: "36px 44px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 35,
          boxShadow: "0 20px 60px rgba(0, 0, 0, 0.7), 0 0 40px rgba(56, 189, 248, 0.2)",
          transform: `scale(${nodeSpring})`,
        }}
      >
        {/* Node 1: Inbound Call */}
        <div style={{ textAlign: "center", flex: 1 }}>
          <div
            style={{
              width: 76,
              height: 76,
              borderRadius: 24,
              background: "rgba(56, 189, 248, 0.15)",
              border: "2px solid #38BDF8",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 34,
              margin: "0 auto 12px auto",
            }}
          >
            📞
          </div>
          <div style={{ fontSize: 20, fontWeight: 900, color: "#FFF" }}>Missed Call</div>
          <div style={{ fontSize: 15, color: "#94A3B8", marginTop: 2 }}>9:00 PM After-Hours</div>
        </div>

        {/* Pulse Arrow 1 */}
        <div style={{ fontSize: 32, color: "#38BDF8", padding: "0 10px" }}>➔</div>

        {/* Node 2: Instant AI Triage */}
        <div style={{ textAlign: "center", flex: 1.4 }}>
          <div
            style={{
              width: 88,
              height: 88,
              borderRadius: 28,
              background: "linear-gradient(135deg, #0284C7, #4F46E5)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 42,
              margin: "0 auto 12px auto",
              boxShadow: "0 0 30px rgba(2, 132, 199, 0.6)",
            }}
          >
            ⚡
          </div>
          <div style={{ fontSize: 22, fontWeight: 900, color: "#38BDF8" }}>
            10-Second AI Triage
          </div>
          <div style={{ fontSize: 15, color: "#C7D2FE", marginTop: 2 }}>Instant SMS + Priority Book</div>
        </div>

        {/* Pulse Arrow 2 */}
        <div style={{ fontSize: 32, color: "#10B981", padding: "0 10px" }}>➔</div>

        {/* Node 3: Booked Revenue */}
        <div style={{ textAlign: "center", flex: 1 }}>
          <div
            style={{
              width: 76,
              height: 76,
              borderRadius: 24,
              background: "rgba(16, 185, 129, 0.15)",
              border: "2px solid #10B981",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 34,
              margin: "0 auto 12px auto",
              boxShadow: "0 0 20px rgba(16, 185, 129, 0.4)",
            }}
          >
            💰
          </div>
          <div style={{ fontSize: 20, fontWeight: 900, color: "#10B981" }}>Job Locked</div>
          <div style={{ fontSize: 15, color: "#A7F3D0", marginTop: 2 }}>$3,500 Ticket Won</div>
        </div>
      </div>

      {/* High-Converting Call To Action Box (Spacious, Zero Overlap) */}
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
          transform: `scale(${ctaSpring})`,
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
            See The Exact Workflow
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
            Stop Bleeding After-Hours Leads to Competitors
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
    </div>
  );
};
