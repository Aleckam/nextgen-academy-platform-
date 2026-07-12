import { useEffect, useState } from "react";
import client from "../../api/client";
import Layout from "../../components/Layout";
import StatCard from "../../components/StatCard";

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    client.get("/admin/overview").then((res) => setStats(res.data));
  }, []);

  if (!stats) return <Layout><div className="card">Loading…</div></Layout>;

  return (
    <Layout>
      <div className="page-header"><h1>Admin overview</h1></div>
      <div className="stat-grid">
        <StatCard value={stats.total_users} label="Total users" />
        <StatCard value={stats.total_students} label="Students" />
        <StatCard value={stats.total_schools} label="Schools" tone="amber" />
        <StatCard value={stats.active_subscriptions} label="Active subscriptions" tone="green" />
        <StatCard value={stats.certificates_issued} label="Certificates issued" tone="green" />
        <StatCard value={stats.lessons_completed} label="Lessons completed" />
      </div>
    </Layout>
  );
}
