import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

export default function Welcome() {
  const nav = useNavigate();
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    // Deliberate delay to ensure the animations feel premium on enter
    setTimeout(() => setIsLoaded(true), 150);
  }, []);

  // --- Theme Constants ---
  const NEON_PURPLE = "#bc13fe";
  const LAVENDER_SILK = "linear-gradient(90deg, #ffffff 0%, #d8b4fe 50%, #bc13fe 100%)";
  
  const animations = `
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

    @keyframes titleReveal {
      0% { opacity: 0; transform: translateY(40px) scale(0.9); filter: blur(15px); }
      100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0px); }
    }

    /* The Flowing Water Wave Animation */
    @keyframes move_wave_1 {
      0% { transform: scaleY(0.6) scaleX(0.9) translate3d(0, 0, 0) skewX(-10deg); }
      50% { transform: scaleY(0.7) scaleX(1.1) translate3d(-100px, 10px, 0) skewX(10deg); }
      100% { transform: scaleY(0.6) scaleX(0.9) translate3d(0, 0, 0) skewX(-10deg); }
    }
    
    @keyframes move_wave_2 {
      0% { transform: scaleY(0.5) scaleX(1) translate3d(0, 0, 0) skewX(5deg); }
      50% { transform: scaleY(0.6) scaleX(0.9) translate3d(80px, -5px, 0) skewX(-5deg); }
      100% { transform: scaleY(0.5) scaleX(1) translate3d(0, 0, 0) skewX(5deg); }
    }

    @keyframes gooeyClick {
      0% { transform: scale(1); opacity: 1; }
      20% { transform: scaleY(1.3) scaleX(0.8); opacity: 0.8; }
      100% { transform: scale(0.95); opacity: 0.9; }
    }
  `;

  const containerStyle: React.CSSProperties = {
    height: "100vh",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    background: "#000",
    fontFamily: "'Orbitron', sans-serif",
    textAlign: "center",
    overflow: "hidden",
    position: "relative",
    padding: '0 20px', // Standard gutter
  };

  const titleBoxStyle: React.CSSProperties = {
    background: LAVENDER_SILK,
    padding: "20px 70px",
    borderRadius: "2px",
    marginBottom: "15px",
    boxShadow: `0 0 50px ${NEON_PURPLE}66`,
    opacity: isLoaded ? 1 : 0,
    animation: "titleReveal 2s cubic-bezier(0.19, 1, 0.22, 1) forwards",
    zIndex: 10,
  };

  const mainTitleStyle: React.CSSProperties = {
    fontSize: "clamp(36px, 10vw, 80px)",
    fontWeight: 900,
    color: "#000", // Sexy black text on gradient
    letterSpacing: "18px",
    margin: 0,
    textTransform: "uppercase",
  };

  const subtitleStyle: React.CSSProperties = {
    fontFamily: "'Orbitron', sans-serif",
    fontSize: "clamp(12px, 3vw, 18px)",
    fontWeight: 400,
    letterSpacing: "10px",
    textTransform: "uppercase",
    background: LAVENDER_SILK, // Gradient text COLOR
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
    marginBottom: "80px",
    animation: "titleReveal 2.8s cubic-bezier(0.19, 1, 0.22, 1) forwards",
    zIndex: 10,
  };

  const btnStyle: React.CSSProperties = {
    background: "rgba(188, 19, 254, 0.05)",
    border: `2px solid ${NEON_PURPLE}`,
    color: "#fff",
    padding: "22px 70px",
    fontSize: "14px",
    letterSpacing: "6px",
    borderRadius: "50px",
    cursor: "pointer",
    transition: "0.5s all cubic-bezier(0.175, 0.885, 0.32, 1.275)",
    boxShadow: `0 0 30px ${NEON_PURPLE}44`,
    textTransform: "uppercase",
    fontWeight: 700,
    position: "relative",
    zIndex: 10,
  };

  // --- Dynamic Water Background Elements ---
  const waveBase: React.CSSProperties = {
    position: "absolute",
    left: 0,
    top: "10%",
    width: "100%",
    height: "80%",
    borderRadius: "30%",
    background: NEON_PURPLE,
    filter: "blur(70px)",
    mixBlendMode: 'screen',
    zIndex: 1,
  };

  const flowStyle1: React.CSSProperties = {
    ...waveBase,
    background: `linear-gradient(135deg, ${NEON_PURPLE}, #fff)`,
    animation: "move_wave_1 6s infinite alternate cubic-bezier(0.445, 0.05, 0.55, 0.95)",
    opacity: 0.15,
  };

  const flowStyle2: React.CSSProperties = {
    ...waveBase,
    background: `linear-gradient(135deg, ${NEON_PURPLE}, #d8b4fe)`,
    animation: "move_wave_2 10s infinite alternate cubic-bezier(0.445, 0.05, 0.55, 0.95)",
    opacity: 0.2,
    top: "15%",
  };

  return (
    <div style={containerStyle}>
      <style>{animations}</style>
      
      {/* Cinematic Water Background Nodes */}
      <div style={flowStyle1} />
      <div style={flowStyle2} />
      
      {/* Central Gateway Node */}
      <div style={titleBoxStyle}>
        <h1 style={mainTitleStyle}>A*Recon</h1>
      </div>

      <p style={subtitleStyle}>Reconnaissance, Redefined</p>

      <button
        onClick={() => nav("/auth")}
        style={btnStyle}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = NEON_PURPLE;
          e.currentTarget.style.boxShadow = `0 0 60px ${NEON_PURPLE}`;
          e.currentTarget.style.color = "#000";
          e.currentTarget.style.transform = "scale(1.1) rotateZ(1deg)";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = "rgba(188, 19, 254, 0.05)";
          e.currentTarget.style.boxShadow = `0 0 30px ${NEON_PURPLE}44`;
          e.currentTarget.style.color = "#fff";
          e.currentTarget.style.transform = "scale(1) rotateZ(0deg)";
        }}
        onMouseDown={(e) => {
          e.currentTarget.style.animation = 'gooeyClick 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards';
        }}
        onMouseUp={(e) => {
          e.currentTarget.style.animation = 'none';
        }}
      >
        [ GET STARTED ]
      </button>

      {/* High-Contrast Base Reflection */}
      <div style={{
        position: 'absolute',
        bottom: '-180px',
        width: '700px',
        height: '350px',
        background: LAVENDER_SILK,
        filter: 'blur(160px)',
        opacity: 0.25,
        borderRadius: '50%',
        zIndex: 0,
      }} />
    </div>
  );
}