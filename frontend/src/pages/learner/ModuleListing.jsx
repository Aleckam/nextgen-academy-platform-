import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import client from "../../api/client";
import Layout from "../../components/Layout";
import { useAuth } from "../../context/AuthContext";

/** Programme -> Module -> Lesson listing (§3.3, §3.4). */
export default function ModuleListing() {
  const { user } = useAuth();
  const [programmes, setProgrammes] = useState([]);
  const [modulesByProgramme, setModulesByProgramme] = useState({});

  useEffect(() => {
    client.get("/content/programmes", { params: { age_group: user?.age_group } }).then((res) => {
      setProgrammes(res.data);
      res.data.forEach((p) => {
        client.get(`/content/programmes/${p.id}/modules`).then((mres) =>
          setModulesByProgramme((prev) => ({ ...prev, [p.id]: mres.data }))
        );
      });
    });
  }, [user]);

  return (
    <Layout>
      <div className="page-header"><h1>My modules</h1></div>
      {programmes.length === 0 && <div className="card placeholder-page">No programme assigned yet.</div>}
      {programmes.map((p) => (
        <div key={p.id} className="card" style={{ marginBottom: 16 }}>
          <strong>{p.title}</strong>
          <div className="stat-grid" style={{ marginTop: 10 }}>
            {(modulesByProgramme[p.id] || []).map((m) => (
              <div key={m.id} className="card" style={{ boxShadow: "none" }}>
                <div style={{ fontWeight: 600 }}>{m.title}</div>
                <div style={{ fontSize: 12.5, color: "var(--text-muted)" }}>{m.lesson_count} lessons</div>
                <Link className="btn" style={{ marginTop: 8, display: "inline-block" }} to={`/learn/lesson/1`}>
                  Continue
                </Link>
              </div>
            ))}
          </div>
        </div>
      ))}
    </Layout>
  );
}
