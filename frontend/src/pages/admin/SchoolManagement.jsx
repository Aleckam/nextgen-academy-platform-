import { useEffect, useState } from "react";
import client from "../../api/client";
import Layout from "../../components/Layout";

export default function SchoolManagement() {
  const [schools, setSchools] = useState([]);
  const [name, setName] = useState("");

  const load = () => client.get("/admin/schools").then((res) => setSchools(res.data));
  useEffect(() => { load(); }, []);

  const create = async (e) => {
    e.preventDefault();
    await client.post("/schools", { name });
    setName("");
    load();
  };

  return (
    <Layout>
      <div className="page-header"><h1>School management</h1></div>
      <div className="card" style={{ marginBottom: 16 }}>
        <form onSubmit={create} style={{ display: "flex", gap: 8 }}>
          <input value={name} onChange={(e) => setName(e.target.value)} placeholder="New school name" style={{ flex: 1, padding: 8, borderRadius: 6, border: "1px solid var(--border)" }} />
          <button className="btn primary">Add school</button>
        </form>
      </div>
      <div className="card">
        <table className="data-table">
          <thead><tr><th>Name</th><th>Term</th><th>Year</th></tr></thead>
          <tbody>
            {schools.map((s) => (
              <tr key={s.id}><td>{s.name}</td><td>{s.term_label}</td><td>{s.academic_year}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </Layout>
  );
}
