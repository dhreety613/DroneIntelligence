import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  const containerStyle: React.CSSProperties = {
    minHeight: "100vh",
    background: "#000",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    color: "#fff",
    fontFamily: "Orbitron, sans-serif",
  };

  const titleStyle: React.CSSProperties = {
    fontSize: "40px",
    fontWeight: 900,
    letterSpacing: "8px",
    marginBottom: "60px",
    background: "linear-gradient(90deg, #fff, #bc13fe)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
  };

  const buttonContainer: React.CSSProperties = {
    display: "flex",
    flexDirection: "column",
    gap: "25px",
    width: "300px",
  };

  const buttonStyle: React.CSSProperties = {
    padding: "16px",
    borderRadius: "50px",
    border: "1px solid #bc13fe",
    background: "rgba(188, 19, 254, 0.1)",
    color: "#fff",
    fontSize: "14px",
    letterSpacing: "4px",
    cursor: "pointer",
    transition: "0.4s",
  };

  return (
    <div style={containerStyle}>
      <h1 style={titleStyle}>DRONE COMMAND CENTER</h1>

      <div style={buttonContainer}>
        {/* ANALYSIS */}
        <button
          style={buttonStyle}
          onClick={() => navigate("/analysis")}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = "#bc13fe";
            e.currentTarget.style.color = "#000";
            e.currentTarget.style.boxShadow = "0 0 20px #bc13fe";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = "rgba(188, 19, 254, 0.1)";
            e.currentTarget.style.color = "#fff";
            e.currentTarget.style.boxShadow = "none";
          }}
        >
          ANALYSIS
        </button>

        {/* MISSIONS */}
        <button
          style={buttonStyle}
          onClick={() => navigate("/missions")}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = "#bc13fe";
            e.currentTarget.style.color = "#000";
            e.currentTarget.style.boxShadow = "0 0 20px #bc13fe";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = "rgba(188, 19, 254, 0.1)";
            e.currentTarget.style.color = "#fff";
            e.currentTarget.style.boxShadow = "none";
          }}
        >
          MISSIONS
        </button>

        {/* LIVE MISSION */}
        <button
          style={buttonStyle}
          onClick={() => navigate("/live")}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = "#bc13fe";
            e.currentTarget.style.color = "#000";
            e.currentTarget.style.boxShadow = "0 0 20px #bc13fe";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = "rgba(188, 19, 254, 0.1)";
            e.currentTarget.style.color = "#fff";
            e.currentTarget.style.boxShadow = "none";
          }}
        >
          LIVE MISSION
        </button>
      </div>
    </div>
  );
}