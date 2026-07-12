import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { roleHome } from "../../routes/roleHome";

/** Sign-up flow (§7) — collapsed to a single step in this scaffold; the
 * full 3-step flow (account type -> details -> plan/payment) is Phase 1
 * frontend work, not yet built here. */
export default function SignUpPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "", account_type: "individual" });
  const [error, setError] = useState(null);

  const submit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      const user = await register(form);
      navigate(roleHome(user.role));
    } catch (err) {
      setError(err.response?.data?.error || "Registration failed");
    }
  };

  return (
    <div style={{ maxWidth: 420, margin: "60px auto" }}>
      <div className="card">
        <h1 style={{ fontSize: 20 }}>Create your account</h1>
        {error && <div style={{ color: "var(--red)", marginBottom: 10, fontSize: 13.5 }}>{error}</div>}
        <form onSubmit={submit}>
          <label>Account type</label>
          <select
            value={form.account_type}
            onChange={(e) => setForm({ ...form, account_type: e.target.value })}
            style={inputStyle}
          >
            <option value="individual">Individual</option>
            <option value="family">Family (3 learners)</option>
            <option value="professional">Professional</option>
          </select>
          <label>Full name</label>
          <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} style={inputStyle} />
          <label>Email</label>
          <input value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} style={inputStyle} />
          <label>Password</label>
          <input
            type="password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            style={inputStyle}
          />
          <button className="btn primary" style={{ width: "100%", marginTop: 10 }}>Continue</button>
        </form>
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
