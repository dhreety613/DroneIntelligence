import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

export default function Welcome() {
  const nav = useNavigate();
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    setIsLoaded(true);
  }, []);

  // --- Theme Constants ---
  const NEON_PURPLE = "#bc13fe";
  const LAVENDER_GRADIENT = "linear-gradient(90deg, #ffffff 0%, #d8b4fe 50%, #bc13fe 100%)";
  
  const animations = `
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

    @keyframes backdropPulse {
      0% { background: radial-gradient(circle at 50% 50%, #1a022a 0%, #000 100%); }
      100% { background: radial-gradient(circle at 50% 50%, #0d0115 0%, #000 100%); }
    }

    @keyframes titleReveal {
      0% { opacity: 0; transform: translateY(40px) scale(0.9); filter: blur(20px); }
      100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0px); }
    }

    @keyframes slimyHover {
      0% { transform: scale(1); }
      50% { transform: scaleY(1.1) scaleX(0.95); }
      100% { transform: scale(1.05); }
    }
  `;

  const containerStyle: React.CSSProperties = {
    height: "100vh",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    background: "#000",
    animation: "backdropPulse 8s infinite alternate",
    fontFamily: "'Orbitron', sans-serif",
    textAlign: "center",
    overflow: "hidden",
    position: "relative",
  };

  const gradientHeaderBox: React.CSSProperties = {
    background: LAVENDER_GRADIENT,
    padding: "20px 60px",
    borderRadius: "2px",
    marginBottom: "30px",
    boxShadow: `0 0 60px ${NEON_PURPLE}44`,
    opacity: isLoaded ? 1 : 0,
    animation: "titleReveal 2s cubic-bezier(0.19, 1, 0.22, 1) forwards",
  };

  const titleStyle: React.CSSProperties = {
    fontSize: "clamp(32px, 8vw, 64px)",
    fontWeight: 900,
    color: "#000", // Sexy black text on gradient
    letterSpacing: "15px",
    margin: 0,
    textTransform: "uppercase",
  };

  const subtitleStyle: React.CSSProperties = {
    fontSize: "14px",
    letterSpacing: "8px",
    color: "#fff",
    opacity: 0.6,
    marginBottom: "60px",
    textTransform: "uppercase",
    animation: "titleReveal 2.5s cubic-bezier(0.19, 1, 0.22, 1) forwards",
  };

  const btnStyle: React.CSSProperties = {
    background: "transparent",
    border: `1px solid ${NEON_PURPLE}`,
    color: "#fff",
    padding: "22px 80px",
    fontSize: "14px",
    letterSpacing: "6px",
    borderRadius: "50px",
    cursor: "pointer",
    transition: "0.4s all cubic-bezier(0.175, 0.885, 0.32, 1.275)",
    boxShadow: `0 0 20px ${NEON_PURPLE}22`,
    textTransform: "uppercase",
    fontWeight: 700,
    position: "relative",
    zIndex: 10,
  };

  const glassOverlay: React.CSSProperties = {
    position: "absolute",
    width: "100%",
    height: "100%",
    background: "url('https://www.transparenttextures.com/patterns/carbon-fibre.png')",
    opacity: 0.05,
    pointerEvents: "none",
  };

  return (
    <div style={containerStyle}>
      <style>{animations}</style>
      <div style={glassOverlay} />
      
      {/* Central Identity Module */}
      <div style={gradientHeaderBox}>
        <h1 style={titleStyle}>DRONE INTEL</h1>
      </div>

      <p style={subtitleStyle}>
        Autonomous Navigation // Neural Routing // Real-time Recon
      </p>

      <button
        onClick={() => nav("/auth")}
        style={btnStyle}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = NEON_PURPLE;
          e.currentTarget.style.boxShadow = `0 0 50px ${NEON_PURPLE}`;
          e.currentTarget.style.color = "#000";
          e.currentTarget.style.transform = "scale(1.1)";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = "transparent";
          e.currentTarget.style.boxShadow = `0 0 20px ${NEON_PURPLE}22`;
          e.currentTarget.style.color = "#fff";
          e.currentTarget.style.transform = "scale(1)";
        }}
      >
        [ ENTER SYSTEM ]
      </button>

      {/* Decorative Floor Glow */}
      <div style={{
        position: 'absolute',
        bottom: '-150px',
        width: '600px',
        height: '300px',
        background: NEON_PURPLE,
        filter: 'blur(150px)',
        opacity: 0.2,
        borderRadius: '50%'
      }} />
    </div>
  );
}