import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import client from "../../api/client";
import Layout from "../../components/Layout";
import ProgressBar from "../../components/ProgressBar";
import Badge from "../../components/Badge";

/** WF02 — Individual Class View */
export default function ClassView() {
  const { classId } = useParams();
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    client
      .get(`/classes/${classId}`)
      .then((res) => setData(res.data))
      .catch((err) => setError(err.response?.data?.error || "Failed to load class"));
  }, [classId]);

  if (error) return <Layout><div className="card">{error}</div></Layout>;
  if (!data) return <Layout><div className="card">Loading…</div></Layout>;

  const { class: cls, module_progress, students, activity_feed } = data;

  return (
    <Layout>
      <div style={{ fontSize: 13, marginBottom: 10 }}>
        <Link to="/school/dashboard">Dashboard</Link> / Classes / {cls.name}
      </div>

      <div className="card" style={{ background: "var(--navy)", color: "#fff", marginBottom: 20 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
          <div>
            <div style={{ color: "#9fb4d8", fontSize: 12 }}>CLASS</div>
            <h2 style={{ margin: "4px 0" }}>{cls.name}</h2>
            <div style={{ color: "#c8d5ea", fontSize: 13 }}>{cls.student_count} students</div>
          </div>
          <button className="btn gold">Download Class Report</button>
        </div>
      </div>

      <div className="card" style={{ marginBottom: 20 }}>
        <strong>Programme modules — class average</strong>
        <div style={{ display: "grid", gridTemplateColumns: `repeat(${module_progress.length || 1}, 1fr)`, gap: 12, marginTop: 12 }}>
          {module_progress.map((m) => (
            <div key={m.id} className="card" style={{ boxShadow: "none" }}>
              <div style={{ fontSize: 12, color: "var(--text-muted)" }}>{m.title}</div>
              <div style={{ fontSize: 20, fontWeight: 700, marginTop: 4 }}>{m.completion_pct}%</div>
            </div>
          ))}
          {module_progress.length === 0 && <div className="placeholder-page">No programme assigned to this class yet.</div>}
        </div>
      </div>

      <div className="two-col">
        <div className="card">
          <strong>Students ({students.length})</strong>
          <table className="data-table" style={{ marginTop: 10 }}>
            <thead>
              <tr>
                <th>Student</th>
                <th>Progress</th>
                <th>Quiz avg</th>
                <th>Last active</th>
              </tr>
            </thead>
            <tbody>
              {students.map((s) => (
                <tr key={s.id}>
                  <td>
                    <div>{s.name}</div>
                    <Badge status={s.status} />
                  </td>
                  <td style={{ minWidth: 120 }}>
                    <div>{s.progress_pct}%</div>
                    <ProgressBar pct={s.progress_pct} />
                  </td>
                  <td>{s.quiz_avg_pct != null ? `${s.quiz_avg_pct}%` : "—"}</td>
                  <td>{s.last_active_at ? new Date(s.last_active_at).toLocaleDateString() : "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="card">
          <strong>Class activity</strong>
          <div style={{ marginTop: 10 }}>
            {activity_feed.length === 0 && <div className="placeholder-page">No recent activity.</div>}
            {activity_feed.map((e, i) => (
              <div key={i} style={{ padding: "8px 0", borderBottom: "1px solid var(--border)", fontSize: 13.5 }}>
                {e.message}
                <div style={{ color: "var(--text-muted)", fontSize: 11.5 }}>
                  {new Date(e.at).toLocaleString()}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </Layout>
  );
}
