import { Link } from "react-router-dom";
import Layout from "../../components/Layout";

/** Teacher accounts — read-only class dashboard, resource library, no
 * marking required (§3.5). Reuses the class view; a real build should
 * resolve the teacher's own class id from the JWT rather than hardcoding. */
export default function TeacherDashboard() {
  return (
    <Layout>
      <div className="page-header"><h1>My class</h1></div>
      <div className="card">
        <p>Read-only view of your class's progress — no marking required.</p>
        <Link className="btn primary" to="/school/classes/1">Open class view</Link>
      </div>
    </Layout>
  );
}
