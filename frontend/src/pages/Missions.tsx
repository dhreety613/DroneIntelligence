import { useState, useEffect } from "react";
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
  const [showCards, setShowCards] = useState(false);

  const planRoute = async () => {
    try {
      setLoading(true);
      setError("");
      setShowCards(false);

      const res = await api.post<RouteResponse>("/planning/route", {
        image_path: "test.jpg",
        start: { row: 0, col: 0 },
        goal: { row: 19, col: 19 },
        algorithm: "astar",
        costmap: {
          rows: 20,
          cols: 20,
          diagonal_movement: false,
        },
        bounds: {
          north: 24.88,
          south: 24.82,
          east: 92.82,
          west: 92.74,
        },
        include_weather: true,
      });

      setRoute(res.data);
      setTimeout(() => setShowCards(true), 400);
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || err.message || "Route planning failed");
    } finally {
      setLoading(false);
    }
  };

  // --- Ultra-Smooth Liquid Scroll ---
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

  // --- Theme Constants ---
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
    padding: "160px 20px 100px 20px",
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
    color: "#000",
    fontSize: "24px",
    fontWeight: 900,
    letterSpacing: "8px",
    textTransform: "uppercase",
  };

  const btnStyle: React.CSSProperties = {
    display: "block",
    margin: "0 auto 80px auto",
    background: "rgba(188, 19, 254, 0.1)",
    border: `1px solid ${NEON_PURPLE}`,
    color: "#fff",
    padding: "20px 60px",
    fontSize: "14px",
    letterSpacing: "6px",
    cursor: "pointer",
    borderRadius: "50px",
    transition: "0.5s all ease",
    boxShadow: `0 0 30px ${NEON_PURPLE}22`,
    fontFamily: "'Orbitron', sans-serif",
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
    color: "#d8b4fe",
    fontSize: "11px",
    letterSpacing: "4px",
    marginBottom: "20px",
    fontWeight: 900,
    opacity: 0.9,
  };

  const dataTextStyle: React.CSSProperties = {
    fontSize: "18px",
    fontWeight: 400,
    color: "#fff",
    letterSpacing: "1px",
    marginBottom: "8px",
  };

  return (
    <div style={containerStyle}>
      <style>{animations}</style>

      {/* FIXED TOP HEADER BAR */}
      <div style={headerBarStyle}>
        <h1 style={headerTextStyle}>MISSIONS</h1>
      </div>

      <button
        style={btnStyle}
        onClick={planRoute}
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
        {loading ? "SYNCING PATH..." : "[ INITIATE MISSION ]"}
      </button>

      {error && (
        <div style={{ textAlign: "center", color: "#f87171", fontFamily: "'Orbitron', sans-serif", letterSpacing: "2px", marginBottom: "40px" }}>
          !! ERROR_CORE_FAILURE: {error} !!
        </div>
      )}

      {route && (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: window.innerWidth > 1000 ? "350px 1fr" : "1fr",
            gap: "40px",
            maxWidth: "1200px",
            margin: "0 auto",
          }}
        >
          {/* SUMMARY CARD */}
          <div style={getGlassCardStyle(0)}>
            <div style={sectionLabelStyle}>// MISSION_SUMMARY</div>
            <div style={dataTextStyle}>Algorithm: <b style={{color: NEON_PURPLE}}>{route.algorithm}</b></div>
            <div style={dataTextStyle}>Cost Index: <b>{route.total_cost}</b></div>
            <div style={dataTextStyle}>Step Length: <b>{route.path_length}</b></div>
            <div style={dataTextStyle}>Start: <b>[{route.start.row}, {route.start.col}]</b></div>
            <div style={dataTextStyle}>Goal: <b>[{route.goal.row}, {route.goal.col}]</b></div>
            
            <div style={{
              fontSize: '22px', 
              fontWeight: 900, 
              marginTop: '25px', 
              color: route.feasible ? NEON_PURPLE : "#ff3e3e",
              textShadow: route.feasible ? `0 0 15px ${NEON_PURPLE}` : 'none'
            }}>
              {route.feasible ? ">> PATH VALIDATED" : ">> PATH OBSTRUCTED"}
            </div>

            <div style={{...dataTextStyle, fontSize: '12px', marginTop: '20px', opacity: 0.6, fontStyle: 'italic'}}>
              System Message: {route.message}
            </div>
          </div>

          {/* MAP CARD */}
          <div style={{...getGlassCardStyle(1), minHeight: "500px"}}>
            <div style={sectionLabelStyle}>// GEO_SPATIAL_FEED</div>
            <div style={{
              borderRadius: "20px", 
              overflow: "hidden", 
              border: "1px solid rgba(255,255,255,0.1)",
              height: "calc(100% - 40px)"
            }}>
              <RouteMap geoPath={route.geo_path} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}