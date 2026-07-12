import { Link } from "react-router-dom";

export default function PublicLayout({ children }) {
  return (
    <div>
      <header
        style={{
          background: "var(--navy)",
          color: "#fff",
          padding: "14px 28px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <Link to="/" style={{ color: "#fff", fontWeight: 700 }}>NextGen Academy of Finance &amp; AI</Link>
        <nav style={{ display: "flex", gap: 18, fontSize: 13.5 }}>
          <Link to="/pricing" style={{ color: "#cfe0ff" }}>Pricing</Link>
          <Link to="/blog" style={{ color: "#cfe0ff" }}>Blog</Link>
          <Link to="/login" style={{ color: "#cfe0ff" }}>Log in</Link>
          <Link to="/signup" style={{ color: "#fff" }}>Sign up</Link>
        </nav>
      </header>
      <main style={{ padding: 28, maxWidth: 1100, margin: "0 auto" }}>{children}</main>
    </div>
  );
}
