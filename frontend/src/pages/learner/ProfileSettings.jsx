import { useState } from "react";
import client from "../../api/client";
import Layout from "../../components/Layout";
import { useAuth } from "../../context/AuthContext";

/** Profile management — name, age group, profile photo (§3.1, §7 Should Have). */
export default function ProfileSettings() {
  const { user } = useAuth();
  const [name, setName] = useState(user?.name || "");
  const [saved, setSaved] = useState(false);

  const save = async (e) => {
    e.preventDefault();
    await client.patch("/users/me", { name });
    setSaved(true);
  };

  return (
    <Layout>
      <div className="page-header"><h1>Profile &amp; settings</h1></div>
      <div className="card" style={{ maxWidth: 420 }}>
        <form onSubmit={save}>
          <label>Name</label>
          <input value={name} onChange={(e) => setName(e.target.value)} style={{ display: "block", width: "100%", padding: 8, marginBottom: 12, borderRadius: 6, border: "1px solid var(--border)" }} />
          <button className="btn primary">Save</button>
          {saved && <span style={{ marginLeft: 10, color: "var(--green)", fontSize: 13 }}>Saved</span>}
        </form>
      </div>
    </Layout>
  );
}
