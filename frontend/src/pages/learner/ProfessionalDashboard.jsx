import { useEffect, useState } from "react";
import client from "../../api/client";
import Layout from "../../components/Layout";
import { useAuth } from "../../context/AuthContext";

/** Professional dashboard — progress rings, module navigation, resource
 * downloads (§3.4). */
export default function ProfessionalDashboard() {
  const { user } = useAuth();
  const [programmes, setProgrammes] = useState([]);

  useEffect(() => {
    client.get("/content/programmes", { params: { age_group: "professional" } }).then((res) => setProgrammes(res.data));
  }, []);

  return (
    <Layout>
      <div className="page-header"><h1>Welcome, {user?.name}</h1></div>
      {programmes.length === 0 && <div className="card placeholder-page">No professional-track programme published yet.</div>}
      <div className="stat-grid">
        {programmes.map((p) => (
          <div key={p.id} className="card">
            <strong>{p.title}</strong>
            <p style={{ color: "var(--text-muted)", fontSize: 13 }}>{p.description}</p>
          </div>
        ))}
      </div>
    </Layout>
  );
}
