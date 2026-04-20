import { useEffect, useMemo, useState } from "react";
import api from "../services/api";
import LiveMissionMap from "../components/LiveMissionMap";

type GeoPoint = {
  lat: number;
  lon: number;
};

type MissionRouteResponse = {
  algorithm: string;
  image_path: string;
  feasible: boolean;
  start: { row: number; col: number };
  goal: { row: number; col: number };
  total_cost: number;
  path_length: number;
  geo_path: GeoPoint[];
  message: string;
};

type ReplanResponse = {
  mission_id: string;
  feasible: boolean;
  algorithm: string;
  old_remaining_waypoints: number;
  new_total_waypoints: number;
  current_row: number;
  current_col: number;
  goal_row: number;
  goal_col: number;
  total_cost: number;
  adjusted_geo_path: GeoPoint[];
  message: string;
};

export default function LiveMission() {
  const [route, setRoute] = useState<MissionRouteResponse | null>(null);
  const [adjustedRoute, setAdjustedRoute] = useState<GeoPoint[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [adjustmentInfo, setAdjustmentInfo] = useState<string>("No adjustment yet.");
  const [showCards, setShowCards] = useState(false);

  useEffect(() => {
    const loadInitialRoute = async () => {
      try {
        setLoading(true);

        // Create mission from stored backend setup
        await api.post("/mission/create-from-setup");

        // Get the original route from stored backend setup
        const res = await api.post<MissionRouteResponse>("/planning/run-current");

        setRoute(res.data);
        setTimeout(() => setShowCards(true), 400);
      } catch (err) {
        console.error(err);
        setAdjustmentInfo("Failed to load live mission. Make sure backend setup is done.");
      } finally {
        setLoading(false);
      }
    };

    loadInitialRoute();
  }, []);

  useEffect(() => {
    const activePath = adjustedRoute.length > 0 ? adjustedRoute : route?.geo_path;
    if (!activePath || activePath.length === 0) return;

    const interval = setInterval(() => {
      setCurrentIndex((prev) => {
        if (prev >= activePath.length - 1) {
          clearInterval(interval);
          return prev;
        }
        return prev + 1;
      });
    }, 1200);

    return () => clearInterval(interval);
  }, [route, adjustedRoute]);

  const currentPosition = useMemo(() => {
    const activePath = adjustedRoute.length > 0 ? adjustedRoute : route?.geo_path;
    if (!activePath || activePath.length === 0) return null;
    return activePath[Math.min(currentIndex, activePath.length - 1)] ?? null;
  }, [route, adjustedRoute, currentIndex]);

  const simulateAdjustment = async () => {
    try {
      setLoading(true);

      const replan = await api.post<ReplanResponse>("/replanning/local", {
        mission_id: "mission_001",
        algorithm: "astar",
        diagonal_movement: false,
        local_obstacle: {
          row: 8,
          col: 8,
          severity: 0.9,
          label: "fallen_tree",
          source: "onboard_camera",
        },
      });

      setAdjustmentInfo(
        `Adjustment triggered. Old waypoints: ${replan.data.old_remaining_waypoints}, new: ${replan.data.new_total_waypoints}, cost: ${replan.data.total_cost}`
      );
      setAdjustedRoute(replan.data.adjusted_geo_path || []);
      setCurrentIndex(0);
    } catch (err) {
      console.error(err);
      setAdjustmentInfo("Adjustment failed.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (showCards) {
      const scrollStep = () => {
        const distanceToBottom =
          document.documentElement.scrollHeight - window.innerHeight - window.scrollY;
        if (distanceToBottom > 10) {
          window.scrollBy({ top: 3, behavior: "auto" });
          requestAnimationFrame(scrollStep);
        }
      };
      const timeout = setTimeout(() => requestAnimationFrame(scrollStep), 800);
      return () => clearTimeout(timeout);
    }
  }, [showCards]);

  const NEON_PURPLE = "#bc13fe";
  const HEADER_GRADIENT =
    "linear-gradient(90deg, #ffffff 0%, #d8b4fe 50%, #bc13fe 100%)";
  const GLASS_GRADIENT =
    "linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%)";

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
    background: "rgba(239, 68, 68, 0.1)",
    border: "1px solid #ef4444",
    color: "#fff",
    padding: "16px 30px",
    fontSize: "12px",
    letterSpacing: "3px",
    cursor: "pointer",
    borderRadius: "50px",
    transition: "0.5s all ease",
    boxShadow: "0 0 20px rgba(239, 68, 68, 0.2)",
    marginBottom: "20px",
    width: "100%",
    textTransform: "uppercase",
    fontFamily: "'Orbitron', sans-serif",
  };

  const getGlassCardStyle = (index: number): React.CSSProperties => ({
    background: GLASS_GRADIENT,
    backdropFilter: "blur(25px)",
    WebkitBackdropFilter: "blur(25px)",
    border: "1px solid rgba(255, 255, 255, 0.2)",
    padding: "35px",
    borderRadius: "30px",
    opacity: showCards ? 1 : 0,
    animation: showCards
      ? `slimyPop 2.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) ${index * 0.7}s forwards`
      : "none",
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
    fontSize: "16px",
    fontWeight: 400,
    color: "#fff",
    letterSpacing: "1px",
    marginBottom: "12px",
  };

  return (
    <div style={containerStyle}>
      <style>{animations}</style>

      <div style={headerBarStyle}>
        <h1 style={headerTextStyle}>LIVE MISSION</h1>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: window.innerWidth > 1100 ? "380px 1fr" : "1fr",
          gap: "40px",
          maxWidth: "1400px",
          margin: "0 auto",
        }}
      >
        <div style={getGlassCardStyle(0)}>
          <div style={sectionLabelStyle}>// MISSION_CONTROLS</div>

          <button
            onClick={simulateAdjustment}
            disabled={loading || !route}
            style={btnStyle}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = "#ef4444";
              e.currentTarget.style.boxShadow = "0 0 30px rgba(239, 68, 68, 0.6)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = "rgba(239, 68, 68, 0.1)";
              e.currentTarget.style.boxShadow = "0 0 20px rgba(239, 68, 68, 0.2)";
            }}
          >
            {loading ? "PROCESSING..." : "SIMULATE ADJUSTMENT"}
          </button>

          <div style={dataTextStyle}>
            Status:{" "}
            <b style={{ color: adjustedRoute.length > 0 ? NEON_PURPLE : "#fff" }}>
              {adjustedRoute.length > 0 ? "ADJUSTED_ACTIVE" : "FOLLOWING_ORIGINAL"}
            </b>
          </div>
          <div style={dataTextStyle}>
            Current Step: <b>{currentIndex + 1}</b>
          </div>

          <div
            style={{
              ...dataTextStyle,
              fontSize: "12px",
              marginTop: "20px",
              opacity: 0.6,
              borderTop: "1px solid rgba(255,255,255,0.1)",
              paddingTop: "15px",
            }}
          >
            <div style={sectionLabelStyle}>// ADJUSTMENT_LOG</div>
            {adjustmentInfo}
          </div>

          <div
            style={{
              marginTop: "30px",
              padding: "20px",
              background: "rgba(0,0,0,0.3)",
              borderRadius: "15px",
            }}
          >
            <div style={{ ...sectionLabelStyle, marginBottom: "10px" }}>// LEGEND</div>
            <p style={{ fontSize: "11px", color: "#3b82f6" }}>● ORIGINAL_PATH_LINK</p>
            <p style={{ fontSize: "11px", color: "#ef4444" }}>● ADJUSTED_PATH_LINK</p>
            <p style={{ fontSize: "11px", color: "#4ade80" }}>● LIVE_DRONE_MARKER</p>
          </div>
        </div>

        <div style={{ ...getGlassCardStyle(1), minHeight: "600px" }}>
          <div style={sectionLabelStyle}>// LIVE_SPATIAL_TELEMETRY</div>
          <div
            style={{
              borderRadius: "20px",
              overflow: "hidden",
              border: "1px solid rgba(255,255,255,0.1)",
              height: "calc(100% - 40px)",
              boxShadow: `inset 0 0 30px #000`,
            }}
          >
            {route && (
              <LiveMissionMap
                originalPath={route.geo_path}
                adjustedPath={adjustedRoute}
                currentPosition={currentPosition}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}