import api from "../services/api";
import { useState, useEffect } from "react";

export default function Auth() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [username, setUsername] = useState("");
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    setIsLoaded(true);
  }, []);

  const handleSubmit = async () => {
    try {
      if (isLogin) {
        const res = await api.post("/auth/login", { email, password });
        console.log(res.data);
        alert("Login success");
      } else {
        await api.post("/auth/signup", { username, email, password });
        alert("Signup success");
      }
    } catch (err: any) {
      alert(err.response?.data?.detail || "Error");
    }
  };

  // --- Theme Constants ---
  const NEON_PURPLE = "#bc13fe";
  const HEADER_GRADIENT = "linear-gradient(90deg, #ffffff 0%, #d8b4fe 50%, #bc13fe 100%)";
  const GLASS_GRADIENT = "linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.03) 100%)";

  const animations = `
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

    @keyframes nodeReveal {
      0% { opacity: 0; transform: translateY(30px) scale(0.95); filter: blur(15px); }
      100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0px); }
    }

    @keyframes pulseGlow {
      0% { box-shadow: 0 0 20px rgba(188, 19, 254, 0.2); }
      100% { box-shadow: 0 0 40px rgba(188, 19, 254, 0.4); }
    }
  `;

  const containerStyle: React.CSSProperties = {
    height: "100vh",
    background: "#000",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    fontFamily: "'Orbitron', sans-serif",
    padding: "20px",
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

  const glassCardStyle: React.CSSProperties = {
    background: GLASS_GRADIENT,
    backdropFilter: "blur(25px)",
    WebkitBackdropFilter: "blur(25px)",
    border: "1px solid rgba(255, 255, 255, 0.15)",
    padding: "50px",
    borderRadius: "30px",
    width: "100%",
    maxWidth: "450px",
    animation: "nodeReveal 1.2s cubic-bezier(0.19, 1, 0.22, 1) forwards",
    textAlign: "center",
    boxShadow: "0 25px 50px rgba(0,0,0,0.8)",
  };

  const inputStyle: React.CSSProperties = {
    width: "100%",
    background: "rgba(255, 255, 255, 0.05)",
    border: "1px solid rgba(255, 255, 255, 0.1)",
    padding: "18px 20px",
    borderRadius: "15px",
    color: "#fff",
    marginBottom: "20px",
    fontFamily: "'Orbitron', sans-serif",
    fontSize: "14px",
    outline: "none",
    transition: "0.3s all ease",
  };

  const mainBtnStyle: React.CSSProperties = {
    width: "100%",
    padding: "18px",
    background: NEON_PURPLE,
    border: "none",
    borderRadius: "50px",
    color: "#000",
    fontWeight: 900,
    fontSize: "16px",
    letterSpacing: "4px",
    cursor: "pointer",
    marginTop: "10px",
    transition: "0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)",
    boxShadow: `0 0 30px ${NEON_PURPLE}66`,
    textTransform: "uppercase",
  };

  const switchBtnStyle: React.CSSProperties = {
    background: "none",
    border: "none",
    color: "#fff",
    opacity: 0.5,
    marginTop: "25px",
    fontSize: "11px",
    letterSpacing: "3px",
    cursor: "pointer",
    textTransform: "uppercase",
    transition: "0.3s opacity",
  };

  return (
    <div style={containerStyle}>
      <style>{animations}</style>

      <div style={headerBarStyle}>
        <h1 style={{ color: "#000", fontSize: "24px", fontWeight: 900, letterSpacing: "8px" }}>
          DRONE INTEL ANALYSIS
        </h1>
      </div>

      <div style={glassCardStyle}>
        <div style={{ color: NEON_PURPLE, fontSize: "10px", letterSpacing: "5px", marginBottom: "30px", fontWeight: 900 }}>
          // {isLogin ? "IDENTITY_CHECK" : "CREATE_ACCESS_NODE"}
        </div>

        {!isLogin && (
          <input
            style={inputStyle}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="[ USERNAME ]"
            onFocus={(e) => (e.currentTarget.style.borderColor = NEON_PURPLE)}
            onBlur={(e) => (e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.1)")}
          />
        )}

        <input
          style={inputStyle}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="[ EMAIL_ADDRESS ]"
          onFocus={(e) => (e.currentTarget.style.borderColor = NEON_PURPLE)}
          onBlur={(e) => (e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.1)")}
        />

        <input
          style={inputStyle}
          type="password"
          onChange={(e) => setPassword(e.target.value)}
          placeholder="[ ACCESS_KEY ]"
          onFocus={(e) => (e.currentTarget.style.borderColor = NEON_PURPLE)}
          onBlur={(e) => (e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.1)")}
        />

        <button
          style={mainBtnStyle}
          onClick={handleSubmit}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = "scale(1.05)";
            e.currentTarget.style.boxShadow = `0 0 50px ${NEON_PURPLE}`;
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = "scale(1)";
            e.currentTarget.style.boxShadow = `0 0 30px ${NEON_PURPLE}66`;
          }}
        >
          {isLogin ? "INITIATE LOGIN" : "RESERVE ACCESS"}
        </button>

        <button
          style={switchBtnStyle}
          onClick={() => setIsLogin(!isLogin)}
          onMouseEnter={(e) => (e.currentTarget.style.opacity = "1")}
          onMouseLeave={(e) => (e.currentTarget.style.opacity = "0.5")}
        >
          {isLogin ? ">> REQUEST NEW CREDENTIALS" : ">> RETURN TO SECURE LOGIN"}
        </button>
      </div>
    </div>
  );
}