import { useState, useEffect } from "react";
import api from "../services/api";

export default function Analysis() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [showCards, setShowCards] = useState(false);

  const runAnalysis = async () => {
    setData(null);
    setShowCards(false);
    setLoading(true);
    try {
      const res = await api.post("/analysis/image", {
        image_path: "C:/Users/armyt/Desktop/Drone/backend/test.jpg",
        include_weather: true,
      });
      setData(res.data);
      setTimeout(() => setShowCards(true), 400);
    } catch (err) {
      console.error(err);
      alert("Error running analysis");
    } finally {
      setLoading(false);
    }
  };

  // --- Liquid Smooth Scroll ---
  useEffect(() => {
    if (showCards) {
      const scrollStep = () => {
        const distanceToBottom = document.documentElement.scrollHeight - window.innerHeight - window.scrollY;
        if (distanceToBottom > 10) {
          window.scrollBy({ top: 3, behavior: "auto" });
          requestAnimationFrame(scrollStep);
        }
      };
      const timeout = setTimeout(() => requestAnimationFrame(scrollStep), 800);
      return () => clearTimeout(timeout);
    }
  }, [showCards]);

  // --- Styles ---
  const NEON_PURPLE = "#bc13fe";
  const HEADER_GRADIENT = "linear-gradient(90deg, #ffffff 0%, #d8b4fe 50%, #bc13fe 100%)";
  const GLASS_GRADIENT = "linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%)";

  const animations = `
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

    @keyframes slimyPop {
      0% {
        opacity: 0;
        transform: translateY(100px) scaleY(1.3) scaleX(0.9);
        filter: blur(20px);
      }
      60% {
        transform: translateY(-10px) scaleY(0.9) scaleX(1.05);
        filter: blur(5px);
      }
      100% {
        opacity: 1;
        transform: translateY(0) scaleY(1) scaleX(1);
        filter: blur(0px);
      }
    }
  `;

  const containerStyle: React.CSSProperties = {
    background: "#000",
    minHeight: "100vh",
    padding: "160px 20px 100px 20px", // Extra top padding to clear the fixed header
    color: "#fff",
    fontFamily: "'Orbitron', sans-serif",
    overflowX: "hidden",
  };

  const headerBarStyle: React.CSSProperties = {
    position: "fixed",
    top: 0,
    left: 0,
    width: "100%",
    height: "80px",
    background: HEADER_GRADIENT,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    zIndex: 1000,
    boxShadow: "0 10px 30px rgba(188, 19, 254, 0.3)",
  };

  const headerTextStyle: React.CSSProperties = {
    color: "#000", // Black text on the gradient bar
    fontSize: "24px",
    fontWeight: 900,
    letterSpacing: "8px",
    textTransform: "uppercase",
  };

  const btnStyle: React.CSSProperties = {
    display: "block",
    margin: "0 auto 100px auto",
    background: "rgba(188, 19, 254, 0.1)",
    border: `1px solid ${NEON_PURPLE}`,
    color: "#fff",
    padding: "18px 50px",
    fontSize: "14px",
    letterSpacing: "6px",
    cursor: "pointer",
    borderRadius: "50px",
    transition: "0.5s all ease",
    boxShadow: `0 0 30px ${NEON_PURPLE}22`,
  };

  const cardContainer: React.CSSProperties = {
    display: "flex",
    flexDirection: "column",
    gap: "50px",
    maxWidth: "850px",
    margin: "0 auto",
  };

  const getGlassCardStyle = (index: number): React.CSSProperties => ({
    background: GLASS_GRADIENT,
    backdropFilter: "blur(25px)",
    WebkitBackdropFilter: "blur(25px)",
    border: "1px solid rgba(255, 255, 255, 0.2)",
    padding: "40px",
    borderRadius: "30px",
    opacity: showCards ? 1 : 0,
    animation: showCards ? `slimyPop 2.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) ${index * 0.7}s forwards` : "none",
    boxShadow: "0 20px 50px rgba(0, 0, 0, 0.7)",
    transformOrigin: "bottom center",
  });

  const sectionLabelStyle: React.CSSProperties = {
    color: "#d8b4fe", // Lavender labels
    fontSize: "11px",
    letterSpacing: "4px",
    marginBottom: "20px",
    fontWeight: 900,
    opacity: 0.9,
  };

  const dataTextStyle: React.CSSProperties = {
    fontSize: "20px",
    fontWeight: 400,
    color: "#fff",
    letterSpacing: "1px",
  };

  return (
    <div style={containerStyle}>
      <style>{animations}</style>

      {/* FIXED TOP HEADER BAR */}
      <div style={headerBarStyle}>
        <h1 style={headerTextStyle}>DRONE INTEL ANALYSIS</h1>
      </div>

      <button 
        style={btnStyle} 
        onClick={runAnalysis}
        onMouseEnter={(e) => {
          e.currentTarget.style.boxShadow = `0 0 50px ${NEON_PURPLE}`;
          e.currentTarget.style.background = NEON_PURPLE;
          e.currentTarget.style.color = "#000";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.boxShadow = `0 0 30px ${NEON_PURPLE}22`;
          e.currentTarget.style.background = "rgba(188, 19, 254, 0.1)";
          e.currentTarget.style.color = "#fff";
        }}
      >
        {loading ? "DATA SYNCING..." : "[ INITIATE ANALYSIS ]"}
      </button>

      {data && (
        <div style={cardContainer}>
          {/* OBSTACLE DATA */}
          <div style={getGlassCardStyle(0)}>
            <div style={sectionLabelStyle}>// MODULE_OBSTACLE_SCAN</div>
            <div style={dataTextStyle}>Threat Count: <b>{data.obstacle_analysis.obstacle_count}</b></div>
            <div style={{...dataTextStyle, fontSize: '14px', marginTop: '10px', opacity: 0.6}}>
              Objects: {data.obstacle_analysis.detections.map((d: any) => d.label).join(" | ")}
            </div>
          </div>

          {/* TERRAIN DATA */}
          <div style={getGlassCardStyle(1)}>
            <div style={sectionLabelStyle}>// MODULE_TERRAIN_MAP</div>
            <div style={dataTextStyle}>Surface: <b>{data.terrain_analysis.terrain_class}</b></div>
            <div style={dataTextStyle}>Difficulty: <b>{data.terrain_analysis.difficulty_score}</b></div>
          </div>

          {/* WEATHER DATA */}
          <div style={getGlassCardStyle(2)}>
            <div style={sectionLabelStyle}>// MODULE_ENV_STATS</div>
            <div style={dataTextStyle}>Severity: <b>{data.weather_analysis.severity_level}</b></div>
            <div style={dataTextStyle}>Risk: <b>{data.weather_analysis.risk_score}</b></div>
          </div>

          {/* RISK SUMMARY */}
          <div style={getGlassCardStyle(3)}>
            <div style={sectionLabelStyle}>// MODULE_RISK_COMPUTE</div>
            <div style={dataTextStyle}>Combined Score: <b>{data.combined_risk_score}</b></div>
            <div style={{
              fontSize: '24px', 
              fontWeight: 900, 
              marginTop: '20px', 
              color: data.feasible ? NEON_PURPLE : "#ff3e3e",
              textShadow: data.feasible ? `0 0 15px ${NEON_PURPLE}` : 'none'
            }}>
              {data.feasible ? ">> STATUS: CLEAR FOR TAKEOFF" : ">> STATUS: GROUNDED"}
            </div>
          </div>

          {/* FINAL RECOMMENDATION */}
          <div style={{
            ...getGlassCardStyle(4),
            border: `1px solid ${NEON_PURPLE}`,
            background: "linear-gradient(135deg, rgba(188, 19, 254, 0.25) 0%, rgba(255, 255, 255, 0.05) 100%)"
          }}>
            <div style={{...sectionLabelStyle, color: '#fff'}}>// NEURAL_OUTPUT</div>
            <div style={{...dataTextStyle, fontSize: '22px', fontStyle: 'italic', lineHeight: 1.6}}>
              "{data.recommended_action}"
            </div>
          </div>
        </div>
      )}
    </div>
  );
}