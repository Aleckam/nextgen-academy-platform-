import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import client from "../../api/client";
import PublicLayout from "../../components/PublicLayout";

export default function BlogListPage() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    client.get("/blog").then((res) => setPosts(res.data));
  }, []);

  return (
    <PublicLayout>
      <h1>Blog</h1>
      {posts.length === 0 && <div className="card placeholder-page">No published articles yet.</div>}
      {posts.map((p) => (
        <Link key={p.id} to={`/blog/${p.slug}`} style={{ display: "block", marginBottom: 12 }}>
          <div className="card">
            <span className="badge on-track">{p.category}</span>
            <h3 style={{ margin: "8px 0 4px" }}>{p.title}</h3>
            <p style={{ color: "var(--text-muted)", fontSize: 13.5 }}>{p.excerpt}</p>
          </div>
        </Link>
      ))}
    </PublicLayout>
  );
}
