import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import client from "../../api/client";
import Layout from "../../components/Layout";
import StatCard from "../../components/StatCard";
import ProgressBar from "../../components/ProgressBar";
import Badge from "../../components/Badge";
import { useAuth } from "../../context/AuthContext";

/** WF01 — School Admin Dashboard */
export default function SchoolDashboard() {
  const { user } = useAuth();
  const schoolId = user?.school_id || 1;
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    client
      .get(`/schools/${schoolId}/dashboard`)
      .then((res) => setData(res.data))
      .catch((err) => setError(err.response?.data?.error || "Failed to load dashboard"));
  }, [schoolId]);

  const downloadTermReport = async () => {
    const res = await client.get(`/schools/${schoolId}/term-report.pdf`, { responseType: "blob" });
    const url = window.URL.createObjectURL(new Blob([res.data]));
    const a = document.createElement("a");
    a.href = url;
    a.download = "term-report.pdf";
    a.click();
  };

  if (error) return <Layout><div className="card">{error}</div></Layout>;
  if (!data) return <Layout><div className="card">Loading…</div></Layout>;

  const { school, stats, classes, inactive_students } = data;

  return (
    <Layout>
      <div className="page-header">
        <div>
          <h1>School Dashboard</h1>
          <div style={{ color: "var(--text-muted)", fontSize: 13 }}>{school.name}</div>
        </div>
        <span className="badge on-track">{school.term_label}</span>
      </div>

      <div className="stat-grid">
        <StatCard value={stats.students_enrolled} label={`Students enrolled · Across ${stats.classes_count} classes`} />
        <StatCard value={`${stats.average_completion_pct}%`} label="Average completion" tone="amber" />
        <StatCard value={stats.certificates_earned} label="Certificates earned" tone="green" />
        <StatCard value={stats.active_this_week} label="Active this week" />
      </div>

      <div className="card" style={{ marginBottom: 20 }}>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 10 }}>
          <strong>Classes &amp; Progress</strong>
          <Link to="/school/classes/new">+ Add class</Link>
        </div>
        <table className="data-table">
          <thead>
            <tr>
              <th>Class</th>
              <th>Students</th>
              <th>Completion</th>
              <th>Status</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {classes.map((c) => (
              <tr key={c.id}>
                <td>
                  <div>{c.name}</div>
                  {c.teacher_name && <div style={{ color: "var(--text-muted)", fontSize: 12 }}>{c.teacher_name}</div>}
                </td>
                <td>{c.student_count}</td>
                <td style={{ minWidth: 140 }}>
                  <div>{c.completion_pct}%</div>
                  <ProgressBar pct={c.completion_pct} />
                </td>
                <td><Badge status={c.status} /></td>
                <td><Link className="btn" to={`/school/classes/${c.id}`}>View</Link></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="two-col">
        <div className="card">
          <strong>Students not active recently</strong>
          <div style={{ marginTop: 10 }}>
            {inactive_students.length === 0 && <div className="placeholder-page">Everyone's active — nice.</div>}
            {inactive_students.map((s) => (
              <div key={s.id} style={{ display: "flex", justifyContent: "space-between", padding: "8px 0", borderBottom: "1px solid var(--border)" }}>
                <span>{s.name}</span>
                <span className="badge needs-attention">
                  {s.last_active_at ? `${Math.round((Date.now() - new Date(s.last_active_at)) / 86400000)} days` : "Never"}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="card" style={{ background: "var(--navy)", color: "#fff" }}>
          <strong>{school.term_label} Report — Ready</strong>
          <p style={{ color: "#c8d5ea", fontSize: 13 }}>
            Auto-generated. Covers completion rates, quiz scores, and certificates for all {stats.classes_count} classes.
          </p>
          <button className="btn gold" onClick={downloadTermReport}>Download Term Report (PDF)</button>
        </div>
      </div>
    </Layout>
  );
}
