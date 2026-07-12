import { useEffect, useState } from "react";
import client from "../../api/client";
import Layout from "../../components/Layout";
import StatCard from "../../components/StatCard";
import { useAuth } from "../../context/AuthContext";

/** Ages 7-12 dashboard — gamified progress map, NextGen Coin balance, streak
 * (§3.4). Coin balance / streak are not yet backed by dedicated DB fields in
 * this scaffold (see backend/app/models/content.py Quiz.coin_reward for the
 * award side) — wire up a wallet/streak table before shipping. */
export default function KidsDashboard() {
  const { user } = useAuth();
  const [certs, setCerts] = useState([]);

  useEffect(() => {
    client.get("/certificates/mine").then((res) => setCerts(res.data));
  }, []);

  return (
    <Layout>
      <div className="page-header"><h1>Hi {user?.name?.split(" ")[0]}! 🎉</h1></div>
      <div className="stat-grid">
        <StatCard value="—" label="NextGen Coins (wire up wallet)" tone="amber" />
        <StatCard value="—" label="Lesson streak (wire up streak tracker)" />
        <StatCard value={certs.length} label="Certificates earned" tone="green" />
      </div>
      <div className="card">
        <strong>Your progress map</strong>
        <p className="placeholder-page">Gamified map view — build atop /api/content lesson progress.</p>
      </div>
    </Layout>
  );
}
