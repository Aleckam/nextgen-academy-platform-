import { useEffect, useState } from "react";
import client from "../../api/client";
import Layout from "../../components/Layout";

/** Parent view — child progress overview, certificate gallery, subscription
 * management (§3.4). Assumes children are linked via User.parent_id. */
export default function ParentDashboard() {
  const [subscription, setSubscription] = useState(null);

  useEffect(() => {
    client.get("/subscriptions/mine").then((res) => setSubscription(res.data));
  }, []);

  return (
    <Layout>
      <div className="page-header"><h1>Family dashboard</h1></div>
      <div className="card" style={{ marginBottom: 16 }}>
        <strong>Subscription</strong>
        {subscription ? (
          <div style={{ marginTop: 8 }}>
            <span className="badge on-track">{subscription.status}</span> {subscription.tier} · {subscription.account_type}
          </div>
        ) : (
          <div className="placeholder-page">No active subscription.</div>
        )}
      </div>
      <div className="card placeholder-page">
        Child progress overview — list children linked via User.parent_id, each with completion % and
        certificate count (join LessonProgress / Certificate on child user ids).
      </div>
    </Layout>
  );
}
