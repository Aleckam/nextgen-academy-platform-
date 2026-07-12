import { useEffect, useState } from "react";
import client from "../../api/client";
import Layout from "../../components/Layout";
import { useAuth } from "../../context/AuthContext";

/** Student roster management (§3.5, §7). Lists students school-wide; a
 * dedicated /schools/:id/students list endpoint isn't built yet in this
 * scaffold (only per-class rosters via GET /classes/:id) — add one to
 * back this page fully. */
export default function StudentRoster() {
  const { user } = useAuth();
  const [dashboard, setDashboard] = useState(null);

  useEffect(() => {
    client.get(`/schools/${user?.school_id || 1}/dashboard`).then((res) => setDashboard(res.data));
  }, [user]);

  return (
    <Layout>
      <div className="page-header"><h1>Students</h1></div>
      <div className="card placeholder-page" style={{ marginBottom: 16 }}>
        Full roster with search/filter is a straightforward extension of the class view table
        (frontend/src/pages/school/ClassView.jsx) — add GET /api/schools/:id/students to the backend.
      </div>
      {dashboard && (
        <div className="card">
          <strong>Classes</strong>
          <table className="data-table" style={{ marginTop: 10 }}>
            <thead><tr><th>Class</th><th>Students</th></tr></thead>
            <tbody>
              {dashboard.classes.map((c) => (
                <tr key={c.id}><td>{c.name}</td><td>{c.student_count}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </Layout>
  );
}
