import { useEffect, useState } from "react";
import client from "../../api/client";
import Layout from "../../components/Layout";

export default function UserManagement() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    client.get("/admin/users").then((res) => setUsers(res.data));
  }, []);

  return (
    <Layout>
      <div className="page-header"><h1>User management</h1></div>
      <div className="card">
        <table className="data-table">
          <thead><tr><th>Name</th><th>Role</th><th>Account type</th><th>School</th></tr></thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id}>
                <td>{u.name}</td>
                <td><span className="badge on-track">{u.role}</span></td>
                <td>{u.account_type}</td>
                <td>{u.school_id ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Layout>
  );
}
