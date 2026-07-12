import { useEffect, useState } from "react";
import client from "../../api/client";
import Layout from "../../components/Layout";

/** Certificate gallery in student profile (§3.7). */
export default function CertificatePage() {
  const [certs, setCerts] = useState([]);

  useEffect(() => {
    client.get("/certificates/mine").then((res) => setCerts(res.data));
  }, []);

  return (
    <Layout>
      <div className="page-header"><h1>My certificates</h1></div>
      {certs.length === 0 && <div className="card placeholder-page">Complete a module to earn your first certificate.</div>}
      <div className="stat-grid">
        {certs.map((c) => (
          <div key={c.id} className="card">
            <div className="badge on-track">Verified</div>
            <div style={{ fontWeight: 600, marginTop: 8 }}>Module {c.module_id}</div>
            <div style={{ fontSize: 12.5, color: "var(--text-muted)" }}>
              Issued {new Date(c.issued_at).toLocaleDateString()}
            </div>
            <img src={`/api/certificates/${c.id}/qr.png`} alt="Verification QR" style={{ width: 80, marginTop: 8 }} />
          </div>
        ))}
      </div>
    </Layout>
  );
}
