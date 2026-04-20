import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function Auth() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [username, setUsername] = useState("");
  const nav = useNavigate();

  const handleSubmit = async () => {
    try {
      if (isLogin) {
        const res = await api.post("/auth/login", { email, password });
        console.log(res.data);
        alert("Login successful");
        nav("/home");
      } else {
        await api.post("/auth/signup", { username, email, password });
        alert("Signup successful. Please log in.");
        setIsLogin(true);
        setPassword("");
      }
    } catch (err: any) {
      alert(err.response?.data?.detail || "Error");
    }
  };

  // --- Theme Constants ---
  const NEON_PURPLE = "#bc13fe";
  const HEADER_GRADIENT = "linear-gradient(90deg, #ffffff 0%, #d8b4fe 50%, #bc13fe 100%)";
  const GLASS_GRADIENT = "linear-gradient(135deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.03) 100%)";

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
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: "24px",
    fontFamily: "'Orbitron', sans-serif",
    position: "relative",
    overflow: "hidden",
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

  const authCardStyle: React.CSSProperties = {
    width: "420px",
    background: GLASS_GRADIENT,
    backdropFilter: "blur(25px)",
    WebkitBackdropFilter: "blur(25px)",
    border: "1px solid rgba(255, 255, 255, 0.15)",
    borderRadius: "30px",
    padding: "45px",
    color: "white",
    boxShadow: "0 20px 50px rgba(0,0,0,0.6)",
    animation: "slimyPop 1.2s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards",
    zIndex: 2,
  };

  const inputStyle: React.CSSProperties = {
    width: "100%",
    padding: "16px",
    marginBottom: "18px",
    borderRadius: "12px",
    border: "1px solid rgba(255, 255, 255, 0.1)",
    background: "rgba(0, 0, 0, 0.4)",
    color: "white",
    boxSizing: "border-box",
    fontFamily: "'Orbitron', sans-serif",
    fontSize: "13px",
    letterSpacing: "1px",
    outline: "none",
    transition: "0.3s border-color",
  };

  const primaryButton: React.CSSProperties = {
    width: "100%",
    background: NEON_PURPLE,
    color: "#000",
    border: "none",
    padding: "18px",
    borderRadius: "50px",
    cursor: "pointer",
    marginTop: "10px",
    fontWeight: 900,
    fontSize: "14px",
    letterSpacing: "4px",
    textTransform: "uppercase",
    fontFamily: "'Orbitron', sans-serif",
    boxShadow: `0 0 30px ${NEON_PURPLE}44`,
    transition: "0.4s all ease",
  };

  const googleButton: React.CSSProperties = {
    width: "100%",
    background: "transparent",
    color: "#fff",
    border: "1px solid #ef4444",
    padding: "18px",
    borderRadius: "50px",
    cursor: "pointer",
    marginTop: "15px",
    fontWeight: 900,
    fontSize: "12px",
    letterSpacing: "2px",
    textTransform: "uppercase",
    fontFamily: "'Orbitron', sans-serif",
    transition: "0.4s all ease",
  };

  return (
    <div style={containerStyle}>
      <style>{animations}</style>

      {/* FIXED TOP HEADER */}
      <div style={headerBarStyle}>
        <h1 style={{ color: "#000", fontSize: "24px", fontWeight: 900, letterSpacing: "8px", margin: 0 }}>
          DRONE INTEL ANALYSIS
        </h1>
      </div>

      <div style={authCardStyle}>
        <div style={{ color: "#d8b4fe", fontSize: "10px", letterSpacing: "5px", marginBottom: "15px", fontWeight: 900 }}>
          // ACCESS_PROTOCOL
        </div>
        
        <h2 style={{ fontSize: "28px", marginBottom: "30px", letterSpacing: "2px", fontWeight: 700 }}>
          {isLogin ? "IDENTITY_LOGIN" : "IDENTITY_CREATE"}
        </h2>

        {!isLogin && (
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="USERNAME"
            style={inputStyle}
            onFocus={(e) => e.currentTarget.style.borderColor = NEON_PURPLE}
            onBlur={(e) => e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.1)"}
          />
        )}

        <input
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="EMAIL_ADDRESS"
          style={inputStyle}
          onFocus={(e) => e.currentTarget.style.borderColor = NEON_PURPLE}
          onBlur={(e) => e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.1)"}
        />

        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="SECURE_PASSWORD"
          style={inputStyle}
          onFocus={(e) => e.currentTarget.style.borderColor = NEON_PURPLE}
          onBlur={(e) => e.currentTarget.style.borderColor = "rgba(255, 255, 255, 0.1)"}
        />

        <button 
          onClick={handleSubmit} 
          style={primaryButton}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = "scale(1.02)";
            e.currentTarget.style.boxShadow = `0 0 50px ${NEON_PURPLE}88`;
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = "scale(1)";
            e.currentTarget.style.boxShadow = `0 0 30px ${NEON_PURPLE}44`;
          }}
        >
          {isLogin ? "[ AUTHORIZE ]" : "[ REGISTER ]"}
        </button>

        <button 
          style={googleButton}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = "#ef4444";
            e.currentTarget.style.color = "#000";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = "transparent";
            e.currentTarget.style.color = "#fff";
          }}
        >
          Continue with Google
        </button>

        <p
          style={{
            marginTop: "30px",
            color: "#d8b4fe",
            cursor: "pointer",
            textAlign: "center",
            fontSize: "11px",
            letterSpacing: "2px",
            opacity: 0.7,
            textTransform: "uppercase"
          }}
          onClick={() => setIsLogin(!isLogin)}
        >
          {isLogin ? "> Request new credentials" : "> Return to login console"}
        </p>
      </div>

      {/* Decorative Bottom Glow */}
      <div style={{
        position: 'absolute',
        bottom: '-100px',
        width: '60%',
        height: '200px',
        background: NEON_PURPLE,
        filter: 'blur(150px)',
        borderRadius: '50%',
        opacity: 0.2,
        zIndex: 1
      }} />
    </div>
  );
}