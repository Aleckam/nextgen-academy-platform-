import { useState } from "react";
import client from "../../api/client";
import Layout from "../../components/Layout";

/** Blog CMS — create, edit, publish articles (§3.6). */
export default function BlogCMS() {
  const [form, setForm] = useState({ title: "", slug: "", category: "Financial Literacy", body: "", status: "draft" });
  const [message, setMessage] = useState(null);

  const submit = async (e) => {
    e.preventDefault();
    await client.post("/blog", form);
    setMessage("Saved.");
    setForm({ title: "", slug: "", category: "Financial Literacy", body: "", status: "draft" });
  };

  return (
    <Layout>
      <div className="page-header"><h1>Blog CMS</h1></div>
      <div className="card" style={{ maxWidth: 560 }}>
        <form onSubmit={submit}>
          <label>Title</label>
          <input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} style={inputStyle} />
          <label>Slug</label>
          <input value={form.slug} onChange={(e) => setForm({ ...form, slug: e.target.value })} style={inputStyle} />
          <label>Category</label>
          <select value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} style={inputStyle}>
            {["Kids & Money", "ZSE & Investing", "Zimbabwe Focus", "AI & Finance", "Financial Literacy"].map((c) => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
          <label>Body</label>
          <textarea value={form.body} onChange={(e) => setForm({ ...form, body: e.target.value })} rows={6} style={inputStyle} />
          <label>
            <input type="checkbox" checked={form.status === "published"} onChange={(e) => setForm({ ...form, status: e.target.checked ? "published" : "draft" })} /> Publish now
          </label>
          <div style={{ marginTop: 10 }}>
            <button className="btn primary">Save</button>
            {message && <span style={{ marginLeft: 10, color: "var(--green)" }}>{message}</span>}
          </div>
        </form>
      </div>
    </Layout>
  );
}

const inputStyle = { display: "block", width: "100%", padding: 8, marginBottom: 12, borderRadius: 6, border: "1px solid var(--border)" };
