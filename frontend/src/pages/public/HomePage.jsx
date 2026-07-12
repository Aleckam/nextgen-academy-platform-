import { Link } from "react-router-dom";
import PublicLayout from "../../components/PublicLayout";

export default function HomePage() {
  return (
    <PublicLayout>
      <div className="card" style={{ textAlign: "center", padding: 50 }}>
        <h1>Financial literacy &amp; AI education for Zimbabwe</h1>
        <p style={{ color: "var(--text-muted)", maxWidth: 560, margin: "10px auto" }}>
          For individual learners, schools, and professionals — video lessons, quizzes and
          certificates, built for any device.
        </p>
        <div style={{ display: "flex", gap: 12, justifyContent: "center", marginTop: 20 }}>
          <Link className="btn primary" to="/signup">Get started</Link>
          <Link className="btn" to="/pricing">See pricing</Link>
        </div>
      </div>
    </PublicLayout>
  );
}
