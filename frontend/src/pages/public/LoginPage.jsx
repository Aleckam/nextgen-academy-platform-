import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { roleHome } from "../../routes/roleHome";

/** Login page (adult email/password + student PIN) — §7 Public screens */
export default function LoginPage() {
  const { login, studentLogin } = useAuth();
  const navigate = useNavigate();
  const [mode, setMode] = useState("adult");
  const [error, setError] = useState(null);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [schoolId, setSchoolId] = useState("");
  const [username, setUsername] = useState("");
  const [pin, setPin] = useState("");

  const submitAdult = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      const user = await login(email, password);
      navigate(roleHome(user.role));
    } catch (err) {
      setError(err.response?.data?.error || "Login failed");
    }
  };

  const submitStudent = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      const user = await studentLogin(Number(schoolId), username, pin);
      navigate(roleHome(user.role));
    } catch (err) {
      setError(err.response?.data?.error || "Login failed");
    }
  };

  return (
    <div style={{ maxWidth: 420, margin: "60px auto" }}>
      <div className="card">
        <h1 style={{ fontSize: 20 }}>Log in to NextGen Academy</h1>
        <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
          <button className={`btn ${mode === "adult" ? "primary" : ""}`} onClick={() => setMode("adult")}>
            Parent / Professional / Staff
          </button>
          <button className={`btn ${mode === "student" ? "primary" : ""}`} onClick={() => setMode("student")}>
            Student Login (PIN)
          </button>
        </div>

        {error && <div style={{ color: "var(--red)", marginBottom: 10, fontSize: 13.5 }}>{error}</div>}

        {mode === "adult" ? (
          <form onSubmit={submitAdult}>
            <label>Email</label>
            <input value={email} onChange={(e) => setEmail(e.target.value)} style={inputStyle} />
            <label>Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} style={inputStyle} />
            <button className="btn primary" style={{ width: "100%", marginTop: 10 }}>Log in</button>
            <div style={{ marginTop: 10, fontSize: 13 }}>
              <Link to="/password-reset">Forgot password?</Link> · <Link to="/signup">Create account</Link>
            </div>
          </form>
        ) : (
          <form onSubmit={submitStudent}>
            <label>School code</label>
            <input value={schoolId} onChange={(e) => setSchoolId(e.target.value)} placeholder="e.g. 1" style={inputStyle} />
            <label>Username</label>
            <input value={username} onChange={(e) => setUsername(e.target.value)} style={inputStyle} />
            <label>4-digit PIN</label>
            <input value={pin} onChange={(e) => setPin(e.target.value)} maxLength={4} style={inputStyle} />
            <button className="btn primary" style={{ width: "100%", marginTop: 10 }}>Log in</button>
          </form>
        )}
      </div>
    </div>
  );
}

const inputStyle = {
  display: "block",
  width: "100%",
  padding: "8px 10px",
  marginBottom: 12,
  borderRadius: 6,
  border: "1px solid var(--border)",
};
