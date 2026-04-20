import { useState } from "react";
import api from "../services/api";
import RouteMap from "../components/RouteMap";

type RouteStep = {
  row: number;
  col: number;
  cumulative_cost: number;
};

type GeoRouteStep = {
  lat: number;
  lon: number;
};

type RouteResponse = {
  algorithm: string;
  image_path: string;
  feasible: boolean;
  start: { row: number; col: number };
  goal: { row: number; col: number };
  total_cost: number;
  path_length: number;
  path: RouteStep[];
  geo_path: GeoRouteStep[];
  message: string;
  costmap_rows: number;
  costmap_cols: number;
  bounds: {
    north: number;
    south: number;
    east: number;
    west: number;
  };
};

export default function Missions() {
  const [route, setRoute] = useState<RouteResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const planRoute = async () => {
    try {
      setLoading(true);
      setError("");
      const res = await api.post<RouteResponse>("/planning/run-current");
      setRoute(res.data);
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || err.message || "Route planning failed");
    } finally {
      setLoading(false);
    }
  };

  // --- Theme Constants ---
  const NEON_PURPLE = "#bc13fe";
  const HEADER_GRADIENT = "linear-gradient(90deg, #ffffff 0%, #d8b4fe 50%, #bc13fe 100%)";
  const GLASS_GRADIENT = "linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.03) 100%)";

  const animations = `
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

    @keyframes slimyPop {
      0% { opacity: 0; transform: translateY(60px) scaleY(1.3) scaleX(0.9); filter: blur(20px); }
      60% { transform: translateY(-5px) scaleY(0.9) scaleX(1.02); }
      100% { opacity: 1; transform: translateY(0) scaleY(1) scaleX(1); filter: blur(0px); }
    }
  `;

  const containerStyle: React.CSSProperties = {
    minHeight: "100vh",
    background: "#000",
    color: "#fff",
    padding: "140px 24px 60px 24px",
    fontFamily: "'Orbitron', sans-serif",
    position: "relative",
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

  const planBtnStyle: React.CSSProperties = {
    background: NEON_PURPLE,
    color: "#000",
    border: "none",
    padding: "18px 40px",
    borderRadius: "50px",
    cursor: "pointer",
    fontSize: "14px",
    fontWeight: 900,
    letterSpacing: "4px",
    textTransform: "uppercase",
    marginBottom: "40px",
    boxShadow: `0 0 30px ${NEON_PURPLE}66`,
    transition: "0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)",
    fontFamily: "'Orbitron', sans-serif",
  };

  const getGlassCardStyle = (delay: number): React.CSSProperties => ({
    background: GLASS_GRADIENT,
    backdropFilter: "blur(25px)",
    WebkitBackdropFilter: "blur(25px)",
    border: "1px solid rgba(255, 255, 255, 0.15)",
    borderRadius: "30px",
    padding: "35px",
    animation: `slimyPop 1.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) ${delay}s forwards`,
    opacity: 0,
    boxShadow: "0 20px 50px rgba(0,0,0,0.6)",
  });

  const sectionLabelStyle: React.CSSProperties = {
    color: "#d8b4fe",
    fontSize: "10px",
    letterSpacing: "5px",
    marginBottom: "25px",
    fontWeight: 900,
    textTransform: "uppercase",
  };

  const infoRowStyle: React.CSSProperties = {
    fontSize: "14px",
    marginBottom: "15px",
    letterSpacing: "1px",
    borderBottom: "1px solid rgba(255,255,255,0.05)",
    paddingBottom: "10px",
    display: "flex",
    justifyContent: "space-between",
  };

  return (
    <div style={containerStyle}>
      <style>{animations}</style>

      <div style={headerBarStyle}>
        <h1 style={{ color: "#000", fontSize: "24px", fontWeight: 900, letterSpacing: "8px", margin: 0 }}>
          DRONE INTEL ANALYSIS
        </h1>
      </div>

      <div style={{ textAlign: "center" }}>
        <button
          onClick={planRoute}
          style={planBtnStyle}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = "scale(1.05)";
            e.currentTarget.style.boxShadow = `0 0 50px ${NEON_PURPLE}`;
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = "scale(1)";
            e.currentTarget.style.boxShadow = `0 0 30px ${NEON_PURPLE}66`;
          }}
        >
          {loading ? "[ CALCULATING... ]" : "[ INITIATE_PLANNING ]"}
        </button>

        {error && (
          <div style={{ color: "#ef4444", fontSize: "12px", letterSpacing: "2px", marginBottom: "20px" }}>
            ALERT // {error}
          </div>
        )}
      </div>

      {route && (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: window.innerWidth > 1100 ? "380px 1fr" : "1fr",
            gap: "30px",
            maxWidth: "1400px",
            margin: "0 auto",
          }}
        >
          {/* Summary Card */}
          <div style={getGlassCardStyle(0.2)}>
            <div style={sectionLabelStyle}>// ROUTE_SUMMARY</div>
            <div style={infoRowStyle}><span>Algorithm:</span> <b>{route.algorithm}</b></div>
            <div style={infoRowStyle}>
              <span>Status:</span> 
              <b style={{ color: route.feasible ? "#4ade80" : "#ef4444" }}>
                {route.feasible ? "FEASIBLE" : "NON_FEASIBLE"}
              </b>
            </div>
            <div style={infoRowStyle}><span>Cost Density:</span> <b>{route.total_cost}</b></div>
            <div style={infoRowStyle}><span>Nodes:</span> <b>{route.path_length}</b></div>
            <div style={infoRowStyle}><span>Origin:</span> <b>{route.start.row}, {route.start.col}</b></div>
            <div style={infoRowStyle}><span>Target:</span> <b>{route.goal.row}, {route.goal.col}</b></div>
            
            <p style={{ fontSize: "11px", opacity: 0.5, marginTop: "20px", fontStyle: "italic" }}>
              Log: {route.message}
            </p>
          </div>

          {/* Map Card */}
          <div style={getGlassCardStyle(0.5)}>
            <div style={sectionLabelStyle}>// GEO_SPATIAL_PATH_VISUALIZATION</div>
            <div style={{ 
              borderRadius: "20px", 
              overflow: "hidden", 
              border: "1px solid rgba(255,255,255,0.1)",
              background: "rgba(0,0,0,0.4)"
            }}>
              <RouteMap geoPath={route.geo_path} />
            </div>
          </div>
        </div>
      )}

      {/* Footer Decoration */}
      <div style={{
        marginTop: "60px",
        width: "120px",
        height: "4px",
        background: HEADER_GRADIENT,
        borderRadius: "10px",
        margin: "60px auto 0 auto",
        boxShadow: `0 0 20px ${NEON_PURPLE}66`,
        opacity: 0.6
      }} />
    </div>
  );
}