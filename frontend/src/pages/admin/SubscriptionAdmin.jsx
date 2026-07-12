import { useEffect, useState } from "react";
import client from "../../api/client";
import Layout from "../../components/Layout";

/** Subscription & billing admin, payment reconciliation (§3.2). */
export default function SubscriptionAdmin() {
  const [subs, setSubs] = useState([]);

  useEffect(() => {
    client.get("/subscriptions/admin").then((res) => setSubs(res.data));
  }, []);

  return (
    <Layout>
      <div className="page-header"><h1>Subscriptions &amp; billing</h1></div>
      <div className="card">
        {subs.length === 0 && <div className="placeholder-page">No subscriptions yet.</div>}
        <table className="data-table">
          <thead><tr><th>Account type</th><th>Tier</th><th>Status</th><th>Provider</th></tr></thead>
          <tbody>
            {subs.map((s) => (
              <tr key={s.id}>
                <td>{s.account_type}</td>
                <td>{s.tier}</td>
                <td><span className="badge on-track">{s.status}</span></td>
                <td>{s.payment_provider}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Layout>
  );
}
