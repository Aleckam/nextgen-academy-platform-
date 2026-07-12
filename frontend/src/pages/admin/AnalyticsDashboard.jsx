import Layout from "../../components/Layout";
import PlaceholderPage from "../../components/PlaceholderPage";

/** Basic analytics dashboard (§7, Should Have). AdminDashboard already
 * surfaces the core counters via GET /api/admin/overview — extend that
 * endpoint with time-series data before building charts here. */
export default function AnalyticsDashboard() {
  return (
    <Layout>
      <PlaceholderPage title="Analytics" note="See Admin Overview for current counters; add time-series endpoints for trend charts." />
    </Layout>
  );
}
