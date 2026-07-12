import { useEffect, useState } from "react";
import client from "../../api/client";
import Layout from "../../components/Layout";

/** Payment & subscription screen (§7 Must Have). Paynow (local) / Stripe
 * (USD) checkout redirect is not implemented in this scaffold — see
 * backend/app/api/subscriptions.py for the pending-subscription + webhook
 * shape it expects. */
export default function PaymentSubscription() {
  const [subscription, setSubscription] = useState(null);

  useEffect(() => {
    client.get("/subscriptions/mine").then((res) => setSubscription(res.data));
  }, []);

  return (
    <Layout>
      <div className="page-header"><h1>Subscription</h1></div>
      <div className="card">
        {subscription ? (
          <>
            <span className="badge on-track">{subscription.status}</span>
            <div style={{ marginTop: 8 }}>{subscription.tier} · {subscription.account_type}</div>
            <div style={{ color: "var(--text-muted)", fontSize: 13 }}>via {subscription.payment_provider}</div>
          </>
        ) : (
          <div className="placeholder-page">
            No active subscription. Checkout (Paynow / Stripe) is not wired up in this scaffold —
            see backend/app/api/subscriptions.py.
          </div>
        )}
      </div>
    </Layout>
  );
}
