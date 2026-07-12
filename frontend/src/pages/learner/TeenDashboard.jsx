import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import client from "../../api/client";
import Layout from "../../components/Layout";
import { useAuth } from "../../context/AuthContext";

/** Ages 13-18 dashboard — module progress cards, virtual ZSE portfolio
 * widget, leaderboard (§3.4). The portfolio widget shows illustrative data
 * only (no live market data integration is defined in §6 — add one before
 * treating these prices as real). */
export default function TeenDashboard() {
  const { user } = useAuth();
  const [programmes, setProgrammes] = useState([]);

  useEffect(() => {
    client.get("/content/programmes", { params: { age_group: "13-18" } }).then((res) => setProgrammes(res.data));
  }, []);

  return (
    <Layout>
      <div className="page-header"><h1>Welcome back, {user?.name?.split(" ")[0]}</h1></div>
      <div className="two-col">
        <div className="card">
          <strong>Your programmes</strong>
          {programmes.map((p) => (
            <div key={p.id} style={{ padding: "10px 0", borderBottom: "1px solid var(--border)" }}>
              {p.title}
              <Link className="btn" style={{ marginLeft: 10 }} to="/learn/modules">Open</Link>
            </div>
          ))}
        </div>
        <div className="card">
          <strong>Your virtual portfolio (illustrative)</strong>
          <div style={{ fontSize: 24, fontWeight: 700, marginTop: 6 }}>$1,087.40</div>
          <div style={{ color: "var(--green)", fontSize: 13 }}>+$87.40 (+8.7%) since start</div>
        </div>
      </div>
    </Layout>
  );
}
