import { useEffect, useState } from "react";
import client from "../../api/client";
import Layout from "../../components/Layout";

/** School subscription management — renewal, billing, add/remove students
 * (§3.5). */
export default function SchoolSubscription() {
  const [subscription, setSubscription] = useState(null);

  useEffect(() => {
    client.get("/subscriptions/mine").then((res) => setSubscription(res.data));
  }, []);

  return (
    <Layout>
      <div className="page-header"><h1>School subscription</h1></div>
      <div className="card">
        {subscription ? (
          <>
            <span className="badge on-track">{subscription.status}</span>
            <div style={{ marginTop: 8 }}>{subscription.tier} · {subscription.seats} seats</div>
            <div style={{ color: "var(--text-muted)", fontSize: 13 }}>
              Renews {subscription.renewal_date ? new Date(subscription.renewal_date).toLocaleDateString() : "—"}
            </div>
          </>
        ) : (
          <div className="placeholder-page">No active subscription on file.</div>
        )}
      </div>
    </Layout>
  );
}
